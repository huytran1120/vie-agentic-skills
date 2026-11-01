import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class StageshowSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/stageshow-import.json").read_text(encoding="utf-8"))
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 1)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["namespaces"], {})
        self.assertEqual(self.imported["revision"], "802057409787133703c56001080169e347305572")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3353)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("No collision found", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("stageshow", self.credits["sections"])
        self.assertIn("benjitaylor/skills", self.credits["sections"]["stageshow"][0])
        self.assertIn("802057409787133703c56001080169e347305572", self.credits["sections"]["stageshow"][0])
        self.assertIn("MIT", self.credits["sections"]["stageshow"][0])

        # Check in skills_index.json
        self.assertIn("stageshow", self.skills_by_id)
        skill = self.skills_by_id["stageshow"]
        self.assertEqual(skill["canonical_id"], "stageshow")
        self.assertEqual(skill["category"], "frontend")
        self.assertEqual(skill["risk"], "safe")
        self.assertEqual(skill["author"], "Benji Taylor")
        self.assertEqual(skill["license"], "MIT")
        self.assertEqual(skill["source_repo"], "benjitaylor/skills")
        self.assertEqual(skill["source_revision"], "802057409787133703c56001080169e347305572")
        self.assertEqual(skill["path"], "skills/stageshow")

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        self.assertIn("stageshow", cat_by_id)
        cat_entry = cat_by_id["stageshow"]
        self.assertEqual(cat_entry["canonical_id"], "stageshow")
        self.assertEqual(cat_entry["category"], "frontend")
        self.assertEqual(cat_entry["license"], "MIT")
        self.assertEqual(cat_entry["author"], "Benji Taylor")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 358)

        skill_dir = ROOT / "skills/stageshow"
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertTrue((skill_dir / "LICENSE").is_file())
        self.assertTrue((skill_dir / "NOTICE.md").is_file())
        self.assertTrue((skill_dir / "README.md").is_file())
        self.assertTrue((skill_dir / "package.json").is_file())
        self.assertTrue((skill_dir / "kit/cursor.tsx").is_file())
        self.assertTrue((skill_dir / "scripts/film.mjs").is_file())
        self.assertTrue((skill_dir / "playground/main.tsx").is_file())

        skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_md_text)
        self.assertIn("benjitaylor/skills", skill_md_text)
        self.assertIn("MIT License", skill_md_text)
        self.assertIn("Benji Taylor", skill_md_text)

        # Verify key directory structures exist
        self.assertTrue((skill_dir / "assets").is_dir())
        self.assertTrue((skill_dir / "examples").is_dir())
        self.assertTrue((skill_dir / "kit").is_dir())
        self.assertTrue((skill_dir / "kit/brands").is_dir())
        self.assertTrue((skill_dir / "playground").is_dir())
        self.assertTrue((skill_dir / "references").is_dir())
        self.assertTrue((skill_dir / "scripts").is_dir())
        self.assertTrue((skill_dir / "teaching").is_dir())

        # Check non-executable and non-symlink
        sample_paths = [
            "skills/stageshow/SKILL.md",
            "skills/stageshow/LICENSE",
            "skills/stageshow/NOTICE.md",
            "skills/stageshow/README.md",
            "skills/stageshow/package.json",
            "skills/stageshow/kit/cursor.tsx",
            "skills/stageshow/scripts/film.mjs",
            "skills/stageshow/kit/brands/linear.svg",
        ]
        for sp in sample_paths:
            p = ROOT / sp
            self.assertTrue(p.is_file(), f"Missing file: {p}")
            self.assertFalse(p.is_symlink())
            self.assertFalse(p.stat().st_mode & 0o111)

    def test_cli_standalone_installation_and_receipt_and_uninstallation(self):
        # Test link mode for cursor and copy mode for claude
        with tempfile.TemporaryDirectory(prefix="vas-stageshow-link-") as temp:
            project = Path(temp)
            result = cli("install", "stageshow", "--target", "cursor", "--mode", "link", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "stageshow"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "kit/cursor.tsx").is_file())
            self.assertTrue((installed / "scripts/film.mjs").is_file())

            # Check receipt
            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("stageshow", ledger)
            self.assertEqual(ledger["stageshow"]["target_name"], "stageshow")

            # Status
            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "stageshow", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        with tempfile.TemporaryDirectory(prefix="vas-stageshow-copy-") as temp:
            project = Path(temp)
            result = cli("install", "stageshow", "--target", "claude", "--mode", "copy", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "stageshow"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "kit/cursor.tsx").is_file())
            self.assertTrue((installed / "scripts/film.mjs").is_file())

            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("stageshow", ledger)

            # Uninstall
            uninst_res = cli("uninstall", "stageshow", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("stageshow", manifests)
        m = manifests["stageshow"]
        self.assertEqual(m["skill_id"], "stageshow")
        self.assertEqual(m["target_name"], "stageshow")
        self.assertEqual(m["provenance"]["category"], "frontend")
        self.assertEqual(m["provenance"]["license"], "MIT")
        self.assertEqual(m["provenance"]["author"], "Benji Taylor")
        self.assertEqual(m["provenance"]["source_repo"], "benjitaylor/skills")
        self.assertEqual(len(m["files"]), 358)

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("NOTICE.md", file_paths)
        self.assertIn("README.md", file_paths)
        self.assertIn("package.json", file_paths)
        self.assertIn("kit/cursor.tsx", file_paths)
        self.assertIn("scripts/film.mjs", file_paths)
        self.assertIn("kit/brands/linear.svg", file_paths)


if __name__ == "__main__":
    unittest.main()
