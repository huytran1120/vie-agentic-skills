#!/usr/bin/env python3
"""Tests for claude-awesome-video-creation skill import, packaging, and CLI workflows."""

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


class TestVideoCreationSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.import_manifest_path = ROOT / "data/video-creation-import.json"
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
        self.assertEqual(self.imported["source_repo"], "HaochenSHI66/claude-awesome-video-creation")
        self.assertEqual(self.imported["revision"], "4b0f8d89d50046ac13003e95bcde081e328c2373")
        self.assertEqual(self.imported["license"], "MIT")

        # Verify source-credits.json
        self.assertIn("videocreation", self.credits["sections"])
        self.assertIn("HaochenSHI66/claude-awesome-video-creation", self.credits["sections"]["videocreation"][0])
        self.assertIn("4b0f8d89d50046ac13003e95bcde081e328c2373", self.credits["sections"]["videocreation"][0])
        self.assertIn("MIT", self.credits["sections"]["videocreation"][0])

        # Verify category taxonomy remains exactly 119
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4073)

        sid = "claude-awesome-video-creation"
        self.assertIn(sid, self.skills_by_id)
        skill = self.skills_by_id[sid]
        self.assertEqual(skill["canonical_id"], sid)
        self.assertEqual(skill["category"], "media")
        self.assertEqual(skill["risk"], "safe")
        self.assertIn("HaochenSHI66", skill["author"])
        self.assertEqual(skill["license"], "MIT")
        self.assertEqual(skill["source_repo"], "HaochenSHI66/claude-awesome-video-creation")
        self.assertEqual(skill["source_revision"], "4b0f8d89d50046ac13003e95bcde081e328c2373")
        self.assertIn("video", skill["tags"])
        self.assertIn("remotion", skill["tags"])

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        self.assertIn(sid, cat_by_id)
        cat_entry = cat_by_id[sid]
        self.assertEqual(cat_entry["canonical_id"], sid)
        self.assertEqual(cat_entry["category"], "media")
        self.assertEqual(cat_entry["license"], "MIT")
        self.assertIn("HaochenSHI66", cat_entry["author"])

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 194)

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        # Check key files in claude-awesome-video-creation
        skill_dir = ROOT / "skills/claude-awesome-video-creation"
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertTrue((skill_dir / "LICENSE").exists())
        self.assertTrue((skill_dir / "NOTICE.md").exists())
        self.assertTrue((skill_dir / "LICENSE.txt").exists())
        self.assertTrue((skill_dir / "references/cinetic-core.md").exists())
        self.assertTrue((skill_dir / "references/craft-rules.md").exists())
        self.assertTrue((skill_dir / "references/technique-library.md").exists())
        self.assertTrue((skill_dir / "scripts/sheet.sh").exists())
        self.assertTrue((skill_dir / "scripts/key_magenta.py").exists())
        self.assertTrue((skill_dir / "scripts/render_segments.sh").exists())
        self.assertTrue((skill_dir / "scripts/check_static.py").exists())
        self.assertTrue((skill_dir / "assets/remotion-starter/package.json").exists())
        self.assertTrue((skill_dir / "assets/remotion-starter/remotion.config.ts").exists())

        # Check executable bits
        executable_scripts = [
            skill_dir / "scripts/sheet.sh",
            skill_dir / "scripts/key_magenta.py",
            skill_dir / "scripts/render_segments.sh",
            skill_dir / "scripts/check_static.py",
        ]
        for s in executable_scripts:
            self.assertTrue(os.access(s, os.X_OK), f"Script not executable: {s}")

        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_text)
        self.assertIn("Canonical ID: `claude-awesome-video-creation`", skill_text)
        self.assertIn("HaochenSHI66/claude-awesome-video-creation", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with claude-awesome-video-creation
        with tempfile.TemporaryDirectory(prefix="vas-video-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "claude-awesome-video-creation",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "claude-awesome-video-creation"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "scripts/sheet.sh").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("claude-awesome-video-creation", ledger)
            self.assertEqual(ledger["claude-awesome-video-creation"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "claude-awesome-video-creation", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with claude-awesome-video-creation
        with tempfile.TemporaryDirectory(prefix="vas-video-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "claude-awesome-video-creation",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "claude-awesome-video-creation"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "references/cinetic-core.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("claude-awesome-video-creation", ledger)
            self.assertEqual(ledger["claude-awesome-video-creation"]["mode"], "copy")
            self.assertEqual(ledger["claude-awesome-video-creation"]["target_name"], "claude-awesome-video-creation")
            self.assertEqual(ledger["claude-awesome-video-creation"]["category"], "media")

            uninst_res = cli("uninstall", "claude-awesome-video-creation", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("claude-awesome-video-creation", manifests)
        m = manifests["claude-awesome-video-creation"]
        self.assertEqual(m["skill_id"], "claude-awesome-video-creation")
        self.assertEqual(m["target_name"], "claude-awesome-video-creation")
        self.assertIn("HaochenSHI66", m["provenance"]["author"])
        self.assertEqual(m["provenance"]["source_repo"], "HaochenSHI66/claude-awesome-video-creation")

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("NOTICE.md", file_paths)
        self.assertIn("scripts/sheet.sh", file_paths)
        self.assertIn("references/cinetic-core.md", file_paths)
        self.assertEqual(len(m["files"]), 194)


if __name__ == "__main__":
    unittest.main()
