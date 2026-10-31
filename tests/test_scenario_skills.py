import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class ScenarioSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/scenario-import.json").read_text(encoding="utf-8"))
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 167)
        self.assertEqual(len(self.imported["skipped"]), 7)
        self.assertEqual(self.imported["revision"], "7f4b801c7248d51b093ec365aceb114bd06139e6")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3186)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("No collision found", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("scenario", self.credits["sections"])
        self.assertIn("scenario-labs/skills", self.credits["sections"]["scenario"][0])
        self.assertIn("7f4b801c7248d51b093ec365aceb114bd06139e6", self.credits["sections"]["scenario"][0])
        self.assertIn("MIT", self.credits["sections"]["scenario"][0])

        # Check all 167 skills in skills_index.json
        scenario_skills = [s for s in self.index if s.get("source_repo") == "scenario-labs/skills"]
        self.assertEqual(len(scenario_skills), 167)

        categories = {}
        for skill in scenario_skills:
            self.assertEqual(skill["canonical_id"], skill["id"])
            self.assertEqual(skill["author"], "Scenario Inc.")
            self.assertEqual(skill["license"], "MIT")
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["source_revision"], "7f4b801c7248d51b093ec365aceb114bd06139e6")
            self.assertTrue(skill["path"].startswith("skills/scenario"))
            cat = skill["category"]
            self.assertIn(cat, ["media", "game-development"])
            categories[cat] = categories.get(cat, 0) + 1

        self.assertEqual(categories["game-development"], 89)
        self.assertEqual(categories["media"], 78)

        # Check in catalog.json
        cat_skills = [s for s in self.catalog["skills"] if s.get("source_repo") == "scenario-labs/skills"]
        self.assertEqual(len(cat_skills), 167)

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 1717)

        # Verify executable scripts count
        exec_files = [r for r in records if r["executable"]]
        self.assertEqual(len(exec_files), 22)
        for ef in exec_files:
            p = ROOT / ef["path"]
            self.assertTrue(p.is_file())
            st = p.stat()
            self.assertTrue(bool(st.st_mode & stat.S_IXUSR), f"Not executable: {p}")

        # Check expert router READMEs
        expert_skills = [
            "scenario-blender-expert",
            "scenario-maya-expert",
            "scenario-zbrush-expert",
            "scenario-godot-expert",
            "scenario-roblox-expert",
            "scenario-unity-expert",
            "scenario-unreal-expert",
        ]
        for exp in expert_skills:
            exp_dir = ROOT / "skills" / exp
            self.assertTrue((exp_dir / "SKILL.md").is_file())
            self.assertTrue((exp_dir / "LICENSE").is_file())
            self.assertTrue((exp_dir / "README.md").is_file())

        # Sample check of SKILL.md notes
        sample_skill_md = (ROOT / "skills/scenario-3d/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", sample_skill_md)
        self.assertIn("scenario-labs/skills", sample_skill_md)
        self.assertIn("MIT License", sample_skill_md)
        self.assertIn("Scenario Inc.", sample_skill_md)

    def test_cli_standalone_installation_and_receipt_and_uninstallation(self):
        # Test link mode for cursor with scenario-blender-expert
        with tempfile.TemporaryDirectory(prefix="vas-scenario-link-") as temp:
            project = Path(temp)
            result = cli("install", "scenario-blender-expert", "--target", "cursor", "--mode", "link", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "scenario-blender-expert"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "README.md").is_file())

            # Check receipt
            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("scenario-blender-expert", ledger)
            self.assertEqual(ledger["scenario-blender-expert"]["target_name"], "scenario-blender-expert")

            # Status
            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "scenario-blender-expert", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # Test copy mode for claude with scenario-godot-2d
        with tempfile.TemporaryDirectory(prefix="vas-scenario-copy-") as temp:
            project = Path(temp)
            result = cli("install", "scenario-godot-2d", "--target", "claude", "--mode", "copy", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "scenario-godot-2d"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())

            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("scenario-godot-2d", ledger)

            # Uninstall
            uninst_res = cli("uninstall", "scenario-godot-2d", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("scenario-blender-expert", manifests)
        m = manifests["scenario-blender-expert"]
        self.assertEqual(m["skill_id"], "scenario-blender-expert")
        self.assertEqual(m["target_name"], "scenario-blender-expert")
        self.assertEqual(m["provenance"]["category"], "game-development")
        self.assertEqual(m["provenance"]["license"], "MIT")
        self.assertEqual(m["provenance"]["author"], "Scenario Inc.")
        self.assertEqual(m["provenance"]["source_repo"], "scenario-labs/skills")

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("README.md", file_paths)


if __name__ == "__main__":
    unittest.main()
