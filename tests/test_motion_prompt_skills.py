#!/usr/bin/env python3
"""Tests for showheyohtaki/motion-prompt import, packaging, checksums, and CLI workflows."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import vas as VAS
import build_pages as PAGES


def cli(*args, cwd=ROOT):
    cmd = [sys.executable, str(ROOT / "vas.py"), *args]
    return subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


class TestMotionPromptSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.import_manifest_path = ROOT / "data/motion-prompt-import.json"
        with open(cls.import_manifest_path, "r", encoding="utf-8") as f:
            cls.imported = json.load(f)

        with open(ROOT / "data/catalog.json", "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)

        with open(ROOT / "skills_index.json", "r", encoding="utf-8") as f:
            cls.index = json.load(f)

        with open(ROOT / "data/source-credits.json", "r", encoding="utf-8") as f:
            cls.credits = json.load(f)

        cls.skills_by_id = {s["canonical_id"]: s for s in cls.index}

    def test_import_metadata_and_catalog_presence(self):
        self.assertEqual(self.imported["source_repo"], "showheyohtaki/motion-prompt")
        self.assertEqual(self.imported["revision"], "7819d3879eb7d5a1475c11c001bedffb5cab64af")
        self.assertEqual(self.imported["skill_count"], 1)

        # Verify source-credits.json
        self.assertIn("motionprompt", self.credits["sections"])
        self.assertIn("showheyohtaki/motion-prompt", self.credits["sections"]["motionprompt"][0])
        self.assertIn("7819d3879eb7d5a1475c11c001bedffb5cab64af", self.credits["sections"]["motionprompt"][0])

        # Verify category taxonomy remains 119 and catalog has 4,076 skills
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4076)

        self.assertIn("motion-prompt", self.skills_by_id)
        skill = self.skills_by_id["motion-prompt"]
        self.assertEqual(skill["canonical_id"], "motion-prompt")
        self.assertEqual(skill["category"], "design")
        self.assertEqual(skill["risk"], "safe")
        self.assertEqual(skill["license"], "MIT")
        self.assertEqual(skill["author"], "Shohei Ohtaki (showheyohtaki)")
        self.assertEqual(skill["source_repo"], "showheyohtaki/motion-prompt")
        self.assertEqual(skill["source_revision"], "7819d3879eb7d5a1475c11c001bedffb5cab64af")

    def test_standalone_file_inventory_and_modes(self):
        files = self.imported["files"]
        self.assertEqual(len(files), 6)

        for record in files:
            file_path = ROOT / record["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), record["sha256"], f"Checksum mismatch: {file_path}")

            st = os.stat(file_path)
            is_exec = bool(st.st_mode & 0o111)
            self.assertEqual(is_exec, record["executable"], f"Executable bit mismatch on {file_path}")

        skill_dir = ROOT / "skills/motion-prompt"
        self.assertTrue((skill_dir / "LICENSE").is_file())
        self.assertTrue((skill_dir / "THIRD-PARTY-NOTICES.md").is_file())
        self.assertTrue((skill_dir / "NOTICE.md").is_file())
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertTrue((skill_dir / "references/porting.md").is_file())
        self.assertTrue((skill_dir / "scripts/motion-prompt.mjs").is_file())

        skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_md_text)
        self.assertIn("Canonical ID: `motion-prompt`", skill_md_text)
        self.assertIn("MIT", skill_md_text)

    def test_independent_cli_installation_and_clean_removal(self):
        skill_id = "motion-prompt"
        with tempfile.TemporaryDirectory() as td:
            cwd = Path(td)
            dest_dir = cwd / ".agents/skills"

            # 1. Install via link mode
            res = cli("install", skill_id, "--target", "workspace", "--dest", str(dest_dir), "--mode", "link", cwd=cwd)
            self.assertEqual(res.returncode, 0, f"Install failed: {res.stderr}")
            installed_skill_dir = dest_dir / skill_id
            self.assertTrue(installed_skill_dir.is_dir())
            self.assertTrue((installed_skill_dir / "SKILL.md").exists())
            self.assertTrue((installed_skill_dir / "NOTICE.md").exists())
            self.assertTrue((installed_skill_dir / "LICENSE").exists())
            self.assertTrue((installed_skill_dir / "THIRD-PARTY-NOTICES.md").exists())
            self.assertTrue((installed_skill_dir / "references/porting.md").exists())
            self.assertTrue((installed_skill_dir / "scripts/motion-prompt.mjs").exists())
            self.assertTrue((dest_dir / ".vas-manifest.json").exists())

            # 2. Check status
            res = cli("status", "--target", "workspace", "--dest", str(dest_dir), cwd=cwd)
            self.assertEqual(res.returncode, 0, f"Status failed: {res.stderr}")
            self.assertIn(skill_id, res.stdout)
            self.assertIn("[installed]", res.stdout)

            # 3. Uninstall
            res = cli("uninstall", skill_id, "--target", "workspace", "--dest", str(dest_dir), cwd=cwd)
            self.assertEqual(res.returncode, 0, f"Uninstall failed: {res.stderr}")
            self.assertFalse(installed_skill_dir.exists())

            # 4. Install via copy mode
            res = cli("install", skill_id, "--target", "workspace", "--dest", str(dest_dir), "--mode", "copy", cwd=cwd)
            self.assertEqual(res.returncode, 0, f"Copy install failed: {res.stderr}")
            self.assertTrue(installed_skill_dir.is_dir())
            self.assertFalse((installed_skill_dir / "SKILL.md").is_symlink())
            self.assertTrue((installed_skill_dir / "scripts/motion-prompt.mjs").is_file())

            # 5. Clean uninstall
            res = cli("uninstall", skill_id, "--target", "workspace", "--dest", str(dest_dir), cwd=cwd)
            self.assertEqual(res.returncode, 0, f"Uninstall failed: {res.stderr}")
            self.assertFalse(installed_skill_dir.exists())

    def test_pages_manifest_generation_and_checksums(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("motion-prompt", manifests)
        m = manifests["motion-prompt"]
        self.assertEqual(m["skill_id"], "motion-prompt")
        self.assertEqual(m["target_name"], "motion-prompt")
        self.assertEqual(m["provenance"]["source_repo"], "showheyohtaki/motion-prompt")
        self.assertEqual(len(m["files"]), 6)

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("THIRD-PARTY-NOTICES.md", file_paths)
        self.assertIn("NOTICE.md", file_paths)
        self.assertIn("references/porting.md", file_paths)
        self.assertIn("scripts/motion-prompt.mjs", file_paths)


if __name__ == "__main__":
    unittest.main()
