import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest

from test_local_project import ROOT, cli


class BlenderSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "skills_index.json").read_text())
        cls.skills = [s for s in cls.index if s["id"].startswith("blender-skills/")]
        cls.manifest = json.loads((ROOT / "data/blender-import.json").read_text())

    def test_exactly_one_canonical_pack_is_namespaced(self):
        self.assertEqual(len(self.skills), 94)
        self.assertEqual(self.manifest["skill_count"], 94)
        self.assertEqual(len({s["name"] for s in self.skills}), 94)
        self.assertEqual(len(self.index) - len(self.skills), 2964)
        for skill in self.skills:
            self.assertEqual(skill["canonical_id"], skill["id"])
            self.assertEqual(skill["category"], "blender")
            self.assertEqual(skill["source_repo"], "arjun988/blender-skills")
            self.assertEqual(skill["source_revision"], self.manifest["revision"])
            self.assertEqual(skill["license"], "MIT")
            self.assertTrue(skill["source_path"].startswith(".claude/skills/"))
            self.assertEqual(skill["risk"], "unknown")
            self.assertGreater(len(skill["description"]), 40)

    def test_vendored_files_and_only_documented_adaptations_match_hashes(self):
        revision = self.manifest["revision"]
        for record in self.manifest["files"]:
            with self.subTest(path=record["path"]):
                path = ROOT / record["path"]
                self.assertTrue(path.resolve().is_relative_to(ROOT))
                content = path.read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"])
                if path.name == "SKILL.md":
                    original = content.decode().replace("shared-references/", "../references/")
                    original = re.sub(
                        rf"https://github\.com/arjun988/blender-skills/blob/{revision}/\.claude/skills/(environment-artist|geometry-nodes|texture-workflow)/SKILL\.md",
                        lambda m: f"../{m[1]}/SKILL.md",
                        original,
                    ).encode()
                else:
                    original = content
                self.assertEqual(hashlib.sha256(original).hexdigest(), record["source_sha256"])

    def test_all_shared_references_and_license_ship_with_each_skill(self):
        license_text = (ROOT / "skills/blender-skills/LICENSE").read_text()
        for skill in self.skills:
            directory = ROOT / skill["path"]
            text = (directory / "SKILL.md").read_text()
            self.assertNotIn("../references/", text)
            self.assertEqual((directory / "LICENSE").read_text(), license_text)
            self.assertEqual(len(list((directory / "shared-references").glob("*.md"))), 9)
            for reference in re.findall(r"shared-references/([\w-]+\.md)", text):
                self.assertTrue((directory / "shared-references" / reference).is_file())
            self.assertFalse((directory / ".mcp.json").exists())

    def test_every_blender_skill_installs_and_uninstalls_in_both_modes(self):
        ids = [skill["id"] for skill in self.skills]
        for mode in ("copy", "link"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix="vie-blender-") as temp:
                destination = Path(temp) / "project with spaces" / "skills"
                installed = cli("install", *ids, "--mode", mode, "--dest", str(destination))
                self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
                manifest = json.loads((destination / ".vas-manifest.json").read_text())
                self.assertEqual(set(manifest), set(ids))
                for skill in self.skills:
                    target = destination / skill["id"].split("/")[-1]
                    source = ROOT / skill["path"]
                    self.assertEqual(target.is_symlink(), mode == "link")
                    self.assertEqual((target / "LICENSE").read_bytes(), (source / "LICENSE").read_bytes())
                    for path in source.rglob("*"):
                        if path.is_file():
                            self.assertEqual((target / path.relative_to(source)).read_bytes(), path.read_bytes())
                removed = cli("uninstall", *ids, "--dest", str(destination))
                self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                self.assertEqual(list(destination.iterdir()), [destination / ".vas-manifest.json"])


if __name__ == "__main__":
    unittest.main()
