#!/usr/bin/env python3
"""Tests for research-explainer and companion Manim skills import, packaging, and CLI workflows."""

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


class TestResearchExplainerSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.import_manifest_path = ROOT / "data/research-explainer-import.json"
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
        self.assertEqual(self.imported["source_repo"], "sepi2p/research-explainer-skill")
        self.assertEqual(self.imported["revision"], "374ecd10fdf60bd08269ff7f51464f754a504ce7")
        self.assertEqual(self.imported["skill_count"], 4)

        # Verify source-credits.json
        self.assertIn("researchexplainer", self.credits["sections"])
        self.assertIn("sepi2p/research-explainer-skill", self.credits["sections"]["researchexplainer"][0])
        self.assertIn("374ecd10fdf60bd08269ff7f51464f754a504ce7", self.credits["sections"]["researchexplainer"][0])

        # Verify category taxonomy remains exactly 119 and catalog has 3,889 skills
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4078)

        expected_skills = {
            "research-explainer": {
                "category": "media",
                "risk": "safe",
                "license": "MIT",
                "author": "sepi2p",
            },
            "manim-composer": {
                "category": "media",
                "risk": "safe",
                "license": "MIT",
                "author": "Adithya S Kolavi (adithya-s-k)",
            },
            "manimce-best-practices": {
                "category": "media",
                "risk": "safe",
                "license": "MIT",
                "author": "Adithya S Kolavi (adithya-s-k)",
            },
            "manimgl-best-practices": {
                "category": "media",
                "risk": "safe",
                "license": "CC-BY-NC-SA-4.0",
                "author": "Adithya S Kolavi / Grant Sanderson (3Blue1Brown)",
            },
        }

        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}

        for sid, exp in expected_skills.items():
            self.assertIn(sid, self.skills_by_id)
            skill = self.skills_by_id[sid]
            self.assertEqual(skill["canonical_id"], sid)
            self.assertEqual(skill["category"], exp["category"])
            self.assertEqual(skill["risk"], exp["risk"])
            self.assertEqual(skill["license"], exp["license"])
            self.assertEqual(skill["author"], exp["author"])
            self.assertEqual(skill["source_repo"], "sepi2p/research-explainer-skill")
            self.assertEqual(skill["source_revision"], "374ecd10fdf60bd08269ff7f51464f754a504ce7")

            self.assertIn(sid, cat_by_id)
            cat_entry = cat_by_id[sid]
            self.assertEqual(cat_entry["canonical_id"], sid)
            self.assertEqual(cat_entry["category"], exp["category"])
            self.assertEqual(cat_entry["license"], exp["license"])

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 432)

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        # Check key files in all 4 skills
        for sid in ("manim-composer", "manimce-best-practices", "manimgl-best-practices", "research-explainer"):
            skill_dir = ROOT / f"skills/{sid}"
            self.assertTrue((skill_dir / "SKILL.md").exists())
            self.assertTrue((skill_dir / "LICENSE").exists())
            self.assertTrue((skill_dir / "NOTICE.md").exists())
            skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## VAS installation notes", skill_text)
            self.assertIn(f"Canonical ID: `{sid}`", skill_text)
            self.assertIn("sepi2p/research-explainer-skill", skill_text)

        # Check executable scripts in research-explainer
        re_dir = ROOT / "skills/research-explainer"
        for rel_exec in [
            "scripts/rx.py",
            "templates/short/setup.sh",
            "templates/short/work/mix.sh",
            "templates/short/work/stills.sh",
            "templates/diorama/video/render_par.sh",
            "templates/diorama/video/stills.sh",
            "templates/diorama/video/stills_scene.sh",
            "templates/diorama/work/render_part.sh",
            "templates/watercolor-story/setup.sh",
            "templates/watercolor-story/work/mix.sh",
            "templates/watercolor-story/work/empty_room.sh",
            "templates/watercolor-story/work/stills.sh",
        ]:
            script_path = re_dir / rel_exec
            self.assertTrue(script_path.is_file(), f"Missing script: {script_path}")
            self.assertTrue(os.access(script_path, os.X_OK), f"Script not executable: {script_path}")

        # Check bundled examples in research-explainer
        self.assertTrue((re_dir / "examples/averaging-noise/scenes.md").is_file())
        self.assertTrue((re_dir / "examples/how-a-network-sees/scenes.md").is_file())

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with research-explainer
        with tempfile.TemporaryDirectory(prefix="vas-re-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "research-explainer",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "research-explainer"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "scripts/rx.py").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("research-explainer", ledger)
            self.assertEqual(ledger["research-explainer"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "research-explainer", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with manim-composer
        with tempfile.TemporaryDirectory(prefix="vas-mc-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "manim-composer",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "manim-composer"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "references/narrative-patterns.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("manim-composer", ledger)
            self.assertEqual(ledger["manim-composer"]["mode"], "copy")
            self.assertEqual(ledger["manim-composer"]["target_name"], "manim-composer")

            uninst_res = cli("uninstall", "manim-composer", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 3. Test copy mode with manimce-best-practices
        with tempfile.TemporaryDirectory(prefix="vas-mce-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "manimce-best-practices",
                "--target", "workspace",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["workspace"][0]
            installed = dest_dir / "manimce-best-practices"
            self.assertTrue(installed.exists())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "rules/scenes.md").is_file())

            uninst_res = cli("uninstall", "manimce-best-practices", "--target", "workspace", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for sid in ("research-explainer", "manim-composer", "manimce-best-practices", "manimgl-best-practices"):
            self.assertIn(sid, manifests)
            m = manifests[sid]
            self.assertEqual(m["skill_id"], sid)
            self.assertEqual(m["target_name"], sid)
            self.assertEqual(m["provenance"]["source_repo"], "sepi2p/research-explainer-skill")

            file_paths = {f["path"] for f in m["files"]}
            self.assertIn("SKILL.md", file_paths)
            self.assertIn("LICENSE", file_paths)
            self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
