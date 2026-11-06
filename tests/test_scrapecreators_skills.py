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


class ScrapeCreatorsSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/scrapecreators-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 13)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["revision"], "64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3859)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("zero content duplicates", self.imported["duplicate_check"]["collision_rationale"])
        self.assertEqual(
            self.imported["namespaces"],
            {"audience-research": "scrapecreators-audience-research"}
        )

        # Check in source-credits.json
        self.assertIn("scrapecreators", self.credits["sections"])
        self.assertIn("ScrapeCreators/social-media-research-skills", self.credits["sections"]["scrapecreators"][0])
        self.assertIn("64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2", self.credits["sections"]["scrapecreators"][0])
        self.assertIn("MIT", self.credits["sections"]["scrapecreators"][0])

        # Verify category taxonomy remains exactly 119
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 3889)

        expected_skills = [
            ("ad-library-teardown", "marketing"),
            ("scrapecreators-audience-research", "marketing"),
            ("comment-mining", "research"),
            ("competitor-social-research", "research"),
            ("content-repurposing", "content"),
            ("creator-profile-teardown", "marketing"),
            ("influencer-prospecting", "marketing"),
            ("outlier-post-finder", "marketing"),
            ("product-demand-research", "research"),
            ("scrapecreators-api", "api-integration"),
            ("social-listening-brief", "marketing"),
            ("transcript-intelligence", "media-processing"),
            ("trend-discovery", "research"),
        ]

        for sid, expected_cat in expected_skills:
            self.assertIn(sid, self.skills_by_id)
            skill = self.skills_by_id[sid]
            self.assertEqual(skill["canonical_id"], sid)
            self.assertEqual(skill["category"], expected_cat)
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["author"], "ScrapeCreators")
            self.assertEqual(skill["license"], "MIT")
            self.assertEqual(skill["source_repo"], "ScrapeCreators/social-media-research-skills")
            self.assertEqual(skill["source_revision"], "64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2")
            self.assertIn("social-media", skill["tags"])
            self.assertIn("scrapecreators", skill["tags"])

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        for sid, expected_cat in expected_skills:
            self.assertIn(sid, cat_by_id)
            cat_entry = cat_by_id[sid]
            self.assertEqual(cat_entry["canonical_id"], sid)
            self.assertEqual(cat_entry["category"], expected_cat)
            self.assertEqual(cat_entry["license"], "MIT")
            self.assertEqual(cat_entry["author"], "ScrapeCreators")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 39)  # 13 skills * 3 files (SKILL.md, LICENSE, NOTICE.md)

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            # Verify permissions (non-executable markdown/license files)
            st_mode = file_path.stat().st_mode
            self.assertEqual(st_mode & 0o111, 0, f"File should not be executable: {file_path}")

            # Verify sha256 checksum
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        # Check sample directories
        for sid in ["ad-library-teardown", "scrapecreators-audience-research", "trend-discovery"]:
            s_dir = ROOT / "skills" / sid
            self.assertTrue(s_dir.is_dir())
            self.assertTrue((s_dir / "SKILL.md").exists())
            self.assertTrue((s_dir / "LICENSE").exists())
            self.assertTrue((s_dir / "NOTICE.md").exists())

            skill_text = (s_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## VAS installation notes", skill_text)
            self.assertIn(f"Canonical ID: `{sid}`", skill_text)
            self.assertIn("ScrapeCreators/social-media-research-skills", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with ad-library-teardown
        with tempfile.TemporaryDirectory(prefix="vas-sc-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "ad-library-teardown",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "ad-library-teardown"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("ad-library-teardown", ledger)
            self.assertEqual(ledger["ad-library-teardown"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "ad-library-teardown", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with namespaced scrapecreators-audience-research
        with tempfile.TemporaryDirectory(prefix="vas-sc-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "scrapecreators-audience-research",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "scrapecreators-audience-research"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("scrapecreators-audience-research", ledger)
            self.assertEqual(ledger["scrapecreators-audience-research"]["mode"], "copy")
            self.assertEqual(ledger["scrapecreators-audience-research"]["target_name"], "scrapecreators-audience-research")
            self.assertEqual(ledger["scrapecreators-audience-research"]["category"], "marketing")

            uninst_res = cli("uninstall", "scrapecreators-audience-research", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for sid in ["ad-library-teardown", "scrapecreators-audience-research", "transcript-intelligence"]:
            self.assertIn(sid, manifests)
            m = manifests[sid]
            self.assertEqual(m["skill_id"], sid)
            self.assertEqual(m["target_name"], sid)
            self.assertEqual(m["provenance"]["author"], "ScrapeCreators")
            self.assertEqual(m["provenance"]["source_repo"], "ScrapeCreators/social-media-research-skills")

            file_paths = {f["path"] for f in m["files"]}
            self.assertIn("SKILL.md", file_paths)
            self.assertIn("LICENSE", file_paths)
            self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
