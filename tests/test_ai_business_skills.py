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


class AIBusinessSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/ai-business-skills-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 147)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(len(self.imported["namespaces"]), 146)
        # namespaces check
        # self.assertIn("product-marketing-context", self.imported["namespaces"])
        self.assertEqual(self.imported["namespaces"]["aibiz-product-marketing-context"], "aibiz-product-marketing-context")
        self.assertEqual(self.imported["revision"], "fe33cb1a47e6140d3693651acbb743e2b1b5b26f")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3429)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("zero content collisions", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("aibusiness", self.credits["sections"])
        self.assertIn("minhnv0807/ai-business-skills", self.credits["sections"]["aibusiness"][0])
        self.assertIn("fe33cb1a47e6140d3693651acbb743e2b1b5b26f", self.credits["sections"]["aibusiness"][0])
        self.assertIn("MIT", self.credits["sections"]["aibusiness"][0])

        # Check sample skills in skills_index.json
        sample_ids = [
            "ke-hoach-mkt", "script-video", "copy-quang-cao", "audit-ads-performance",
            "copy-hai-lop", "kich-ban-sale-chatbot", "aibiz-product-marketing-context",
            "marketing-plan-global", "ad-copy-global", "ads-audit-global",
            "dropshipping-mastery-global", "personal-brand-context", "ai-avatar-production"
        ]
        for sid in sample_ids:
            self.assertIn(sid, self.skills_by_id)
            skill = self.skills_by_id[sid]
            self.assertEqual(skill["canonical_id"], sid)
            self.assertEqual(skill["category"], "marketing")
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["author"], "AI Business Skills")
            self.assertIn("MIT", skill["license"])
            self.assertEqual(skill["source_repo"], "minhnv0807/ai-business-skills")
            self.assertEqual(skill["source_revision"], "fe33cb1a47e6140d3693651acbb743e2b1b5b26f")

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        for sid in sample_ids:
            self.assertIn(sid, cat_by_id)
            cat_entry = cat_by_id[sid]
            self.assertEqual(cat_entry["canonical_id"], sid)
            self.assertEqual(cat_entry["category"], "marketing")
            self.assertEqual(cat_entry["license"], "MIT")
            self.assertEqual(cat_entry["author"], "AI Business Skills")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 746)

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")

            # Verify permissions
            is_exec = r["executable"]
            st_mode = file_path.stat().st_mode
            if is_exec:
                self.assertNotEqual(st_mode & 0o111, 0, f"Script should be executable: {file_path}")
            else:
                self.assertEqual(st_mode & 0o111, 0, f"File should not be executable: {file_path}")

            # Verify sha256 checksum
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        # Check key sample skill directories
        for sid in ["ke-hoach-mkt", "kich-ban-sale-chatbot", "aibiz-product-marketing-context"]:
            s_dir = ROOT / "skills" / sid
            self.assertTrue(s_dir.is_dir())
            self.assertTrue((s_dir / "SKILL.md").exists())
            self.assertTrue((s_dir / "LICENSE").exists())
            self.assertTrue((s_dir / "NOTICE.md").exists())

            skill_text = (s_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Hướng dẫn sử dụng trong VAS / Usage in VAS", skill_text)
            self.assertIn(f"./vas install {sid}", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with aibiz-product-marketing-context
        with tempfile.TemporaryDirectory(prefix="vas-aibiz-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "aibiz-product-marketing-context",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "aibiz-product-marketing-context"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("aibiz-product-marketing-context", ledger)
            self.assertEqual(ledger["aibiz-product-marketing-context"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "aibiz-product-marketing-context", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with 77-kich-ban-sale-chatbot
        with tempfile.TemporaryDirectory(prefix="vas-aibiz-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "kich-ban-sale-chatbot",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "kich-ban-sale-chatbot"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "references/phap-ly-marketing-vn.md").is_file())
            self.assertTrue((installed / "references/quy-tac-van-hanh.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("kich-ban-sale-chatbot", ledger)
            self.assertEqual(ledger["kich-ban-sale-chatbot"]["mode"], "copy")
            self.assertEqual(ledger["kich-ban-sale-chatbot"]["target_name"], "kich-ban-sale-chatbot")
            self.assertEqual(ledger["kich-ban-sale-chatbot"]["category"], "marketing")

            uninst_res = cli("uninstall", "kich-ban-sale-chatbot", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for sid in ["ke-hoach-mkt", "kich-ban-sale-chatbot", "aibiz-product-marketing-context"]:
            self.assertIn(sid, manifests)
            m = manifests[sid]
            self.assertEqual(m["skill_id"], sid)
            self.assertEqual(m["target_name"], sid)
            self.assertEqual(m["provenance"]["category"], "marketing")
            self.assertEqual(m["provenance"]["author"], "AI Business Skills")
            self.assertEqual(m["provenance"]["source_repo"], "minhnv0807/ai-business-skills")

            file_paths = {f["path"] for f in m["files"]}
            self.assertIn("SKILL.md", file_paths)
            self.assertIn("LICENSE", file_paths)
            self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
