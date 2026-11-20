#!/usr/bin/env python3
"""Tests for the 32-skill motion graphics and Blender 5.x batch import."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_pages as PAGES


def cli(*args, cwd=ROOT):
    cmd = [sys.executable, str(ROOT / "vas.py"), *args]
    return subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


MANIFEST_SPECS = (
    ("data/reanimate-import.json", "NiazMorshed2007/reanimate", "3f7a55a2986a84ca2173e86ee9127eefe31d046d", "MIT", 1, "reanimate", "reanimate"),
    ("data/huashu-art-motion-import.json", "alchaincyf/huashu-art-motion", "a97c45018d46e950d56d61981138e08f4e092909", "MIT", 1, "huashuartmotion", "huashu-art-motion"),
    ("data/anidoodle-import.json", "alexgreensh/anidoodle", "4ae27d2c281fcfd01bce87ab13dc5ad4df81a795", "Apache-2.0", 1, "anidoodle", "anidoodle"),
    ("data/cinetic-import.json", "Leonxlnx/cinetic", "f4bbfc844877891fe92279d47b7874fb44d485ae", "MIT", 1, "cinetic", "cinetic"),
    ("data/el4cteo-blender-import.json", "EL4CTEO/blender-skills", "9e7e04a603c125a0d17447ab97112fa70a865067", "MIT", 28, "el4cteoblender", "blender-core"),
)


class TestMotionBlenderBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["canonical_id"]: s for s in cls.index}

    def test_catalog_counts_and_all_five_manifests(self):
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4128)

        total_new = 0
        for rel_manifest, repo, rev, lic, count, credit_key, sample_id in MANIFEST_SPECS:
            with self.subTest(manifest=rel_manifest):
                data = json.loads((ROOT / rel_manifest).read_text(encoding="utf-8"))
                self.assertEqual(data["source_repo"], repo)
                self.assertEqual(data["revision"], rev)
                self.assertEqual(data["license"], lic)
                self.assertEqual(data["skill_count"], count)
                self.assertEqual(len(data["skills"]), count)
                self.assertIn(credit_key, self.credits["sections"])
                self.assertIn(repo, self.credits["sections"][credit_key][0])
                self.assertIn(rev, self.credits["sections"][credit_key][0])

                for meta in data["skills"]:
                    cid = meta["canonical_id"]
                    self.assertIn(cid, self.skills_by_id)
                    indexed = self.skills_by_id[cid]
                    self.assertEqual(indexed["source_repo"], repo)
                    self.assertEqual(indexed["source_revision"], rev)
                    self.assertEqual(indexed["license"], lic)
                total_new += count
        self.assertEqual(total_new, 32)

    def test_file_inventory_checksums_and_executable_bits(self):
        for rel_manifest, *_ in MANIFEST_SPECS:
            data = json.loads((ROOT / rel_manifest).read_text(encoding="utf-8"))
            with self.subTest(manifest=rel_manifest):
                self.assertGreater(len(data["files"]), 0)
                for record in data["files"]:
                    file_path = ROOT / record["path"]
                    self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")
                    self.assertFalse(file_path.is_symlink(), f"Unexpected symlink: {file_path}")
                    h = hashlib.sha256()
                    with open(file_path, "rb") as f:
                        while chunk := f.read(65536):
                            h.update(chunk)
                    self.assertEqual(h.hexdigest(), record["sha256"], f"Checksum mismatch: {file_path}")
                    st = os.stat(file_path)
                    is_exec = bool(st.st_mode & 0o111) and file_path.suffix != ".md"
                    self.assertEqual(is_exec, record["executable"], f"Executable bit mismatch: {file_path}")

    def test_cli_install_status_uninstall_isolated(self):
        samples = ["reanimate", "huashu-art-motion", "anidoodle", "cinetic", "blender-core", "blender-animation"]
        for mode in ("copy", "link"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix=f"vas-motion-{mode}-") as tmpdir:
                dest = Path(tmpdir) / ".agents/skills"
                dest.mkdir(parents=True, exist_ok=True)
                for sid in samples:
                    res_show = cli("show", sid)
                    self.assertEqual(res_show.returncode, 0, res_show.stderr)
                    res_install = cli("install", sid, "--target", "workspace", "--mode", mode, "--dest", str(dest))
                    self.assertEqual(res_install.returncode, 0, res_install.stderr)
                    installed_dir = dest / sid
                    self.assertTrue((installed_dir / "SKILL.md").is_file())
                    self.assertTrue((installed_dir / "LICENSE").is_file())
                    self.assertTrue((installed_dir / "NOTICE.md").is_file())
                res_status = cli("status", "--target", "workspace", "--dest", str(dest))
                self.assertEqual(res_status.returncode, 0, res_status.stderr)
                for sid in samples:
                    self.assertIn(sid, res_status.stdout)
                    res_un = cli("uninstall", sid, "--target", "workspace", "--dest", str(dest))
                    self.assertEqual(res_un.returncode, 0, res_un.stderr)
                    self.assertFalse((dest / sid).exists())

    def test_pages_install_manifests_cover_all_32_skills(self):
        manifests = PAGES.installation_manifests(ROOT)
        for rel_manifest, repo, _, lic, _, _, _ in MANIFEST_SPECS:
            data = json.loads((ROOT / rel_manifest).read_text(encoding="utf-8"))
            for meta in data["skills"]:
                cid = meta["canonical_id"]
                with self.subTest(skill=cid):
                    self.assertIn(cid, manifests)
                    entry = manifests[cid]
                    self.assertEqual(entry["schema_version"], 1)
                    self.assertEqual(entry["skill_id"], cid)
                    self.assertEqual(entry["target_name"], cid)
                    self.assertEqual(entry["source_path"], f"skills/{cid}")
                    self.assertEqual(entry["provenance"]["source_repo"], repo)
                    self.assertEqual(entry["provenance"]["license"], lic)
                    paths = {f["path"] for f in entry["files"]}
                    self.assertIn("SKILL.md", paths)
                    self.assertIn("LICENSE", paths)
                    self.assertIn("NOTICE.md", paths)


if __name__ == "__main__":
    unittest.main()
