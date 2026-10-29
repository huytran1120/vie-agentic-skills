import hashlib
import json
from pathlib import Path
import re
import tempfile
import time
import unittest

from test_local_project import ROOT, cli
from test_pages_build import PAGES


class HallmarkSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = ROOT / "skills/hallmark"
        cls.manifest = json.loads((ROOT / "data/hallmark-import.json").read_text())
        cls.index = json.loads((ROOT / "skills_index.json").read_text())
        cls.skill = next(skill for skill in cls.index if skill["id"] == "hallmark")

    def test_one_canonical_skill_has_complete_source_and_license_metadata(self):
        self.assertEqual(len([s for s in self.index if s["id"] == "hallmark"]), 1)
        self.assertEqual(self.manifest["skill_count"], 1)
        self.assertEqual(self.manifest["source_repo"], "Nutlope/hallmark")
        self.assertEqual(self.manifest["revision"], "8f6969f8922caabde9de1784959eae11ddf68073")
        expected = {
            "id": "hallmark", "canonical_id": "hallmark", "name": "hallmark",
            "path": "skills/hallmark", "category": "front-end", "risk": "unknown",
            "source_repo": "Nutlope/hallmark", "source_path": "skills/hallmark/SKILL.md",
            "source_revision": self.manifest["revision"], "license": "MIT",
            "author": "Hallmark contributors / Together AI",
        }
        for key, value in expected.items():
            self.assertEqual(self.skill[key], value, key)
        self.assertIn("Copyright (c) 2026 Hallmark contributors",
                      (self.pack / "LICENSE").read_text())
        for filename in ("data/catalog.json", "data/skills_index.json"):
            data = json.loads((ROOT / filename).read_text())
            rows = data["skills"] if isinstance(data, dict) else data
            matches = [row for row in rows if row["id"] == "hallmark"]
            self.assertEqual(len(matches), 1)
            for key in ("canonical_id", "source_repo", "source_revision",
                        "source_path", "license", "author"):
                self.assertEqual(matches[0][key], self.skill[key], key)
        credits = json.loads((ROOT / "data/source-credits.json").read_text())
        self.assertIn(self.manifest["revision"], credits["sections"]["hallmark"][0])

    def test_all_182_files_preserve_hashes_modes_and_reversible_notes(self):
        records = self.manifest["files"]
        self.assertEqual(len(records), 182)
        self.assertEqual(len({record["source_path"] for record in records}), len(records))
        recorded = set()
        for record in records:
            path = ROOT / record["path"]
            self.assertTrue(path.resolve().is_relative_to(self.pack))
            self.assertFalse(path.is_symlink())
            content = path.read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"])
            self.assertEqual(bool(path.stat().st_mode & 0o111), record["executable"])
            if path.name == "SKILL.md":
                notes = self.manifest["skill_notes"].encode()
                self.assertTrue(content.endswith(notes))
                content = content[:-len(notes)]
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["source_sha256"])
            git_blob = b"blob " + str(len(content)).encode() + b"\0" + content
            self.assertEqual(hashlib.sha1(git_blob).hexdigest(), record["source_git_blob"])
            recorded.add(path)
        self.assertEqual(recorded, {path for path in self.pack.rglob("*") if path.is_file()})
        original_body = (self.pack / "SKILL.md").read_text()
        original_body = original_body[:-len(self.manifest["skill_notes"])]
        original_body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", original_body, flags=re.S)
        normalized = " ".join(original_body.split())
        for skill in self.index:
            if skill["id"] != "hallmark":
                body = (ROOT / skill["path"] / "SKILL.md").read_text(errors="replace")
                body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", body, flags=re.S)
                self.assertNotEqual(" ".join(body.split()), normalized, skill["id"])

    def test_standalone_references_themes_and_photo_attribution_are_complete(self):
        for path in self.pack.rglob("*.md"):
            for target in re.findall(r"\]\(([^)\s]+)\)", path.read_text()):
                if re.match(r"^(https?:|mailto:|#)", target) or "<" in target:
                    continue
                relative = target.split("#")[0]
                if relative:
                    self.assertTrue((path.parent / relative).is_file(), f"{path}: {target}")
        themes = json.loads((self.pack / "references/themes/index.json").read_text())["themes"]
        self.assertEqual(len(themes), 50)
        for theme in themes:
            for suffix in (".md", ".jpg"):
                self.assertTrue((self.pack / "references/themes" / (theme["slug"] + suffix)).is_file())
        photos = json.loads((self.pack / "scripts/photos.json").read_text())["photos"]
        self.assertEqual(len(photos), 755)
        for photo in photos:
            for key in ("file", "page", "license", "author"):
                self.assertTrue(photo[key], key)
        self.assertEqual(len(list((self.pack / "scripts").glob("*.mjs"))), 10)
        for relative in ("scripts/sloplint-render.mjs", "scripts/photos.json",
                         "scripts/fixtures/kept/before.html", "agents/openai.yaml"):
            self.assertTrue((self.pack / relative).is_file(), relative)
        notes = self.manifest["skill_notes"]
        for text in ("Node.js 18", "TOGETHER_API_KEY", "CC BY-SA",
                     "do not", "scripts/install.mjs", "scripts/install-hook.mjs"):
            self.assertIn(text, notes)

    def test_isolated_link_and_copy_installs_use_every_agent_mapping(self):
        targets = {
            "antigravity": ".agents/skills", "codex": ".codex/skills",
            "claude": ".claude/skills", "cursor": ".cursor/skills",
            "windsurf": ".windsurf/skills", "cline": ".cline/skills",
            "copilot": ".github/skills",
        }
        for mode in ("copy", "link"):
            for target, relative in targets.items():
                with self.subTest(mode=mode, target=target), tempfile.TemporaryDirectory(prefix="vas-hallmark-") as temp:
                    project = Path(temp)
                    result = cli("install", "hallmark", "--target", target, "--mode", mode, cwd=project)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    destination = project / relative
                    installed = destination / "hallmark"
                    self.assertEqual(installed.is_symlink(), mode == "link")
                    for record in self.manifest["files"]:
                        source = ROOT / record["path"]
                        file = installed / source.relative_to(self.pack)
                        self.assertEqual(file.read_bytes(), source.read_bytes())
                        self.assertEqual(bool(file.stat().st_mode & 0o111), record["executable"])
                    receipt = json.loads((destination / ".vas-manifest.json").read_text())
                    self.assertEqual(set(receipt), {"hallmark"})
                    self.assertEqual(receipt["hallmark"]["target_name"], "hallmark")
                    status = cli("status", "--target", target, cwd=project)
                    self.assertEqual(status.returncode, 0, status.stderr)
                    self.assertIn("Total installed: 1", status.stdout)
                    removed = cli("uninstall", "hallmark", "--target", target, cwd=project)
                    self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                    self.assertEqual(list(destination.iterdir()), [destination / ".vas-manifest.json"])

    def test_complete_install_manifest_and_remote_receipt_work_with_the_cli(self):
        manifest = PAGES.installation_manifests(ROOT)["hallmark"]
        revision = manifest["revision"]
        self.assertRegex(revision, r"^[0-9a-f]{40}$")
        self.assertNotEqual(revision, self.manifest["revision"])
        self.assertEqual(manifest["skill_id"], "hallmark")
        self.assertEqual(manifest["target_name"], "hallmark")
        self.assertEqual(manifest["provenance"]["source_repo"], "Nutlope/hallmark")
        self.assertIn(self.manifest["revision"], manifest["provenance"]["source"])
        self.assertEqual(manifest["receipt"]["key"], "hallmark")
        expected = {
            str(Path(record["path"]).relative_to("skills/hallmark")): record
            for record in self.manifest["files"]
        }
        self.assertEqual({file["path"] for file in manifest["files"]}, set(expected))
        with tempfile.TemporaryDirectory(prefix="vas-hallmark-receipt-") as temp:
            project = Path(temp)
            destination = project / ".cursor/skills"
            for file in manifest["files"]:
                self.assertEqual(file["sha256"], expected[file["path"]]["sha256"])
                self.assertEqual(file["executable"], expected[file["path"]]["executable"])
                if manifest["available"]:
                    self.assertTrue(file["url"].startswith(
                        f"https://raw.githubusercontent.com/huytran1120/vie-agentic-skills/{revision}/skills/hallmark/"
                    ))
                else:
                    self.assertEqual(manifest["unavailable_reason"], "unpublished_local_changes")
                    self.assertNotIn("url", file)
                content = (self.pack / file["path"]).read_bytes()
                self.assertEqual(len(content), file["bytes"])
                target = destination / manifest["target_name"] / file["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                target.chmod(0o755 if file["executable"] else 0o644)
            receipt = manifest["receipt"]
            ledger = {
                receipt["key"]: {**receipt["entry"], "installed_at": int(time.time())},
                "keep": {"target_name": "keep", "mode": "copy"},
            }
            ledger_path = destination / receipt["filename"]
            ledger_path.write_text(json.dumps(ledger))
            status = cli("status", "--target", "cursor", cwd=project)
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("hallmark", status.stdout)
            removed = cli("uninstall", "hallmark", "--target", "cursor", cwd=project)
            self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
            self.assertFalse((destination / "hallmark").exists())
            self.assertEqual(json.loads(ledger_path.read_text()), {"keep": ledger["keep"]})


if __name__ == "__main__":
    unittest.main()
