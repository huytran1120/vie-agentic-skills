import hashlib
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class StoreScreenshotsSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/store-screenshots-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 1)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["revision"], "c25bf66faa7396818c0f7b267e6add4d441573a8")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3875)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("zero existing duplicates", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("storescreenshots", self.credits["sections"])
        self.assertIn("thearkxd/store-screenshots-skill", self.credits["sections"]["storescreenshots"][0])
        self.assertIn("c25bf66faa7396818c0f7b267e6add4d441573a8", self.credits["sections"]["storescreenshots"][0])
        self.assertIn("MIT", self.credits["sections"]["storescreenshots"][0])

        # Verify category taxonomy remains exactly 119
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4077)

        sid = "store-screenshots"
        self.assertIn(sid, self.skills_by_id)
        skill = self.skills_by_id[sid]
        self.assertEqual(skill["canonical_id"], sid)
        self.assertEqual(skill["category"], "design")
        self.assertEqual(skill["risk"], "low")
        self.assertIn("thearkxd", skill["author"])
        self.assertEqual(skill["license"], "MIT")
        self.assertEqual(skill["source_repo"], "thearkxd/store-screenshots-skill")
        self.assertEqual(skill["source_revision"], "c25bf66faa7396818c0f7b267e6add4d441573a8")
        self.assertIn("design", skill["tags"])
        self.assertIn("screenshots", skill["tags"])

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        self.assertIn(sid, cat_by_id)
        cat_entry = cat_by_id[sid]
        self.assertEqual(cat_entry["canonical_id"], sid)
        self.assertEqual(cat_entry["category"], "design")
        self.assertEqual(cat_entry["license"], "MIT")
        self.assertIn("thearkxd", cat_entry["author"])

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 1699)

        for r in records[:50]:  # Sample first 50 files for full sha256 check
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        # Check key files in store-screenshots
        skill_dir = ROOT / "skills/store-screenshots"
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertTrue((skill_dir / "LICENSE").exists())
        self.assertTrue((skill_dir / "NOTICE.md").exists())
        self.assertTrue((skill_dir / "references/storytelling.md").exists())
        self.assertTrue((skill_dir / "references/copy-rules.md").exists())
        self.assertTrue((skill_dir / "references/design-process.md").exists())
        self.assertTrue((skill_dir / "references/scene-format.md").exists())
        self.assertTrue((skill_dir / "scripts/compose.py").exists())
        self.assertTrue((skill_dir / "scripts/search_library.py").exists())
        self.assertTrue((skill_dir / "scripts/check_set.py").exists())
        self.assertTrue((skill_dir / "assets/library/catalog.json").exists())
        self.assertTrue((skill_dir / "assets/library/classifications.json").exists())
        self.assertTrue((skill_dir / "assets/fonts/FONTS.md").exists())

        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_text)
        self.assertIn("Canonical ID: `store-screenshots`", skill_text)
        self.assertIn("thearkxd/store-screenshots-skill", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with store-screenshots
        with tempfile.TemporaryDirectory(prefix="vas-screenshots-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "store-screenshots",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "store-screenshots"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "scripts/compose.py").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("store-screenshots", ledger)
            self.assertEqual(ledger["store-screenshots"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "store-screenshots", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with store-screenshots
        with tempfile.TemporaryDirectory(prefix="vas-screenshots-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "store-screenshots",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "store-screenshots"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "references/storytelling.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("store-screenshots", ledger)
            self.assertEqual(ledger["store-screenshots"]["mode"], "copy")
            self.assertEqual(ledger["store-screenshots"]["target_name"], "store-screenshots")
            self.assertEqual(ledger["store-screenshots"]["category"], "design")

            uninst_res = cli("uninstall", "store-screenshots", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("store-screenshots", manifests)
        m = manifests["store-screenshots"]
        self.assertEqual(m["skill_id"], "store-screenshots")
        self.assertEqual(m["target_name"], "store-screenshots")
        self.assertIn("thearkxd", m["provenance"]["author"])
        self.assertEqual(m["provenance"]["source_repo"], "thearkxd/store-screenshots-skill")

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("NOTICE.md", file_paths)
        self.assertIn("scripts/compose.py", file_paths)


if __name__ == "__main__":
    unittest.main()
