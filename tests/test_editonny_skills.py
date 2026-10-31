import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class EditonnySkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/editonny-import.json").read_text(encoding="utf-8"))
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 1)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["namespaces"], {})
        self.assertEqual(self.imported["revision"], "49714f2fba6eafb76b903376e1fe9f50b685506a")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3184)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("No collision found", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("editonny", self.credits["sections"])
        self.assertIn("soumatheusgomes/editonny", self.credits["sections"]["editonny"][0])
        self.assertIn("49714f2fba6eafb76b903376e1fe9f50b685506a", self.credits["sections"]["editonny"][0])
        self.assertIn("MIT", self.credits["sections"]["editonny"][0])

        # Check in skills_index.json
        self.assertIn("editonny", self.skills_by_id)
        skill = self.skills_by_id["editonny"]
        self.assertEqual(skill["canonical_id"], "editonny")
        self.assertEqual(skill["category"], "media")
        self.assertEqual(skill["risk"], "safe")
        self.assertEqual(skill["author"], "Matheus Gomes")
        self.assertEqual(skill["license"], "MIT")
        self.assertEqual(skill["source_repo"], "soumatheusgomes/editonny")
        self.assertEqual(skill["source_revision"], "49714f2fba6eafb76b903376e1fe9f50b685506a")
        self.assertEqual(skill["path"], "skills/editonny")

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        self.assertIn("editonny", cat_by_id)
        cat_entry = cat_by_id["editonny"]
        self.assertEqual(cat_entry["canonical_id"], "editonny")
        self.assertEqual(cat_entry["category"], "media")
        self.assertEqual(cat_entry["license"], "MIT")
        self.assertEqual(cat_entry["author"], "Matheus Gomes")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 2108)

        skill_dir = ROOT / "skills/editonny"
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertTrue((skill_dir / "LICENSE").is_file())
        self.assertTrue((skill_dir / "LICENSE.md").is_file())
        self.assertTrue((skill_dir / "VERSION").is_file())

        skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_md_text)
        self.assertIn("soumatheusgomes/editonny", skill_md_text)
        self.assertIn("MIT License", skill_md_text)
        self.assertIn("Matheus Gomes", skill_md_text)

        # Verify key directory structures exist
        self.assertTrue((skill_dir / "agents").is_dir())
        self.assertTrue((skill_dir / "scripts").is_dir())
        self.assertTrue((skill_dir / "references").is_dir())
        self.assertTrue((skill_dir / "visuals").is_dir())
        self.assertTrue((skill_dir / "engine").is_dir())

        # Check non-executable and non-symlink
        sample_paths = [
            "skills/editonny/SKILL.md",
            "skills/editonny/LICENSE",
            "skills/editonny/VERSION",
            "skills/editonny/scripts/editonny.py",
            "skills/editonny/engine/helpers/transcribe.py",
        ]
        for sp in sample_paths:
            p = ROOT / sp
            self.assertTrue(p.is_file(), f"Missing file: {p}")
            self.assertFalse(p.is_symlink())
            self.assertFalse(p.stat().st_mode & 0o111)

    def test_cli_standalone_installation_and_receipt_and_uninstallation(self):
        # Test link mode for cursor and copy mode for claude
        with tempfile.TemporaryDirectory(prefix="vas-editonny-link-") as temp:
            project = Path(temp)
            result = cli("install", "editonny", "--target", "cursor", "--mode", "link", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "editonny"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())

            # Check receipt
            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("editonny", ledger)
            self.assertEqual(ledger["editonny"]["target_name"], "editonny")

            # Status
            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "editonny", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        with tempfile.TemporaryDirectory(prefix="vas-editonny-copy-") as temp:
            project = Path(temp)
            result = cli("install", "editonny", "--target", "claude", "--mode", "copy", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "editonny"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "scripts/editonny.py").is_file())
            self.assertTrue((installed / "engine/helpers/transcribe.py").is_file())

            receipt_file = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_file.is_file())
            ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
            self.assertIn("editonny", ledger)

            # Uninstall
            uninst_res = cli("uninstall", "editonny", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("editonny", manifests)
        m = manifests["editonny"]
        self.assertEqual(m["skill_id"], "editonny")
        self.assertEqual(m["target_name"], "editonny")
        self.assertEqual(m["provenance"]["category"], "media")
        self.assertEqual(m["provenance"]["license"], "MIT")
        self.assertEqual(m["provenance"]["author"], "Matheus Gomes")
        self.assertEqual(m["provenance"]["source_repo"], "soumatheusgomes/editonny")
        self.assertEqual(len(m["files"]), 2108)

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("VERSION", file_paths)
        self.assertIn("scripts/editonny.py", file_paths)
        self.assertIn("engine/helpers/transcribe.py", file_paths)


if __name__ == "__main__":
    unittest.main()
