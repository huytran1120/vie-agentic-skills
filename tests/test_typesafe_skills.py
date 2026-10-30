import hashlib
import json
from pathlib import Path
import re
import tempfile
import time
import unittest

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class TypeSafeSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = ROOT / "skills/typesafe-ai"
        cls.manifest = json.loads((ROOT / "data/typesafe-import.json").read_text())
        cls.index = json.loads((ROOT / "skills_index.json").read_text())
        cls.skill = next(skill for skill in cls.index if skill["id"] == "typesafe-ai")

    def test_canonical_identity_source_and_mit_notice_are_preserved(self):
        expected = {
            "id": "typesafe-ai", "canonical_id": "typesafe-ai", "name": "typesafe-ai",
            "path": "skills/typesafe-ai", "category": "ai-ml", "risk": "unknown",
            "source_repo": "typesafe-ai/skills",
            "source_path": "skills/typesafe-ai/SKILL.md",
            "source_revision": "302eea662c54bca6730873fe245bec1d69ebc23d",
            "license": "MIT", "author": "TypeSafe AI",
        }
        for key, value in expected.items():
            self.assertEqual(self.skill[key], value, key)
        matches = [s for s in self.index if s.get("source_repo") == "typesafe-ai/skills"]
        self.assertEqual([s["id"] for s in matches], ["typesafe-ai"])
        self.assertEqual(VAS.resolve_skill_id("typesafe-ai", {s["id"]: s for s in self.index}),
                         "typesafe-ai")
        for filename in ("data/catalog.json", "data/skills_index.json"):
            data = json.loads((ROOT / filename).read_text())
            rows = data["skills"] if isinstance(data, dict) else data
            matches = [row for row in rows if row["id"] == "typesafe-ai"]
            self.assertEqual(len(matches), 1)
            for key in ("canonical_id", "source_repo", "source_revision", "source_path",
                        "description", "license", "author"):
                self.assertEqual(matches[0][key], self.skill[key], key)
        license_text = (self.pack / "LICENSE").read_text()
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 TypeSafe AI", license_text)
        credits = json.loads((ROOT / "data/source-credits.json").read_text())
        self.assertIn(self.manifest["revision"], credits["sections"]["typesafe"][0])

    def test_complete_payload_hashes_modes_and_adaptation_are_reversible(self):
        self.assertEqual(self.manifest["source_repo"], self.skill["source_repo"])
        self.assertEqual(self.manifest["revision"], self.skill["source_revision"])
        self.assertEqual(self.manifest["skill_count"], 1)
        records = self.manifest["files"]
        expected = {"skills/typesafe-ai/SKILL.md", "skills/typesafe-ai/LICENSE"}
        self.assertEqual({record["path"] for record in records}, expected)
        self.assertEqual(len(records), 2)
        self.assertEqual({path.relative_to(ROOT).as_posix()
                          for path in self.pack.rglob("*") if path.is_file()}, expected)
        for record in records:
            path = ROOT / record["path"]
            self.assertEqual(record["source_path"], record["path"])
            self.assertFalse(path.is_symlink())
            self.assertFalse(record["executable"])
            self.assertFalse(path.stat().st_mode & 0o111)
            content = path.read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"])
            if path.name == "SKILL.md":
                notes = self.manifest["skill_notes"].encode()
                self.assertTrue(content.endswith(notes))
                content = content[:-len(notes)]
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["source_sha256"])
            blob = b"blob " + str(len(content)).encode() + b"\0" + content
            self.assertEqual(hashlib.sha1(blob).hexdigest(), record["source_git_blob"])

    def test_runbook_has_no_missing_local_dependencies_and_retains_consent(self):
        text = (self.pack / "SKILL.md").read_text()
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            self.assertTrue((self.pack / target.split("#")[0]).is_file(), target)
        for required in ("TYPESAFE_API_KEY", "Ask the\nuser for permission first",
                         "Get a budget", "disclose what data will be sent",
                         "Keep API keys on the server", "external documentation links",
                         "does not install an SDK"):
            self.assertIn(required, text)
        body = text[:-len(self.manifest["skill_notes"])]
        body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", body, flags=re.S)
        normalized = " ".join(body.split())
        for skill in self.index:
            if skill["id"] == "typesafe-ai":
                continue
            other = (ROOT / skill["path"] / "SKILL.md").read_text(errors="replace")
            other = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", other, flags=re.S)
            self.assertNotEqual(" ".join(other.split()), normalized, skill["id"])

    def test_temporary_link_and_copy_installs_use_all_seven_agent_destinations(self):
        targets = {
            "antigravity": ".agents/skills", "codex": ".codex/skills",
            "claude": ".claude/skills", "cursor": ".cursor/skills",
            "windsurf": ".windsurf/skills", "cline": ".cline/skills",
            "copilot": ".github/skills",
        }
        for mode in ("copy", "link"):
            for target, relative in targets.items():
                with self.subTest(mode=mode, target=target), tempfile.TemporaryDirectory(prefix="vas-typesafe-") as temp:
                    project = Path(temp)
                    result = cli("install", "typesafe-ai", "--target", target, "--mode", mode, cwd=project)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    destination = project / relative
                    installed = destination / "typesafe-ai"
                    self.assertEqual(installed.is_symlink(), mode == "link")
                    self.assertEqual({path.name for path in installed.iterdir()}, {"SKILL.md", "LICENSE"})
                    for path in self.pack.iterdir():
                        self.assertEqual((installed / path.name).read_bytes(), path.read_bytes())
                        self.assertFalse((installed / path.name).stat().st_mode & 0o111)
                    receipt_path = destination / ".vas-manifest.json"
                    receipt = json.loads(receipt_path.read_text())
                    self.assertEqual(set(receipt), {"typesafe-ai"})
                    self.assertEqual(receipt["typesafe-ai"]["target_name"], "typesafe-ai")
                    self.assertEqual(receipt["typesafe-ai"]["mode"], mode)
                    status = cli("status", "--target", target, cwd=project)
                    self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
                    self.assertIn("Total installed: 1", status.stdout)
                    removed = cli("uninstall", "typesafe-ai", "--target", target, cwd=project)
                    self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                    self.assertEqual(json.loads(receipt_path.read_text()), {})
                    self.assertEqual(list(destination.iterdir()), [receipt_path])

    def test_complete_manifest_and_quick_install_receipt_work_with_the_cli(self):
        manifest = PAGES.installation_manifests(ROOT)["typesafe-ai"]
        revision = manifest["revision"]
        self.assertRegex(revision, r"^[0-9a-f]{40}$")
        self.assertNotEqual(revision, self.manifest["revision"])
        self.assertEqual(manifest["skill_id"], "typesafe-ai")
        self.assertEqual(manifest["target_name"], "typesafe-ai")
        self.assertEqual(manifest["provenance"]["source_repo"], self.skill["source_repo"])
        self.assertIn(self.manifest["revision"], manifest["provenance"]["source"])
        self.assertEqual(manifest["receipt"]["key"], "typesafe-ai")
        self.assertEqual({file["path"] for file in manifest["files"]}, {"SKILL.md", "LICENSE"})
        with tempfile.TemporaryDirectory(prefix="vas-typesafe-receipt-") as temp:
            project = Path(temp)
            destination = project / ".cursor/skills"
            for file in manifest["files"]:
                content = (self.pack / file["path"]).read_bytes()
                self.assertEqual(file["bytes"], len(content))
                self.assertEqual(file["sha256"], hashlib.sha256(content).hexdigest())
                self.assertFalse(file["executable"])
                if manifest["available"]:
                    self.assertEqual(file["url"],
                                     f"https://raw.githubusercontent.com/huytran1120/vie-agentic-skills/{revision}/skills/typesafe-ai/{file['path']}")
                else:
                    self.assertEqual(manifest["unavailable_reason"], "unpublished_local_changes")
                    self.assertNotIn("url", file)
                target = destination / "typesafe-ai" / file["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                target.chmod(0o644)
            receipt = manifest["receipt"]
            ledger = {
                receipt["key"]: {**receipt["entry"], "installed_at": int(time.time())},
                "keep": {"target_name": "keep", "mode": "copy"},
            }
            ledger_path = destination / receipt["filename"]
            ledger_path.write_text(json.dumps(ledger))
            for action in ("status", "uninstall"):
                args = [action] + (["typesafe-ai"] if action == "uninstall" else [])
                result = cli(*args, "--target", "cursor", "--dest", str(destination), cwd=project)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("typesafe-ai", result.stdout)
            self.assertFalse((destination / "typesafe-ai").exists())
            self.assertEqual(json.loads(ledger_path.read_text()), {"keep": ledger["keep"]})


if __name__ == "__main__":
    unittest.main()
