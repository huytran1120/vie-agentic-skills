import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class StackDiagramSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/stack-diagram-import.json").read_text(encoding="utf-8"))
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 1)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["namespaces"], {})
        self.assertEqual(self.imported["revision"], "75dbd3e3c6fe28844322e6064d3a947b870a6c61")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3354)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("No collision found", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("stackdiagram", self.credits["sections"])
        self.assertIn("caru-ini/stack-diagram", self.credits["sections"]["stackdiagram"][0])
        self.assertIn("75dbd3e3c6fe28844322e6064d3a947b870a6c61", self.credits["sections"]["stackdiagram"][0])
        self.assertIn("MIT", self.credits["sections"]["stackdiagram"][0])

        # Check in skills_index.json
        self.assertIn("stack-diagram", self.skills_by_id)
        skill = self.skills_by_id["stack-diagram"]
        self.assertEqual(skill["canonical_id"], "stack-diagram")
        self.assertEqual(skill["category"], "architecture")
        self.assertEqual(skill["risk"], "safe")
        self.assertEqual(skill["author"], "caru-ini")
        self.assertIn("MIT", skill["license"])
        self.assertEqual(skill["source_repo"], "caru-ini/stack-diagram")
        self.assertEqual(skill["source_revision"], "75dbd3e3c6fe28844322e6064d3a947b870a6c61")
        self.assertEqual(skill["path"], "skills/stack-diagram")

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        self.assertIn("stack-diagram", cat_by_id)
        cat_entry = cat_by_id["stack-diagram"]
        self.assertEqual(cat_entry["canonical_id"], "stack-diagram")
        self.assertEqual(cat_entry["category"], "architecture")
        self.assertEqual(cat_entry["license"], "MIT")
        self.assertEqual(cat_entry["author"], "caru-ini")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 20)

        skill_dir = ROOT / "skills/stack-diagram"
        self.assertTrue(skill_dir.is_dir())

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")
            self.assertFalse(r["executable"])
            self.assertEqual(file_path.stat().st_mode & 0o111, 0, f"File should not be executable: {file_path}")

            # Verify sha256 checksum
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        # Check key standalone files exist
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertTrue((skill_dir / "LICENSE").exists())
        self.assertTrue((skill_dir / "NOTICE.md").exists())
        self.assertTrue((skill_dir / "README.md").exists())
        self.assertTrue((skill_dir / "assets/template.html").exists())
        self.assertTrue((skill_dir / "assets/fonts/Geist.woff2").exists())
        self.assertTrue((skill_dir / "assets/fonts/JetBrainsMono.woff2").exists())
        self.assertTrue((skill_dir / "scripts/build.py").exists())
        self.assertTrue((skill_dir / "scripts/fetch_icons.py").exists())
        self.assertTrue((skill_dir / "scripts/render_png.py").exists())

        # Check SKILL.md contains VAS installation notes
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_text)
        self.assertIn("Canonical ID: `stack-diagram`", skill_text)
        self.assertIn("caru-ini/stack-diagram", skill_text)
        self.assertIn("75dbd3e3c6fe28844322e6064d3a947b870a6c61", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        with tempfile.TemporaryDirectory(prefix="vas-stackdiagram-link-") as temp:
            project = Path(temp)
            result = cli("install", "stack-diagram", "--target", "cursor", "--mode", "link", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "stack-diagram"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "assets/template.html").is_file())
            self.assertTrue((installed / "scripts/build.py").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("stack-diagram", ledger)
            self.assertEqual(ledger["stack-diagram"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "stack-diagram", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        with tempfile.TemporaryDirectory(prefix="vas-stackdiagram-copy-") as temp:
            project = Path(temp)
            result = cli("install", "stack-diagram", "--target", "claude", "--mode", "copy", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "stack-diagram"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())
            self.assertTrue((installed / "assets/template.html").is_file())
            self.assertTrue((installed / "scripts/build.py").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("stack-diagram", ledger)
            self.assertEqual(ledger["stack-diagram"]["mode"], "copy")
            self.assertEqual(ledger["stack-diagram"]["target_name"], "stack-diagram")
            self.assertEqual(ledger["stack-diagram"]["category"], "architecture")

            uninst_res = cli("uninstall", "stack-diagram", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("stack-diagram", manifests)
        m = manifests["stack-diagram"]
        self.assertEqual(m["skill_id"], "stack-diagram")
        self.assertEqual(m["target_name"], "stack-diagram")
        self.assertEqual(m["provenance"]["category"], "architecture")
        self.assertEqual(m["provenance"]["author"], "caru-ini")
        self.assertEqual(m["provenance"]["source_repo"], "caru-ini/stack-diagram")
        self.assertEqual(len(m["files"]), 20)

        file_paths = {f["path"] for f in m["files"]}
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("NOTICE.md", file_paths)
        self.assertIn("README.md", file_paths)
        self.assertIn("assets/template.html", file_paths)
        self.assertIn("assets/fonts/Geist.woff2", file_paths)
        self.assertIn("assets/fonts/JetBrainsMono.woff2", file_paths)
        self.assertIn("scripts/build.py", file_paths)
        self.assertIn("scripts/fetch_icons.py", file_paths)
        self.assertIn("scripts/render_png.py", file_paths)


if __name__ == "__main__":
    unittest.main()
