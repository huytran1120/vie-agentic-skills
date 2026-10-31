import hashlib
import json
from pathlib import Path
import tempfile
import time
import unittest

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class VideoEditorSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/video-editor-import.json").read_text(encoding="utf-8"))
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skill_names = [
            "broll", "captions", "edit-video", "figma-roundtrip",
            "motion-overlays", "music-and-sound", "resolve-scripting",
            "rough-cut", "video-editor-setup", "vlog-pacing",
            "voice-and-audio", "youtube-export"
        ]
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identities_and_metadata(self):
        self.assertEqual(self.imported["skill_count"], 12)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["namespaces"], {})
        self.assertEqual(self.imported["revision"], "6709678d7d5b169149e13480428e12b0f09a47f0")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3172)

        # Check in source-credits.json
        self.assertIn("videoeditor", self.credits["sections"])
        self.assertIn("appariciojunior/video-editor-skills", self.credits["sections"]["videoeditor"][0])
        self.assertIn("6709678d7d5b169149e13480428e12b0f09a47f0", self.credits["sections"]["videoeditor"][0])
        self.assertIn("CC-BY-NC-4.0", self.credits["sections"]["videoeditor"][0])

        # Check all 12 in skills_index.json and catalog.json
        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        for name in self.skill_names:
            self.assertIn(name, self.skills_by_id)
            skill = self.skills_by_id[name]
            self.assertEqual(skill["canonical_id"], name)
            self.assertEqual(skill["category"], "media")
            self.assertEqual(skill["risk"], "safe")
            self.assertEqual(skill["author"], "appariciojunior")
            self.assertEqual(skill["license"], "CC-BY-NC-4.0")
            self.assertEqual(skill["source_repo"], "appariciojunior/video-editor-skills")
            self.assertEqual(skill["source_revision"], "6709678d7d5b169149e13480428e12b0f09a47f0")
            self.assertEqual(skill["path"], f"skills/{name}")

            self.assertIn(name, cat_by_id)
            cat_entry = cat_by_id[name]
            self.assertEqual(cat_entry["canonical_id"], name)
            self.assertEqual(cat_entry["category"], "media")
            self.assertEqual(cat_entry["license"], "CC-BY-NC-4.0")
            self.assertEqual(cat_entry["author"], "appariciojunior")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 26)  # 12 SKILL.md + 12 LICENSE + 1 config.example.json + 1 LEARNINGS.md
        paths_in_import = {r["path"] for r in records}
        self.assertEqual(len(paths_in_import), 26)

        for record in records:
            p = ROOT / record["path"]
            self.assertTrue(p.is_file(), f"Missing file: {p}")
            self.assertFalse(p.is_symlink())
            self.assertFalse(record["executable"])
            self.assertFalse(p.stat().st_mode & 0o111)
            content = p.read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"], str(p))

        # Check each skill has SKILL.md and LICENSE
        for name in self.skill_names:
            skill_dir = ROOT / "skills" / name
            self.assertTrue((skill_dir / "SKILL.md").is_file())
            self.assertTrue((skill_dir / "LICENSE").is_file())
            skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## VAS installation notes", skill_md_text)
            self.assertIn("appariciojunior/video-editor-skills", skill_md_text)
            self.assertIn("CC BY-NC 4.0", skill_md_text)
            self.assertIn("DaVinci Resolve Studio", skill_md_text)

        # Check video-editor-setup internal dependencies
        setup_dir = ROOT / "skills/video-editor-setup"
        self.assertTrue((setup_dir / "templates/config.example.json").is_file())
        self.assertTrue((setup_dir / "references/LEARNINGS.md").is_file())

    def test_cli_standalone_installation_and_receipt_and_uninstallation(self):
        for agent in ("cursor", "claude"):
            for mode in ("copy", "link"):
                with self.subTest(agent=agent, mode=mode), tempfile.TemporaryDirectory(prefix="vas-video-editor-") as temp:
                    project = Path(temp)
                    # Install broll
                    result = cli("install", "broll", "--target", agent, "--mode", mode, cwd=project)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    dest_dir = project / VAS.AGENT_TARGET_MAP[agent][0]
                    installed_broll = dest_dir / "broll"
                    self.assertTrue(installed_broll.exists())
                    self.assertEqual(installed_broll.is_symlink(), mode == "link")
                    self.assertTrue((installed_broll / "SKILL.md").is_file())
                    self.assertTrue((installed_broll / "LICENSE").is_file())

                    # Check receipt
                    receipt_file = dest_dir / ".vas-manifest.json"
                    self.assertTrue(receipt_file.is_file())
                    ledger = json.loads(receipt_file.read_text(encoding="utf-8"))
                    self.assertIn("broll", ledger)
                    self.assertEqual(ledger["broll"]["target_name"], "broll")

                    # Install video-editor-setup (with templates and references)
                    result = cli("install", "video-editor-setup", "--target", agent, "--mode", mode, cwd=project)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    installed_setup = dest_dir / "video-editor-setup"
                    self.assertTrue((installed_setup / "SKILL.md").is_file())
                    self.assertTrue((installed_setup / "LICENSE").is_file())
                    self.assertTrue((installed_setup / "templates/config.example.json").is_file())
                    self.assertTrue((installed_setup / "references/LEARNINGS.md").is_file())

                    # Status
                    status_res = cli("status", "--target", agent, cwd=project)
                    self.assertEqual(status_res.returncode, 0)
                    self.assertIn("Total installed: 2", status_res.stdout)

                    # Uninstall
                    uninst_res = cli("uninstall", "broll", "--target", agent, cwd=project)
                    self.assertEqual(uninst_res.returncode, 0)
                    self.assertFalse(installed_broll.exists())
                    self.assertTrue(installed_setup.exists())

                    # Uninstall setup
                    uninst_res2 = cli("uninstall", "video-editor-setup", "--target", agent, cwd=project)
                    self.assertEqual(uninst_res2.returncode, 0)
                    self.assertFalse(installed_setup.exists())

    def test_pages_installation_manifests_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        for name in self.skill_names:
            self.assertIn(name, manifests)
            m = manifests[name]
            self.assertEqual(m["skill_id"], name)
            self.assertEqual(m["target_name"], name)
            self.assertEqual(m["provenance"]["category"], "media")
            self.assertEqual(m["provenance"]["license"], "CC-BY-NC-4.0")
            self.assertEqual(m["provenance"]["author"], "appariciojunior")
            self.assertEqual(m["provenance"]["source_repo"], "appariciojunior/video-editor-skills")
            file_paths = {f["path"] for f in m["files"]}
            self.assertIn("SKILL.md", file_paths)
            self.assertIn("LICENSE", file_paths)
            if name == "video-editor-setup":
                self.assertIn("templates/config.example.json", file_paths)
                self.assertIn("references/LEARNINGS.md", file_paths)


if __name__ == "__main__":
    unittest.main()
