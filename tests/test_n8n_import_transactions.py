import contextlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

from test_local_project import ROOT


SPEC = importlib.util.spec_from_file_location("transaction_n8n", ROOT / "scripts/import_n8n_mcp.py")
IMPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORT)


class N8nImportTransactionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="vas-n8n-import-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "skills/n8n-self-hosting"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("Original runbook", encoding="utf-8")
        (self.skill / "local-notes.txt").write_text("Preserve local notes on failure", encoding="utf-8")
        data = self.root / "data"
        data.mkdir()
        self.manifest = data / "n8n-mcp-import.json"
        self.manifest.write_text('{"original": true}\n', encoding="utf-8")
        (data / "source-credits.json").write_text(
            json.dumps({"sections": {"other": ["Keep other credits"], "n8nmcp": ["Old credits"]}}),
            encoding="utf-8",
        )
        (data / "catalog.json").write_text(json.dumps({
            "skills": [{"id": "other", "source_repo": "other/repo"},
                       {"id": "n8n-self-hosting", "source_repo": IMPORT.UPSTREAM_REPO_SLUG}],
            "total": 2,
        }), encoding="utf-8")
        self.upstream = {
            f"data/skills/n8n-self-hosting/{name}": f"Upstream fixture: {name}\n".encode()
            for name in IMPORT.UPSTREAM_FILES
        }
        self.upstream["LICENSE"] = b"MIT license fixture\n"
        self.upstream["data/skills/n8n-self-hosting/SKILL.md"] = (
            b"---\nname: n8n-self-hosting\ndescription: New runbook\n---\n\n# New instructions\n"
        )
        self.before = self.snapshot()

    def snapshot(self):
        return {
            path.relative_to(self.root).as_posix(): (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
            for path in self.root.rglob("*") if path.is_file()
        }

    def run_import(self, fetch=None):
        with patch.object(IMPORT, "REPO_ROOT", self.root), patch.object(
            IMPORT, "fetch_bytes", side_effect=fetch or self.upstream.__getitem__,
        ), contextlib.redirect_stdout(io.StringIO()):
            IMPORT.main()

    def assert_preserved(self):
        self.assertEqual(self.snapshot(), self.before)
        self.assertEqual(list(self.root.glob(".n8n-import-*")), [])

    def test_license_download_failure_preserves_existing_import(self):
        with self.assertRaisesRegex(OSError, "Network unavailable"):
            self.run_import(OSError("Network unavailable"))
        self.assert_preserved()

    def test_late_download_failure_preserves_payload_and_metadata(self):
        def fetch(path):
            if path.endswith("assets/init-data.sh"):
                raise OSError("Download interrupted")
            return self.upstream[path]
        with self.assertRaisesRegex(OSError, "Download interrupted"):
            self.run_import(fetch)
        self.assert_preserved()

    def test_invalid_runbook_does_not_replace_existing_import(self):
        self.upstream["data/skills/n8n-self-hosting/SKILL.md"] = b"Not a skill runbook"
        with self.assertRaises(ValueError):
            self.run_import()
        self.assert_preserved()

    def test_empty_license_does_not_replace_existing_import(self):
        self.upstream["LICENSE"] = b""
        with self.assertRaises(ValueError):
            self.run_import()
        self.assert_preserved()

    def test_invalid_catalog_does_not_publish_partial_updates(self):
        (self.root / "data/catalog.json").write_text("{invalid", encoding="utf-8")
        self.before = self.snapshot()
        with self.assertRaises(json.JSONDecodeError):
            self.run_import()
        self.assert_preserved()

    def test_staging_write_failure_preserves_existing_import(self):
        write = Path.write_text
        def fail_staged_catalog(path, *args, **kwargs):
            if path.name == "catalog.json" and path != self.root / "data/catalog.json":
                raise OSError("Staging storage unavailable")
            return write(path, *args, **kwargs)
        with patch.object(Path, "write_text", fail_staged_catalog):
            with self.assertRaisesRegex(OSError, "Staging storage unavailable"):
                self.run_import()
        self.assert_preserved()

    def test_corrupted_staged_payload_is_not_published(self):
        prepare = IMPORT.stage_import
        def corrupt(staging_root):
            counts = prepare(staging_root)
            (staging_root / "skills/n8n-self-hosting/SKILL.md").write_text("Corrupted payload")
            return counts
        with patch.object(IMPORT, "stage_import", side_effect=corrupt):
            with self.assertRaisesRegex(ValueError, "Invalid staged import file"):
                self.run_import()
        self.assert_preserved()

    def test_success_publishes_complete_payload_hashes_modes_and_metadata(self):
        original_paths = list(self.before)
        def fetch(path):
            for name in original_paths:
                self.assertEqual((self.root / name).read_bytes(), self.before[name][0])
            return self.upstream[path]
        self.run_import(fetch)
        manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["files"]), len(IMPORT.UPSTREAM_FILES) + 2)
        self.assertEqual(
            {path.relative_to(self.skill).as_posix() for path in self.skill.rglob("*") if path.is_file()},
            {*IMPORT.UPSTREAM_FILES, "LICENSE", "NOTICE.md"},
        )
        for record in manifest["files"]:
            path = self.root / record["path"]
            self.assertEqual(IMPORT.sha256_file(path), record["sha256"])
            self.assertEqual(bool(path.stat().st_mode & 0o111), record["executable"])
            if record["source_path"] in self.upstream:
                self.assertEqual(
                    IMPORT.sha256_bytes(self.upstream[record["source_path"]]), record["source_sha256"],
                )
        credits = json.loads((self.root / "data/source-credits.json").read_text())
        self.assertEqual(credits["sections"]["other"], ["Keep other credits"])
        self.assertIn(IMPORT.UPSTREAM_REV, credits["sections"]["n8nmcp"][0])
        catalog = json.loads((self.root / "data/catalog.json").read_text())
        self.assertEqual(catalog["total"], 2)
        self.assertEqual({skill["id"] for skill in catalog["skills"]}, {"other", "n8n-self-hosting"})
        self.assertEqual(list(self.root.glob(".n8n-import-*")), [])

    def test_publish_failure_rolls_back_payload_and_all_metadata(self):
        rename = Path.rename
        failed = False
        def fail_catalog(source, target):
            nonlocal failed
            if Path(target) == self.root / "data/catalog.json" and not failed:
                failed = True
                raise OSError("Cannot publish catalog")
            return rename(source, target)
        with patch.object(Path, "rename", fail_catalog):
            with self.assertRaisesRegex(OSError, "Cannot publish catalog"):
                self.run_import()
        self.assertTrue(failed)
        self.assert_preserved()

    def test_first_import_publish_failure_leaves_no_partial_skill(self):
        self.skill.rename(self.root / "previous-fixture")
        self.manifest.unlink()
        self.before = self.snapshot()
        rename = Path.rename
        def fail_new_manifest(source, target):
            if Path(target) == self.manifest:
                raise OSError("Cannot publish import manifest")
            return rename(source, target)
        with patch.object(Path, "rename", fail_new_manifest):
            with self.assertRaisesRegex(OSError, "Cannot publish import manifest"):
                self.run_import()
        self.assert_preserved()
        self.assertFalse(self.skill.exists())
        self.assertFalse(self.manifest.exists())

    def test_failed_rollback_retains_original_payload_backup(self):
        rename = Path.rename
        def fail_publish_and_restore(source, target):
            if Path(target) == self.root / "data/catalog.json" and "backup" not in source.parts:
                raise OSError("Cannot publish catalog")
            if Path(target) == self.skill and "backup" in source.parts:
                raise OSError("Cannot restore payload")
            return rename(source, target)
        stderr = io.StringIO()
        with patch.object(Path, "rename", fail_publish_and_restore), contextlib.redirect_stderr(stderr):
            with self.assertRaisesRegex(OSError, "Cannot restore payload"):
                self.run_import()
        staging = list(self.root.glob(".n8n-import-*"))
        self.assertEqual(len(staging), 1)
        backup = staging[0] / "backup/skills/n8n-self-hosting"
        self.assertEqual((backup / "SKILL.md").read_text(), "Original runbook")
        self.assertEqual((backup / "local-notes.txt").read_text(), "Preserve local notes on failure")
        self.assertIn(str(staging[0]), stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
