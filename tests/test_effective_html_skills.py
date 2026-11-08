import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class EffectiveHtmlSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/effective-html-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 8)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["revision"], "5ce160a3e76dc1c0f9301f8a1903704ec607636a")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3876)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("zero existing duplicates", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("effectivehtml", self.credits["sections"])
        self.assertIn("plannotator/effective-html", self.credits["sections"]["effectivehtml"][0])
        self.assertIn("5ce160a3e76dc1c0f9301f8a1903704ec607636a", self.credits["sections"]["effectivehtml"][0])
        self.assertIn("MIT", self.credits["sections"]["effectivehtml"][0])

        # Verify category taxonomy remains exactly 119
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4074)

        expected_skills = [
            "big-pics-little-words",
            "design-artifact",
            "html",
            "html-diagram",
            "html-plan",
            "html-prototype",
            "html-wireframe",
            "one-pager",
        ]

        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}

        for sid in expected_skills:
            with self.subTest(skill_id=sid):
                self.assertIn(sid, self.skills_by_id)
                skill = self.skills_by_id[sid]
                self.assertEqual(skill["canonical_id"], sid)
                self.assertEqual(skill["category"], "design")
                self.assertEqual(skill["risk"], "safe")
                self.assertEqual(skill["author"], "Plannotator")
                self.assertEqual(skill["license"], "MIT")
                self.assertEqual(skill["source_repo"], "plannotator/effective-html")
                self.assertEqual(skill["source_revision"], "5ce160a3e76dc1c0f9301f8a1903704ec607636a")
                self.assertIn("design", skill["tags"])
                self.assertIn("effective-html", skill["tags"])

                # Check in catalog.json
                self.assertIn(sid, cat_by_id)
                cat_entry = cat_by_id[sid]
                self.assertEqual(cat_entry["canonical_id"], sid)
                self.assertEqual(cat_entry["category"], "design")
                self.assertEqual(cat_entry["license"], "MIT")
                self.assertEqual(cat_entry["author"], "Plannotator")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 37)

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        expected_skills = [
            "big-pics-little-words",
            "design-artifact",
            "html",
            "html-diagram",
            "html-plan",
            "html-prototype",
            "html-wireframe",
            "one-pager",
        ]

        for sid in expected_skills:
            skill_dir = ROOT / f"skills/{sid}"
            self.assertTrue((skill_dir / "SKILL.md").exists())
            self.assertTrue((skill_dir / "LICENSE").exists())
            self.assertTrue((skill_dir / "NOTICE.md").exists())
            self.assertTrue((skill_dir / "agents/openai.yaml").exists())

            skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## VAS installation notes", skill_text)
            self.assertIn(f"Canonical ID: `{sid}`", skill_text)
            self.assertIn("plannotator/effective-html", skill_text)

        # Check references in html skill
        html_dir = ROOT / "skills/html"
        for ref in [
            "charts-and-data.md",
            "creative-direction.md",
            "diagrams.md",
            "documents-and-presentations.md",
            "interfaces.md",
        ]:
            self.assertTrue((html_dir / f"references/{ref}").exists())

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with html-wireframe
        with tempfile.TemporaryDirectory(prefix="vas-html-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "html-wireframe",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "html-wireframe"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "agents/openai.yaml").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("html-wireframe", ledger)
            self.assertEqual(ledger["html-wireframe"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "html-wireframe", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with html (including references)
        with tempfile.TemporaryDirectory(prefix="vas-html-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "html",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "html"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "references/creative-direction.md").is_file())
            self.assertTrue((installed / "references/interfaces.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("html", ledger)
            self.assertEqual(ledger["html"]["mode"], "copy")
            self.assertEqual(ledger["html"]["target_name"], "html")
            self.assertEqual(ledger["html"]["category"], "design")

            uninst_res = cli("uninstall", "html", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for sid in [
            "big-pics-little-words",
            "design-artifact",
            "html",
            "html-diagram",
            "html-plan",
            "html-prototype",
            "html-wireframe",
            "one-pager",
        ]:
            with self.subTest(skill_id=sid):
                self.assertIn(sid, manifests)
                m = manifests[sid]
                self.assertEqual(m["skill_id"], sid)
                self.assertEqual(m["target_name"], sid)
                self.assertEqual(m["provenance"]["author"], "Plannotator")
                self.assertEqual(m["provenance"]["source_repo"], "plannotator/effective-html")

                file_paths = {f["path"] for f in m["files"]}
                self.assertIn("SKILL.md", file_paths)
                self.assertIn("LICENSE", file_paths)
                self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
