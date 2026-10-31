import ast
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("local_vas", ROOT / "vas.py")
VAS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VAS)
DOCUMENT_IDS = ("pdf", "docx", "pptx", "xlsx")


def cli(*args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, "-B", str(ROOT / "vas.py"), *args],
        cwd=cwd, text=True, capture_output=True, timeout=30,
    )


class LocalProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = VAS.load_index()
        cls.by_id = {skill["id"]: skill for skill in cls.index}

    def test_project_identity_preserves_vas_entry_point(self):
        package = json.loads((ROOT / "package.json").read_text())
        self.assertEqual(package["name"], "vie-agentic-skill")
        self.assertTrue(package["private"])
        self.assertEqual(package["bin"], {"vas": "vas"})
        self.assertEqual(package["repository"], {
            "type": "git",
            "url": "git+https://github.com/huytran1120/vie-agentic-skills.git",
        })
        self.assertTrue(os.access(ROOT / "vas", os.X_OK))
        result = cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage: vas", result.stdout)
        self.assertIn("Vie Agentic Skill", result.stdout)

    def test_meta_skill_alias_and_relative_link(self):
        self.assertEqual(
            VAS.resolve_skill_id("vietnam-agentic-skills", self.by_id),
            "vie-agentic-skill",
        )
        link = ROOT / ".agents/skills/vie-agentic-skill"
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), ROOT / "skills/vie-agentic-skill")
        self.assertFalse((ROOT / "skills/vietnam-agentic-skills").exists())

    def test_document_runbooks_are_original_and_have_valid_examples(self):
        for skill_id in DOCUMENT_IDS:
            with self.subTest(skill=skill_id):
                directory = ROOT / "skills" / skill_id
                self.assertEqual(
                    sorted(path.name for path in directory.iterdir()), ["SKILL.md"]
                )
                metadata = self.by_id[skill_id]
                self.assertEqual(metadata["license"], "MIT")
                self.assertEqual(metadata["author"], "Vie Agentic Skill contributors")
                self.assertEqual(metadata["source"], "local-original")
                self.assertNotIn("source_repo", metadata)
                self.assertEqual(
                    metadata["source_path"], f"skills/{skill_id}/SKILL.md"
                )
                text = (directory / "SKILL.md").read_text()
                self.assertIn("independently authored", text)
                examples = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
                self.assertGreaterEqual(len(examples), 1)
                for example in examples:
                    ast.parse(example)

    def test_catalog_retains_all_skills_and_matches_local_scan(self):
        self.assertEqual(len(self.index), 3186)
        self.assertEqual(len(self.by_id), len(self.index))
        self.assertEqual(len({s["category"] for s in self.index}), 119)
        self.assertEqual(VAS.scan_skills_locally(), self.index)
        website = json.loads((ROOT / "docs/skills.min.json").read_text())
        self.assertEqual(website, self.index)
        for skill in self.index:
            with self.subTest(skill=skill["id"]):
                directory = ROOT / skill["path"]
                self.assertTrue(directory.resolve().is_relative_to(ROOT))
                self.assertTrue((directory / "SKILL.md").is_file())

    def test_source_metadata_identifies_local_replacements(self):
        for filename in ("data/catalog.json", "data/skills_index.json"):
            data = json.loads((ROOT / filename).read_text())
            rows = data["skills"] if isinstance(data, dict) else data
            by_id = {row["id"]: row for row in rows}
            for skill_id in DOCUMENT_IDS:
                with self.subTest(file=filename, skill=skill_id):
                    self.assertEqual(by_id[skill_id]["license"], "MIT")
                    self.assertEqual(by_id[skill_id]["source"], "local-original")
                    self.assertEqual(
                        by_id[skill_id]["description"],
                        self.by_id[skill_id]["description"],
                    )
            self.assertIn("vie-agentic-skill", by_id)
            self.assertNotIn("vietnam-agentic-skills", by_id)

    def test_restricted_distribution_is_not_imported(self):
        self.assertFalse((ROOT / "data/aas-v1").exists())
        for skill_id in DOCUMENT_IDS:
            self.assertFalse((ROOT / "skills" / skill_id / "LICENSE.txt").exists())
        credits = json.loads((ROOT / "data/source-credits.json").read_text())
        self.assertIn("local", credits["sections"])
        self.assertIn("Copyright (c) 2026 Huy Tran", (ROOT / "LICENSE").read_text())

    def test_init_creates_rebranded_meta_skill_without_following_symlinks(self):
        source = ROOT / "skills/vie-agentic-skill"
        before = (source / "SKILL.md").read_bytes()
        with tempfile.TemporaryDirectory(prefix="vie-init-") as temp:
            target = Path(temp) / ".agents/skills/vie-agentic-skill"
            target.parent.mkdir(parents=True)
            target.symlink_to(source, target_is_directory=True)
            result = cli("init", cwd=temp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(target.is_symlink())
            self.assertIn("name: vie-agentic-skill", (target / "SKILL.md").read_text())
            self.assertEqual((source / "SKILL.md").read_bytes(), before)

    def test_document_install_status_and_uninstall_round_trip(self):
        ids = (*DOCUMENT_IDS, "vietnam-agentic-skills")
        for mode in ("copy", "link"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix="vie-install-") as temp:
                destination = Path(temp) / "project with spaces" / "skills"
                result = cli("install", *ids, "--mode", mode, "--dest", str(destination))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for skill_id in (*DOCUMENT_IDS, "vie-agentic-skill"):
                    installed = destination / skill_id
                    self.assertEqual(installed.is_symlink(), mode == "link")
                    self.assertEqual(
                        (installed / "SKILL.md").read_bytes(),
                        (ROOT / "skills" / skill_id / "SKILL.md").read_bytes(),
                    )
                manifest = json.loads((destination / ".vas-manifest.json").read_text())
                self.assertEqual(set(manifest), {*DOCUMENT_IDS, "vie-agentic-skill"})
                status = cli("status", "--dest", str(destination))
                self.assertEqual(status.returncode, 0, status.stderr)
                self.assertIn("Total installed: 5", status.stdout)
                removed = cli("uninstall", *ids, "--dest", str(destination))
                self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                self.assertEqual(
                    json.loads((destination / ".vas-manifest.json").read_text()), {}
                )
                self.assertEqual(
                    sorted(p.name for p in destination.iterdir()), [".vas-manifest.json"]
                )

    def test_default_install_still_uses_link_mode(self):
        with tempfile.TemporaryDirectory(prefix="vie-default-") as temp:
            destination = Path(temp) / "skills"
            result = cli("install", "pdf", "--dest", str(destination))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((destination / "pdf").is_symlink())

    def test_missing_skill_fails_explicitly(self):
        with tempfile.TemporaryDirectory(prefix="vie-missing-") as temp:
            result = cli("install", "missing-skill-8743", "--dest", temp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not found or missing SKILL.md", result.stdout)

    def test_sync_output_is_rebranded_and_idempotent(self):
        with tempfile.TemporaryDirectory(prefix="vie-sync-") as temp:
            root = Path(temp)
            (root / "docs").mkdir()
            with (
                patch.object(VAS, "REPO_ROOT", root),
                patch.object(VAS, "INDEX_FILE", root / "skills_index.json"),
                patch.object(VAS, "scan_skills_locally", return_value=self.index),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                VAS.cmd_sync(None)
                paths = ("skills_index.json", "docs/skills.min.json", "CATALOG.md")
                before = {name: (root / name).read_bytes() for name in paths}
                VAS.cmd_sync(None)
                self.assertEqual(
                    before, {name: (root / name).read_bytes() for name in paths}
                )
                self.assertTrue(
                    (root / "CATALOG.md").read_text().startswith("# Vie Agentic Skill")
                )


if __name__ == "__main__":
    unittest.main()
