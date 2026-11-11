#!/usr/bin/env python3
"""Tests for NVIDIA/SkillEvaluator import, packaging, and CLI workflows."""

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


class TestSkillEvaluatorSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.import_manifest_path = ROOT / "data/skillevaluator-import.json"
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
        self.assertEqual(self.imported["source_repo"], "NVIDIA/SkillEvaluator")
        self.assertEqual(self.imported["revision"], "7ae25d2522c9c3b151111fedaa67b814cc3dc5c5")
        self.assertEqual(self.imported["skill_count"], 1)

        # Verify source-credits.json
        self.assertIn("skillevaluator", self.credits["sections"])
        self.assertIn("NVIDIA/SkillEvaluator", self.credits["sections"]["skillevaluator"][0])
        self.assertIn("7ae25d2522c9c3b151111fedaa67b814cc3dc5c5", self.credits["sections"]["skillevaluator"][0])

        # Verify category taxonomy remains 119 and catalog has 4,079 skills
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4079)

        self.assertIn("skillevaluator", self.skills_by_id)
        skill = self.skills_by_id["skillevaluator"]
        self.assertEqual(skill["canonical_id"], "skillevaluator")
        self.assertEqual(skill["category"], "agent-evaluation")
        self.assertEqual(skill["risk"], "safe")
        self.assertEqual(skill["license"], "Apache-2.0")
        self.assertEqual(skill["author"], "Christopher Kevin <christopherk@nvidia.com>")
        self.assertEqual(skill["source_repo"], "NVIDIA/SkillEvaluator")
        self.assertEqual(skill["source_revision"], "7ae25d2522c9c3b151111fedaa67b814cc3dc5c5")

    def test_standalone_file_inventory_and_modes(self):
        files = self.imported["files"]
        self.assertEqual(len(files), 16)

        for record in files:
            file_path = ROOT / record["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), record["sha256"], f"Checksum mismatch: {file_path}")

            st = os.stat(file_path)
            is_exec = bool(st.st_mode & 0o111) and not file_path.suffix == ".md"
            self.assertEqual(is_exec, record["executable"], f"Executable bit mismatch on {file_path}")

        skill_dir = ROOT / "skills/skillevaluator"
        self.assertTrue((skill_dir / "LICENSE").is_file())
        self.assertTrue((skill_dir / "NOTICE.md").is_file())
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertTrue((skill_dir / "evals/config.yml").is_file())
        self.assertTrue((skill_dir / "evals/evals.json").is_file())
        self.assertTrue((skill_dir / "references/commands-tier1.md").is_file())
        self.assertTrue((skill_dir / "references/commands-tier2-tier3.md").is_file())
        self.assertTrue((skill_dir / "references/commands-validate.md").is_file())
        self.assertTrue((skill_dir / "references/custom-graders.md").is_file())
        self.assertTrue((skill_dir / "references/providers.md").is_file())
        self.assertTrue((skill_dir / "references/reports-and-ci.md").is_file())
        self.assertTrue((skill_dir / "references/tier3-datasets.md").is_file())
        self.assertTrue((skill_dir / "references/tier3-running.md").is_file())
        self.assertTrue((skill_dir / "references/troubleshooting.md").is_file())

    def test_cli_operations_isolated_workspace(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            claude_dest = tmppath / ".claude/skills"
            claude_dest.mkdir(parents=True, exist_ok=True)

            # 1. Search CLI
            res_search = cli("search", "skillevaluator")
            self.assertEqual(res_search.returncode, 0)
            self.assertIn("skillevaluator", res_search.stdout)

            # 2. Show CLI
            res_show = cli("show", "skillevaluator")
            self.assertEqual(res_show.returncode, 0)
            self.assertIn("SkillEvaluator", res_show.stdout)

            # 3. Install via copy mode
            res_install = cli(
                "install",
                "skillevaluator",
                "--target",
                "claude",
                "--mode",
                "copy",
                "--dest",
                str(claude_dest),
            )
            self.assertEqual(res_install.returncode, 0)
            installed_dir = claude_dest / "skillevaluator"
            self.assertTrue(installed_dir.is_dir())
            self.assertTrue((installed_dir / "SKILL.md").is_file())
            self.assertTrue((installed_dir / "LICENSE").is_file())
            self.assertTrue((installed_dir / "NOTICE.md").is_file())
            self.assertTrue((installed_dir / "references/commands-tier1.md").is_file())
            self.assertTrue((claude_dest / ".vas-manifest.json").is_file())

            # 4. Status CLI
            res_status = cli("status", "--target", "claude", "--dest", str(claude_dest))
            self.assertEqual(res_status.returncode, 0)
            self.assertIn("skillevaluator", res_status.stdout)

            # 5. Uninstall CLI
            res_uninstall = cli(
                "uninstall",
                "skillevaluator",
                "--target",
                "claude",
                "--dest",
                str(claude_dest),
            )
            self.assertEqual(res_uninstall.returncode, 0)
            self.assertFalse(installed_dir.exists())

    def test_pages_manifest_generation(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("skillevaluator", manifests)
        entry = manifests["skillevaluator"]

        self.assertEqual(entry["schema_version"], 1)
        self.assertEqual(entry["skill_id"], "skillevaluator")
        self.assertEqual(entry["target_name"], "skillevaluator")
        self.assertEqual(entry["source_path"], "skills/skillevaluator")
        self.assertEqual(entry["provenance"]["license"], "Apache-2.0")
        self.assertEqual(entry["provenance"]["author"], "Christopher Kevin <christopherk@nvidia.com>")
        self.assertEqual(entry["provenance"]["source_repo"], "NVIDIA/SkillEvaluator")

        manifest_file_names = {f["path"] for f in entry["files"]}
        self.assertIn("SKILL.md", manifest_file_names)
        self.assertIn("LICENSE", manifest_file_names)
        self.assertIn("NOTICE.md", manifest_file_names)
        self.assertIn("references/commands-tier1.md", manifest_file_names)
        self.assertIn("references/commands-tier2-tier3.md", manifest_file_names)
        self.assertIn("references/custom-graders.md", manifest_file_names)
        self.assertIn("evals/config.yml", manifest_file_names)
        self.assertIn("evals/evals.json", manifest_file_names)
        self.assertEqual(len(entry["files"]), 16)


if __name__ == "__main__":
    unittest.main()
