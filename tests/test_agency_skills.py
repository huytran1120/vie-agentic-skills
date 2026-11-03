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


class AgencySkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/agency-agents-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 283)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["revision"], "b37b5bb33b78f2c1d6567d98e25ca818e3259219")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3576)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertIn("zero existing duplicates", self.imported["duplicate_check"]["collision_rationale"])

        # Check in source-credits.json
        self.assertIn("agency", self.credits["sections"])
        self.assertIn("msitarzewski/agency-agents", self.credits["sections"]["agency"][0])
        self.assertIn("b37b5bb33b78f2c1d6567d98e25ca818e3259219", self.credits["sections"]["agency"][0])
        self.assertIn("MIT", self.credits["sections"]["agency"][0])

        # Verify category taxonomy remains exactly 119
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)

        # Check sample skills across different divisions
        sample_skills = [
            ("agency-software-architect", "engineering"),
            ("agency-backend-architect", "engineering"),
            ("agency-frontend-developer", "engineering"),
            ("agency-brand-guardian", "design"),
            ("agency-growth-hacker", "marketing"),
            ("agency-aeo-foundations-architect", "marketing"),
            ("agency-behavioral-nudge-engine", "product"),
            ("agency-experiment-tracker", "project-management"),
            ("agency-ai-generated-code-security-auditor", "security"),
            ("agency-test-automation-engineer", "testing"),
            ("agency-anthropologist", "education"),
            ("agency-bookkeeper-controller", "finance"),
            ("agency-game-designer", "game-development"),
            ("agency-3d-scene-developer", "engineering"),
            ("agency-clinical-evidence-agent", "health"),
            ("agency-research-synthesist", "research"),
            ("agency-account-strategist", "business"),
            ("agency-macos-spatial-metal-engineer", "creative"),
            ("agency-accounts-payable-agent", "agent-persona"),
            ("agency-analytics-reporter", "operations"),
        ]

        for sid, expected_cat in sample_skills:
            self.assertIn(sid, self.skills_by_id)
            skill = self.skills_by_id[sid]
            self.assertEqual(skill["canonical_id"], sid)
            self.assertEqual(skill["category"], expected_cat)
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["author"], "AgentLand Contributors")
            self.assertEqual(skill["license"], "MIT")
            self.assertEqual(skill["source_repo"], "msitarzewski/agency-agents")
            self.assertEqual(skill["source_revision"], "b37b5bb33b78f2c1d6567d98e25ca818e3259219")
            self.assertIn("agency-agents", skill["tags"])
            self.assertIn("the-agency", skill["tags"])

        # Check in catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        for sid, expected_cat in sample_skills:
            self.assertIn(sid, cat_by_id)
            cat_entry = cat_by_id[sid]
            self.assertEqual(cat_entry["canonical_id"], sid)
            self.assertEqual(cat_entry["category"], expected_cat)
            self.assertEqual(cat_entry["license"], "MIT")
            self.assertEqual(cat_entry["author"], "AgentLand Contributors")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 849)  # 283 skills * 3 files (SKILL.md, LICENSE, NOTICE.md)

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
        for sid in ["agency-software-architect", "agency-frontend-developer", "agency-ai-generated-code-security-auditor"]:
            s_dir = ROOT / "skills" / sid
            self.assertTrue(s_dir.is_dir())
            self.assertTrue((s_dir / "SKILL.md").exists())
            self.assertTrue((s_dir / "LICENSE").exists())
            self.assertTrue((s_dir / "NOTICE.md").exists())

            skill_text = (s_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## VAS installation notes", skill_text)
            self.assertIn(f"Canonical ID: `{sid}`", skill_text)
            self.assertIn("msitarzewski/agency-agents", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        # 1. Test link mode with agency-software-architect
        with tempfile.TemporaryDirectory(prefix="vas-agency-link-") as temp:
            project = Path(temp)
            result = cli(
                "install", "agency-software-architect",
                "--target", "cursor",
                "--mode", "link",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["cursor"][0]
            installed = dest_dir / "agency-software-architect"
            self.assertTrue(installed.exists())
            self.assertTrue(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("agency-software-architect", ledger)
            self.assertEqual(ledger["agency-software-architect"]["mode"], "link")

            status_res = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status_res.returncode, 0)
            self.assertIn("Total installed: 1", status_res.stdout)

            # Uninstall
            uninst_res = cli("uninstall", "agency-software-architect", "--target", "cursor", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

        # 2. Test copy mode with agency-frontend-developer
        with tempfile.TemporaryDirectory(prefix="vas-agency-copy-") as temp:
            project = Path(temp)
            result = cli(
                "install", "agency-frontend-developer",
                "--target", "claude",
                "--mode", "copy",
                cwd=project,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = project / VAS.AGENT_TARGET_MAP["claude"][0]
            installed = dest_dir / "agency-frontend-developer"
            self.assertTrue(installed.exists())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE.md").is_file())

            receipt_path = dest_dir / ".vas-manifest.json"
            self.assertTrue(receipt_path.exists())
            ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertIn("agency-frontend-developer", ledger)
            self.assertEqual(ledger["agency-frontend-developer"]["mode"], "copy")
            self.assertEqual(ledger["agency-frontend-developer"]["target_name"], "agency-frontend-developer")
            self.assertEqual(ledger["agency-frontend-developer"]["category"], "engineering")

            uninst_res = cli("uninstall", "agency-frontend-developer", "--target", "claude", cwd=project)
            self.assertEqual(uninst_res.returncode, 0)
            self.assertFalse(installed.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for sid in ["agency-software-architect", "agency-frontend-developer", "agency-ai-generated-code-security-auditor"]:
            self.assertIn(sid, manifests)
            m = manifests[sid]
            self.assertEqual(m["skill_id"], sid)
            self.assertEqual(m["target_name"], sid)
            self.assertEqual(m["provenance"]["author"], "AgentLand Contributors")
            self.assertEqual(m["provenance"]["source_repo"], "msitarzewski/agency-agents")

            file_paths = {f["path"] for f in m["files"]}
            self.assertIn("SKILL.md", file_paths)
            self.assertIn("LICENSE", file_paths)
            self.assertIn("NOTICE.md", file_paths)


if __name__ == "__main__":
    unittest.main()
