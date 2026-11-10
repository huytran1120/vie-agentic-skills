#!/usr/bin/env python3
"""Tests for google/skills import, packaging, and CLI workflows."""

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


class TestGoogleSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.import_manifest_path = ROOT / "data/google-skills-import.json"
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
        self.assertEqual(self.imported["source_repo"], "google/skills")
        self.assertEqual(self.imported["revision"], "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee")
        self.assertEqual(self.imported["skill_count"], 184)

        # Verify skipped duplicates
        skipped_ids = {s["id"] for s in self.imported["skipped"]}
        self.assertEqual(skipped_ids, {"firebase-basics", "gemini-interactions-api", "retrieving-developer-knowledge"})

        # Verify source-credits.json
        self.assertIn("googleskills", self.credits["sections"])
        self.assertIn("google/skills", self.credits["sections"]["googleskills"][0])
        self.assertIn("2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee", self.credits["sections"]["googleskills"][0])

        # Verify category taxonomy remains exactly 119 and catalog has 4,076 skills
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4076)

        sample_skills = [
            ("gcloud", "cloud"),
            ("bigquery-basics", "data-engineering"),
            ("cloud-run-basics", "cloud"),
            ("spanner-basics", "database"),
            ("gke-basics", "devops"),
            ("google-ads-api-quickstart", "marketing"),
            ("secops-hunt", "security"),
            ("developing-genkit-go", "ai-ml"),
            ("google-analytics-data-api-basics", "data"),
            ("google-cloud-waf-reliability", "architecture"),
        ]

        for sid, expected_cat in sample_skills:
            self.assertIn(sid, self.skills_by_id)
            skill = self.skills_by_id[sid]
            self.assertEqual(skill["canonical_id"], sid)
            self.assertEqual(skill["category"], expected_cat)
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["license"], "Apache-2.0")
            self.assertEqual(skill["author"], "Google")
            self.assertEqual(skill["source_repo"], "google/skills")
            self.assertEqual(skill["source_revision"], "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee")

    def test_standalone_file_inventory_and_modes(self):
        files = self.imported["files"]
        self.assertGreaterEqual(len(files), 1600)

        for record in files:
            file_path = ROOT / record["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), record["sha256"], f"Checksum mismatch: {file_path}")

            if record["executable"]:
                st = os.stat(file_path)
                self.assertTrue(bool(st.st_mode & 0o111), f"Expected executable bit on {file_path}")

        # Check each skill has LICENSE, NOTICE.md, and SKILL.md
        for skill in self.imported["skills"]:
            skill_dir = ROOT / "skills" / skill["id"]
            self.assertTrue((skill_dir / "LICENSE").is_file(), f"Missing LICENSE in {skill_dir}")
            self.assertTrue((skill_dir / "NOTICE.md").is_file(), f"Missing NOTICE.md in {skill_dir}")
            self.assertTrue((skill_dir / "SKILL.md").is_file(), f"Missing SKILL.md in {skill_dir}")

            # Verify SKILL.md ends with installation notes
            skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## VAS installation notes", skill_md_text)
            self.assertIn(f"Canonical ID: `{skill['id']}`", skill_md_text)
            self.assertIn("Apache-2.0", skill_md_text)

    def test_independent_cli_installation_and_clean_removal(self):
        skill_id = "gcloud"
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

            # 5. Clean uninstall
            res = cli("uninstall", skill_id, "--target", "workspace", "--dest", str(dest_dir), cwd=cwd)
            self.assertEqual(res.returncode, 0, f"Uninstall failed: {res.stderr}")
            self.assertFalse(installed_skill_dir.exists())

    def test_pages_manifest_generation_and_checksums(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("gcloud", manifests)
        m = manifests["gcloud"]
        self.assertEqual(m["skill_id"], "gcloud")
        self.assertEqual(m["target_name"], "gcloud")
        self.assertEqual(m["provenance"]["source_repo"], "google/skills")

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
