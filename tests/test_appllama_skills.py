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


class AppllamaSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/appllama-skills-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 2)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["revision"], "dd5caaec3d5d50ad7fc0324da238119c6b7c3707")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3873)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("zero existing duplicates", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("appllama", self.credits["sections"])
        self.assertIn("Appllama/appllama-skills", self.credits["sections"]["appllama"][0])
        self.assertIn("dd5caaec3d5d50ad7fc0324da238119c6b7c3707", self.credits["sections"]["appllama"][0])
        self.assertIn("MIT", self.credits["sections"]["appllama"][0])

        # Verify category taxonomy remains exactly 119
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 3884)

        expected_skills = [
            ("appllama-app-design-skill", "mobile"),
            ("appllama-usage", "mobile"),
        ]

        for sid, expected_cat in expected_skills:
            self.assertIn(sid, self.skills_by_id)
            skill = self.skills_by_id[sid]
            self.assertEqual(skill["canonical_id"], sid)
            self.assertEqual(skill["category"], expected_cat)
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["author"], "Appllama")
            self.assertEqual(skill["license"], "MIT")
            self.assertEqual(skill["source_repo"], "Appllama/appllama-skills")
            self.assertEqual(skill["source_revision"], "dd5caaec3d5d50ad7fc0324da238119c6b7c3707")
            self.assertIn("mobile", skill["tags"])
            self.assertIn("appllama", skill["tags"])

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        for sid, expected_cat in expected_skills:
            self.assertIn(sid, cat_by_id)
            cat_entry = cat_by_id[sid]
            self.assertEqual(cat_entry["canonical_id"], sid)
            self.assertEqual(cat_entry["category"], expected_cat)
            self.assertEqual(cat_entry["license"], "MIT")
            self.assertEqual(cat_entry["author"], "Appllama")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 15)  # 8 for design + 7 for usage

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

        # Check references in appllama-app-design-skill
        design_dir = ROOT / "skills/appllama-app-design-skill"
        self.assertTrue((design_dir / "SKILL.md").exists())
        self.assertTrue((design_dir / "LICENSE").exists())
        self.assertTrue((design_dir / "NOTICE.md").exists())
        self.assertTrue((design_dir / "references/image-assets.md").exists())
        self.assertTrue((design_dir / "references/motion.md").exists())
        self.assertTrue((design_dir / "references/native-controls.md").exists())
        self.assertTrue((design_dir / "references/performance.md").exists())
        self.assertTrue((design_dir / "references/simulator-loop.md").exists())

        design_text = (design_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", design_text)
        self.assertIn("Canonical ID: `appllama-app-design-skill`", design_text)
        self.assertIn("Appllama/appllama-skills", design_text)

        # Check references in appllama-usage
        usage_dir = ROOT / "skills/appllama-usage"
        self.assertTrue((usage_dir / "SKILL.md").exists())
        self.assertTrue((usage_dir / "LICENSE").exists())
        self.assertTrue((usage_dir / "NOTICE.md").exists())
        self.assertTrue((usage_dir / "agents/openai.yaml").exists())
        self.assertTrue((usage_dir / "references/build-from-scratch.md").exists())
        self.assertTrue((usage_dir / "references/improve-a-screen.md").exists())
        self.assertTrue((usage_dir / "references/research-methods.md").exists())

        usage_text = (usage_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", usage_text)
        self.assertIn("Canonical ID: `appllama-usage`", usage_text)
        self.assertIn("Appllama/appllama-skills", usage_text)

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with appllama-app-design-skill
        with tempfile.TemporaryDirectory(prefix="vas-appllama-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "appllama-app-design-skill",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "appllama-app-design-skill"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "references/motion.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("appllama-app-design-skill", ledger)
            self.assertEqual(ledger["appllama-app-design-skill"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "appllama-app-design-skill", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with appllama-usage
        with tempfile.TemporaryDirectory(prefix="vas-appllama-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "appllama-usage",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "appllama-usage"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "agents/openai.yaml").is_file())
            self.assertTrue((installed / "references/build-from-scratch.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("appllama-usage", ledger)
            self.assertEqual(ledger["appllama-usage"]["mode"], "copy")
            self.assertEqual(ledger["appllama-usage"]["target_name"], "appllama-usage")
            self.assertEqual(ledger["appllama-usage"]["category"], "mobile")

            uninst_res = cli("uninstall", "appllama-usage", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for sid in ["appllama-app-design-skill", "appllama-usage"]:
            self.assertIn(sid, manifests)
            m = manifests[sid]
            self.assertEqual(m["skill_id"], sid)
            self.assertEqual(m["target_name"], sid)
            self.assertEqual(m["provenance"]["author"], "Appllama")
            self.assertEqual(m["provenance"]["source_repo"], "Appllama/appllama-skills")

            file_paths = {f["path"] for f in m["files"]}
            self.assertIn("SKILL.md", file_paths)
            self.assertIn("LICENSE", file_paths)
            self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
