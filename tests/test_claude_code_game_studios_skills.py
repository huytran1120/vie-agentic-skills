import hashlib
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class ClaudeCodeGameStudiosSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/claude-code-game-studios-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 74)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(len(self.imported["namespaces"]), 5)
        self.assertEqual(self.imported["revision"], "05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3355)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("zero existing duplicates", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("gamestudios", self.credits["sections"])
        self.assertIn("Donchitos/Claude-Code-Game-Studios", self.credits["sections"]["gamestudios"][0])
        self.assertIn("05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418", self.credits["sections"]["gamestudios"][0])
        self.assertIn("MIT", self.credits["sections"]["gamestudios"][0])

        # Check sample skills in skills_index.json
        sample_ids = [
            "start", "brainstorm", "setup-engine", "gate-check", "dev-story",
            "gamestudio-architecture-review", "gamestudio-code-review",
            "gamestudio-design-system", "gamestudio-prototype", "gamestudio-security-audit"
        ]
        for sid in sample_ids:
            self.assertIn(sid, self.skills_by_id)
            skill = self.skills_by_id[sid]
            self.assertEqual(skill["canonical_id"], sid)
            self.assertEqual(skill["category"], "game-development")
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["author"], "Donchitos")
            self.assertIn("MIT", skill["license"])
            self.assertEqual(skill["source_repo"], "Donchitos/Claude-Code-Game-Studios")
            self.assertEqual(skill["source_revision"], "05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418")

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        for sid in sample_ids:
            self.assertIn(sid, cat_by_id)
            cat_entry = cat_by_id[sid]
            self.assertEqual(cat_entry["canonical_id"], sid)
            self.assertEqual(cat_entry["category"], "game-development")
            self.assertEqual(cat_entry["license"], "MIT")
            self.assertEqual(cat_entry["author"], "Donchitos")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 485)

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            # Verify permissions
            is_exec = r["executable"]
            st_mode = file_path.stat().st_mode
            if is_exec:
                self.assertNotEqual(st_mode & 0o111, 0, f"Script should be executable: {file_path}")
            else:
                self.assertEqual(st_mode & 0o111, 0, f"File should not be executable: {file_path}")

            # Verify sha256 checksum
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        # Check key sample skill directories
        for sid in ["setup-engine", "gate-check", "gamestudio-architecture-review"]:
            s_dir = ROOT / "skills" / sid
            self.assertTrue(s_dir.is_dir())
            self.assertTrue((s_dir / "SKILL.md").exists())
            self.assertTrue((s_dir / "LICENSE").exists())
            self.assertTrue((s_dir / "NOTICE.md").exists())

            skill_text = (s_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## VAS installation notes", skill_text)
            self.assertIn(f"Canonical ID: `{sid}`", skill_text)
            self.assertIn("Donchitos/Claude-Code-Game-Studios", skill_text)
            self.assertIn("05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with gamestudio-architecture-review
        with tempfile.TemporaryDirectory(prefix="vas-gamestudio-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "gamestudio-architecture-review",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "gamestudio-architecture-review"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("gamestudio-architecture-review", ledger)
            self.assertEqual(ledger["gamestudio-architecture-review"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "gamestudio-architecture-review", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with setup-engine
        with tempfile.TemporaryDirectory(prefix="vas-gamestudio-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "setup-engine",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "setup-engine"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "references/3-version.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("setup-engine", ledger)
            self.assertEqual(ledger["setup-engine"]["mode"], "copy")
            self.assertEqual(ledger["setup-engine"]["target_name"], "setup-engine")
            self.assertEqual(ledger["setup-engine"]["category"], "game-development")

            uninst_res = cli("uninstall", "setup-engine", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for sid in ["setup-engine", "gate-check", "gamestudio-architecture-review"]:
            self.assertIn(sid, manifests)
            m = manifests[sid]
            self.assertEqual(m["skill_id"], sid)
            self.assertEqual(m["target_name"], sid)
            self.assertEqual(m["provenance"]["category"], "game-development")
            self.assertEqual(m["provenance"]["author"], "Donchitos")
            self.assertEqual(m["provenance"]["source_repo"], "Donchitos/Claude-Code-Game-Studios")

            file_paths = {f["path"] for f in m["files"]}
            self.assertIn("SKILL.md", file_paths)
            self.assertIn("LICENSE", file_paths)
            self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
