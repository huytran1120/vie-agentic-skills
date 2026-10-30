import ast
import hashlib
import json
from pathlib import Path
import re
import tempfile
import time
import unittest
from urllib.parse import unquote

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class AndroidSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/android-import.json").read_text())
        cls.index = json.loads((ROOT / "skills_index.json").read_text())
        cls.skills = [s for s in cls.index if s.get("source_repo") == "android/skills"]
        cls.records = cls.imported["files"]

    def test_unique_canonical_sources_and_existing_cli_is_not_upgraded(self):
        self.assertEqual(len(self.skills), 35)
        self.assertEqual(self.imported["skill_count"], 35)
        self.assertEqual(len(self.records), 478)
        self.assertEqual(self.imported["revision"], "6daa53ef27fa2aa87827d183a85c06cedceca833")
        self.assertEqual(len({s["source_path"] for s in self.skills}), 35)
        for skill in self.skills:
            for key in ("id", "canonical_id", "name"):
                self.assertEqual(skill[key], Path(skill["path"]).name)
            self.assertEqual(skill["path"], f"skills/{skill['id']}")
            self.assertEqual(skill["category"], "mobile")
            self.assertEqual(skill["risk"], "unknown")
            self.assertEqual(skill["license"], "Apache-2.0")
            self.assertEqual(skill["author"], "Google LLC")
            self.assertEqual(skill["source_revision"], self.imported["revision"])
            self.assertIn(self.imported["revision"], skill["source"])
            self.assertIn(self.imported["revision"], skill["license_source"])
            self.assertIn("android", skill["tags"])
            self.assertNotEqual(skill["description"], "No description available")
        skipped, = self.imported["skipped"]
        self.assertEqual(skipped["id"], "android-cli")
        existing, = [s for s in self.index if s["id"] == "android-cli"]
        self.assertEqual(existing["author"], "Owais")
        self.assertEqual(hashlib.sha256((ROOT / existing["path"] / "SKILL.md").read_bytes()).hexdigest(),
                         skipped["existing_sha256"])
        self.assertNotIn(existing, self.skills)
        for filename in ("data/catalog.json", "data/skills_index.json"):
            data = json.loads((ROOT / filename).read_text())
            rows = data["skills"] if isinstance(data, dict) else data
            actual = {s["id"]: s for s in rows if s.get("source_repo") == "android/skills"}
            self.assertEqual(len(actual), 35)
            for skill in self.skills:
                for key in ("canonical_id", "source_path", "source_revision", "description", "license"):
                    self.assertEqual(actual[skill["id"]][key], skill[key])

    def test_complete_inventory_hashes_modes_and_reversible_adaptations(self):
        expected = {r["path"] for r in self.records}
        self.assertEqual(len(expected), len(self.records))
        actual = {p.relative_to(ROOT).as_posix() for s in self.skills
                  for p in (ROOT / s["path"]).rglob("*") if p.is_file()}
        self.assertEqual(actual, expected)
        executables = []
        for record in self.records:
            path = ROOT / record["path"]
            self.assertFalse(path.is_symlink())
            self.assertEqual(bool(path.stat().st_mode & 0o111), record["executable"], str(path))
            content = path.read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"], str(path))
            if path.name == "SKILL.md":
                notes = self.imported["skill_notes"].encode()
                self.assertTrue(content.endswith(notes))
                content = content[:-len(notes)]
                for change in reversed(self.imported["runbook_adaptations"][path.parent.name]):
                    before, after = change["before"].encode(), change["after"].encode()
                    self.assertEqual(content.count(after), 1)
                    content = content.replace(after, before, 1)
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["source_sha256"], str(path))
            blob = b"blob " + str(len(content)).encode() + b"\0" + content
            self.assertEqual(hashlib.sha1(blob).hexdigest(), record["source_git_blob"], str(path))
            if record["executable"]:
                executables.append(path.name)
        self.assertEqual(sorted(executables),
                         ["generate_report.py", "orchestrator.py", "play_store_scraper.py", "scanner.py"])
        license_hashes = {r["sha256"] for r in self.records if r["source_path"] == "LICENSE.txt"}
        self.assertEqual(len(license_hashes), 1)
        for skill in self.skills:
            license_text = (ROOT / skill["path"] / "LICENSE.txt").read_text()
            self.assertIn("Apache License", license_text)
            self.assertIn("Version 2.0, January 2004", license_text)

    def test_standalone_local_links_helpers_samples_and_consent_notes(self):
        for skill in self.skills:
            pack = ROOT / skill["path"]
            text = (pack / "SKILL.md").read_text()
            self.assertIn("It does not install or", text)
            self.assertIn("Obtain explicit permission", text)
            self.assertIn("No helpers were run", text)
            for document in pack.rglob("*.md"):
                content = re.sub(r"```.*?```", "", document.read_text(), flags=re.S)
                for target in re.findall(r"\]\(([^)\s]+)\)", content):
                    if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|/)", target, re.I):
                        continue
                    relative = unquote(target.split("#")[0].split("?")[0])
                    resolved = (document.parent / relative).resolve()
                    self.assertTrue(resolved.exists(), f"{document}: {target}")
                    self.assertTrue(resolved.is_relative_to(pack), f"{document}: {target}")
            for script in pack.rglob("*.py"):
                tree = ast.parse(script.read_text())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in {"scanner", "play_store_scraper", "keep_radius_pb2"}:
                                self.assertTrue((script.parent / f"{alias.name}.py").is_file())
                    elif isinstance(node, ast.ImportFrom) and node.module == "template_engine":
                        self.assertTrue((script.parent / "template_engine.py").is_file())
        self.assertTrue(list((ROOT / "skills/glance-canonical-layouts").rglob("*.kt")))
        self.assertTrue(list((ROOT / "skills/glance-canonical-layouts").rglob("*.xml")))
        launcher = ROOT / "skills/android-profiler/references/perfetto/bin/trace_processor"
        self.assertTrue(launcher.is_file())
        self.assertFalse(launcher.stat().st_mode & 0o111)
        protobuf = (ROOT / "skills/r8-analyzer/scripts/keep_radius_pb2.py").read_text()
        self.assertIn("6, 33, 4", protobuf)

    def test_new_bodies_are_distinct_from_existing_and_each_other(self):
        def body(text):
            text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
            text = text.partition("\n## VAS installation notes")[0]
            return " ".join(text.split())
        added = {s["id"] for s in self.skills}
        previous = {body((ROOT / s["path"] / "SKILL.md").read_text(errors="replace"))
                    for s in self.index if s["id"] not in added}
        new = [body((ROOT / s["path"] / "SKILL.md").read_text()) for s in self.skills]
        self.assertEqual(len(set(new)), 35)
        self.assertFalse(previous.intersection(new))
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3058)

    def test_each_skill_installs_independently_for_every_agent_in_both_modes(self):
        for skill in self.skills:
            pack = ROOT / skill["path"]
            records = [r for r in self.records if r["path"].startswith(skill["path"] + "/")]
            for mode in ("copy", "link"):
                for target, folders in VAS.AGENT_TARGET_MAP.items():
                    if target not in {"antigravity", "codex", "claude", "cursor", "windsurf", "cline", "copilot"}:
                        continue
                    with self.subTest(skill=skill["id"], mode=mode, target=target), tempfile.TemporaryDirectory(prefix="vas-android-") as temp:
                        project = Path(temp)
                        destination = project / folders[0]
                        result = cli("install", skill["id"], "--target", target, "--mode", mode, cwd=project)
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                        installed = destination / skill["id"]
                        self.assertEqual(installed.is_symlink(), mode == "link")
                        self.assertEqual({p.relative_to(installed).as_posix() for p in installed.rglob("*") if p.is_file()},
                                         {str(Path(r["path"]).relative_to(skill["path"])) for r in records})
                        for record in records:
                            file = installed / Path(record["path"]).relative_to(skill["path"])
                            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), record["sha256"])
                            self.assertEqual(bool(file.stat().st_mode & 0o111), record["executable"])
                        ledger_path = destination / ".vas-manifest.json"
                        ledger = json.loads(ledger_path.read_text())
                        self.assertEqual(set(ledger), {skill["id"]})
                        self.assertEqual(ledger[skill["id"]]["target_name"], pack.name)
                        status = cli("status", "--target", target, cwd=project)
                        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
                        self.assertIn("Total installed: 1", status.stdout)
                        removed = cli("uninstall", skill["id"], "--target", target, cwd=project)
                        self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                        self.assertEqual(json.loads(ledger_path.read_text()), {})
                        self.assertFalse(installed.exists())

    def test_complete_manifests_and_every_quick_install_receipt_round_trip(self):
        manifests = PAGES.installation_manifests(ROOT)
        for skill in self.skills:
            manifest = manifests[skill["id"]]
            self.assertNotEqual(manifest["revision"], self.imported["revision"])
            self.assertEqual(manifest["provenance"]["source_repo"], "android/skills")
            records = {str(Path(r["path"]).relative_to(skill["path"])): r
                       for r in self.records if r["path"].startswith(skill["path"] + "/")}
            self.assertEqual({f["path"] for f in manifest["files"]}, set(records))
            with tempfile.TemporaryDirectory(prefix="vas-android-receipt-") as temp:
                project = Path(temp)
                destination = project / ".cursor/skills"
                for file in manifest["files"]:
                    content = (ROOT / skill["path"] / file["path"]).read_bytes()
                    self.assertEqual(file["bytes"], len(content))
                    self.assertEqual(file["sha256"], records[file["path"]]["sha256"])
                    self.assertEqual(file["executable"], records[file["path"]]["executable"])
                    if manifest["available"]:
                        self.assertIn(f"/{manifest['revision']}/{skill['path']}/", file["url"])
                    else:
                        self.assertEqual(manifest["unavailable_reason"], "unpublished_local_changes")
                        self.assertNotIn("url", file)
                    target = destination / manifest["target_name"] / file["path"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                    target.chmod(0o755 if file["executable"] else 0o644)
                receipt = manifest["receipt"]
                ledger = {receipt["key"]: {**receipt["entry"], "installed_at": int(time.time())},
                          "keep": {"target_name": "keep", "mode": "copy"}}
                ledger_path = destination / receipt["filename"]
                ledger_path.write_text(json.dumps(ledger))
                for action in ("status", "uninstall"):
                    args = [action] + ([skill["id"]] if action == "uninstall" else [])
                    result = cli(*args, "--target", "cursor", cwd=project)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn(skill["id"], result.stdout)
                self.assertFalse((destination / manifest["target_name"]).exists())
                self.assertEqual(json.loads(ledger_path.read_text()), {"keep": ledger["keep"]})


if __name__ == "__main__":
    unittest.main()
