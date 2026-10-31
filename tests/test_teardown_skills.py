import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class TeardownSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/teardown-import.json").read_text(encoding="utf-8"))
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 1)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["namespaces"], {})
        self.assertEqual(self.imported["revision"], "e7e668cd44f48ba79a3c575e9f55c7e194d26eef")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3185)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("No collision found", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("teardown", self.credits["sections"])
        self.assertIn("elvarofficial/teardown", self.credits["sections"]["teardown"][0])
        self.assertIn("e7e668cd44f48ba79a3c575e9f55c7e194d26eef", self.credits["sections"]["teardown"][0])
        self.assertIn("MIT", self.credits["sections"]["teardown"][0])

        # Check in skills_index.json
        self.assertIn("teardown", self.skills_by_id)
        skill = self.skills_by_id["teardown"]
        self.assertEqual(skill["canonical_id"], "teardown")
        self.assertEqual(skill["category"], "media")
        self.assertEqual(skill["risk"], "safe")
        self.assertEqual(skill["author"], "Elvar")
        self.assertEqual(skill["license"], "MIT")
        self.assertEqual(skill["source_repo"], "elvarofficial/teardown")
        self.assertEqual(skill["source_revision"], "e7e668cd44f48ba79a3c575e9f55c7e194d26eef")
        self.assertEqual(skill["path"], "skills/teardown")

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        self.assertIn("teardown", cat_by_id)
        cat_entry = cat_by_id["teardown"]
        self.assertEqual(cat_entry["canonical_id"], "teardown")
        self.assertEqual(cat_entry["category"], "media")
        self.assertEqual(cat_entry["license"], "MIT")
        self.assertEqual(cat_entry["author"], "Elvar")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 73)

        skill_dir = ROOT / "skills/teardown"
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertTrue((skill_dir / "LICENSE").is_file())
        self.assertTrue((skill_dir / "README.md").is_file())
        self.assertTrue((skill_dir / "package.json").is_file())
        self.assertTrue((skill_dir / "run_sfx.py").is_file())
        self.assertTrue((skill_dir / "paths.mjs").is_file())
        self.assertTrue((skill_dir / "sheet.mjs").is_file())
        self.assertTrue((skill_dir / "wave.mjs").is_file())

        skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_md_text)
        self.assertIn("elvarofficial/teardown", skill_md_text)
        self.assertIn("MIT License", skill_md_text)
        self.assertIn("Elvar", skill_md_text)

        # Verify key directory structures exist
        self.assertTrue((skill_dir / "docs").is_dir())
        self.assertTrue((skill_dir / "sfx").is_dir())
        self.assertTrue((skill_dir / "sfx/samples").is_dir())
        self.assertTrue((skill_dir / "sims").is_dir())

        # Check non-executable and non-symlink
        sample_paths = [
            "skills/teardown/SKILL.md",
            "skills/teardown/LICENSE",
            "skills/teardown/README.md",
            "skills/teardown/package.json",
            "skills/teardown/run_sfx.py",
            "skills/teardown/paths.mjs",
            "skills/teardown/sims/v8-live/main.js",
            "skills/teardown/sfx/samples/fs-329533-room-tone-in-an-apartment-livi.ogg",
        ]
        for sp in sample_paths:
            p = ROOT / sp
            self.assertTrue(p.is_file(), f"Missing file: {p}")
            self.assertFalse(p.is_symlink())
            self.assertFalse(p.stat().st_mode & 0o111)

    def test_cli_standalone_installation_and_receipt_and_uninstallation(self):
        # Test link mode for cursor and copy mode for claude
        with tempfile.TemporaryDirectory(prefix="vas-teardown-link-") as temp:
            project = Path(temp)
            result = cli("install", "teardown", "--target", "cursor", "--mode", "link", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "teardown"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "run_sfx.py").is_file())
            self.assertTrue((installed / "sims/v8-live/main.js").is_file())

            # Check receipt
            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("teardown", ledger)
            self.assertEqual(ledger["teardown"]["target_name"], "teardown")

            # Status
            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "teardown", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        with tempfile.TemporaryDirectory(prefix="vas-teardown-copy-") as temp:
            project = Path(temp)
            result = cli("install", "teardown", "--target", "claude", "--mode", "copy", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "teardown"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "run_sfx.py").is_file())
            self.assertTrue((installed / "sheet.mjs").is_file())
            self.assertTrue((installed / "sims/v8-live/main.js").is_file())

            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("teardown", ledger)

            # Uninstall
            uninst_res = cli("uninstall", "teardown", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("teardown", manifests)
        m = manifests["teardown"]
        self.assertEqual(m["skill_id"], "teardown")
        self.assertEqual(m["target_name"], "teardown")
        self.assertEqual(m["provenance"]["category"], "media")
        self.assertEqual(m["provenance"]["license"], "MIT")
        self.assertEqual(m["provenance"]["author"], "Elvar")
        self.assertEqual(m["provenance"]["source_repo"], "elvarofficial/teardown")
        self.assertEqual(len(m["files"]), 73)

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("README.md", file_paths)
        self.assertIn("package.json", file_paths)
        self.assertIn("run_sfx.py", file_paths)
        self.assertIn("sheet.mjs", file_paths)
        self.assertIn("sims/v8-live/main.js", file_paths)
        self.assertIn("sfx/samples/fs-329533-room-tone-in-an-apartment-livi.ogg", file_paths)


if __name__ == "__main__":
    unittest.main()
