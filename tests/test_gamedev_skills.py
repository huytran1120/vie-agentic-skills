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


class GameDevSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads((ROOT / "data/gamedev-import.json").read_text())
        cls.index = json.loads((ROOT / "skills_index.json").read_text())
        cls.skills = [s for s in cls.index if s.get("source_repo") == cls.imported["source_repo"]]
        cls.records = cls.imported["files"]
        cls.targets = {
            "antigravity": ".agents/skills", "codex": ".codex/skills",
            "claude": ".claude/skills", "cursor": ".cursor/skills",
            "windsurf": ".windsurf/skills", "cline": ".cline/skills",
            "copilot": ".github/skills",
        }

    def test_exact_canonical_source_metadata_and_only_two_real_name_collisions(self):
        self.assertEqual(len(self.skills), 78)
        self.assertEqual(self.imported["skill_count"], 78)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["revision"], "19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9")
        self.assertEqual(self.imported["namespaces"], {
            "performance-optimization": "gamedev-performance-optimization",
            "godot-export": "gamedev-godot-export",
        })
        self.assertEqual(len({s["source_path"] for s in self.skills}), 78)
        for skill in self.skills:
            self.assertEqual(skill["id"], skill["canonical_id"])
            self.assertEqual(skill["name"], skill["id"])
            self.assertEqual(skill["path"], f"skills/{skill['id']}")
            self.assertEqual(skill["category"], "game-development")
            self.assertEqual(skill["risk"], "unknown")
            self.assertEqual(skill["license"], "Apache-2.0")
            self.assertEqual(skill["author"], "Abhishek Barali and contributors")
            self.assertEqual(skill["source_revision"], self.imported["revision"])
            self.assertIn(self.imported["revision"], skill["source"])
            self.assertIn(self.imported["revision"], skill["license_source"])
            self.assertIn("gamedev", skill["tags"])
        for filename in ("data/catalog.json", "data/skills_index.json"):
            data = json.loads((ROOT / filename).read_text())
            rows = data["skills"] if isinstance(data, dict) else data
            matches = {s["id"]: s for s in rows if s.get("source_repo") == self.imported["source_repo"]}
            self.assertEqual(len(matches), 78)
            for skill in self.skills:
                for key in ("canonical_id", "source_path", "source_revision", "description", "license"):
                    self.assertEqual(matches[skill["id"]][key], skill[key])

    def test_complete_source_inventory_hashes_modes_and_reversible_changes(self):
        self.assertEqual(len(self.records), 582)
        expected = {r["path"] for r in self.records}
        self.assertEqual(len(expected), len(self.records))
        actual = {p.relative_to(ROOT).as_posix() for s in self.skills
                  for p in (ROOT / s["path"]).rglob("*") if p.is_file()}
        self.assertEqual(actual, expected)
        executable = []
        for record in self.records:
            path = ROOT / record["path"]
            self.assertFalse(path.is_symlink())
            self.assertEqual(bool(path.stat().st_mode & 0o111), record["executable"], str(path))
            content = path.read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"], str(path))
            if record["appended_notes"]:
                notes = self.imported["skill_notes"].encode()
                self.assertTrue(content.endswith(notes))
                content = content[:-len(notes)]
            for change in reversed(self.imported["replacements"].get(record["path"], [])):
                self.assertIn(change["after"].encode(), content)
                content = content.replace(change["after"].encode(), change["before"].encode())
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["source_sha256"], str(path))
            self.assertEqual(hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest(),
                             record["source_git_blob"], str(path))
            if record["executable"]:
                executable.append(path.name)
        self.assertEqual(sorted(executable), ["asset_report.py"] * 2 + ["build_preview_sheet.py"] * 2)
        for skill in self.skills:
            pack = ROOT / skill["path"]
            self.assertIn("Apache License", (pack / "LICENSE").read_text())
            notice = (pack / "NOTICE").read_text()
            self.assertIn("Copyright 2026 Abhishek Barali", notice)
            self.assertIn("trademarks", notice)
        fonts = [r for r in self.records if r["source_path"].endswith("licenses/Go-Fonts.txt")]
        self.assertEqual(len(fonts), 2)
        self.assertEqual(len({r["sha256"] for r in fonts}), 1)

    def test_router_is_standalone_without_extra_index_entries(self):
        router = ROOT / "skills/router"
        companions = sorted((router / "bundled/skills").rglob("RUNBOOK.md"))
        self.assertEqual(len(companions), 77)
        self.assertFalse(list((router / "bundled").rglob("SKILL.md")))
        for skill in self.skills:
            if skill["id"] == "router":
                continue
            source = Path(skill["source_path"])
            companion = router / "bundled" / source.with_name("RUNBOOK.md")
            self.assertIn(companion, companions)
            paths = [r for r in self.records if r["path"].startswith(skill["path"] + "/")
                     and r["source_path"] not in ("LICENSE", "NOTICE")]
            for record in paths:
                relative = Path(record["source_path"])
                if relative.name == "SKILL.md":
                    relative = relative.with_name("RUNBOOK.md")
                self.assertTrue((router / "bundled" / relative).is_file(), record["source_path"])
        self.assertTrue((router / "bundled/docs/VERSION-SUPPORT.md").is_file())
        text = (router / "SKILL.md").read_text()
        self.assertIn("`bundled/skills/<category>/<name>/RUNBOOK.md`", text)
        self.assertIn("it is bundled with this router", text)
        self.assertFalse(any("/bundled/" in s["path"] for s in self.index))
        scanned = {s["id"] for s in VAS.scan_skills_locally()}
        self.assertEqual(scanned, {s["id"] for s in self.index})

    def test_local_references_helpers_and_dependencies_are_preserved_without_execution(self):
        for skill in self.skills:
            pack = ROOT / skill["path"]
            text = (pack / "SKILL.md").read_text()
            self.assertIn("Installing\na skill only copies/links", text)
            self.assertIn("never runs bundled", text)
            for document in pack.rglob("*.md"):
                content = re.sub(r"```.*?```", "", document.read_text(), flags=re.S)
                for target in re.findall(r"\]\(([^)\s]+)\)", content):
                    if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|/)", target, re.I):
                        continue
                    resolved = (document.parent / unquote(target.split("#")[0].split("?")[0])).resolve()
                    self.assertTrue(resolved.exists(), f"{document}: {target}")
                    self.assertTrue(resolved.is_relative_to(pack), f"{document}: {target}")
            for script in pack.rglob("*.py"):
                ast.parse(script.read_text())
        requirements = (ROOT / "skills/create-game-assets/scripts/requirements.txt").read_text()
        self.assertIn("Pillow>=10,<14", requirements)
        economy = ROOT / "skills/roblox-simulator-economy/scripts"
        self.assertTrue((economy / "economy_math.luau").is_file())
        self.assertTrue((economy / "balance.luau").is_file())
        self.assertTrue((ROOT / "skills/ebitengine-game/assets/starter/world/world_test.go").is_file())
        self.assertTrue((ROOT / "skills/ebitengine-game/scripts/new_game.py").is_file())

    def test_all_new_normalized_workflows_are_distinct(self):
        def body(text):
            text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
            return " ".join(text.partition("\n## VAS installation notes")[0].split())
        identifiers = {s["id"] for s in self.skills}
        old = {body((ROOT / s["path"] / "SKILL.md").read_text(errors="replace"))
               for s in self.index if s["id"] not in identifiers}
        new = [body((ROOT / s["path"] / "SKILL.md").read_text()) for s in self.skills]
        self.assertEqual(len(set(new)), 78)
        self.assertFalse(set(new).intersection(old))

    def test_each_payload_installs_in_isolation_and_router_and_namespaces_cover_all_agents(self):
        cases = [(s, mode, list(self.targets)[i % 7]) for i, s in enumerate(self.skills)
                 for mode in ("copy", "link")]
        cases += [(s, mode, target) for s in self.skills
                  if s["id"] in {"router", "gamedev-performance-optimization", "gamedev-godot-export"}
                  for mode in ("copy", "link") for target in self.targets]
        for skill, mode, target in cases:
            with self.subTest(skill=skill["id"], mode=mode, target=target), tempfile.TemporaryDirectory(prefix="vas-gamedev-") as temp:
                project = Path(temp)
                result = cli("install", skill["id"], "--target", target, "--mode", mode, cwd=project)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                destination = project / self.targets[target]
                installed = destination / skill["id"]
                self.assertEqual(installed.is_symlink(), mode == "link")
                records = [r for r in self.records if r["path"].startswith(skill["path"] + "/")]
                self.assertEqual({p.relative_to(installed).as_posix() for p in installed.rglob("*") if p.is_file()},
                                 {str(Path(r["path"]).relative_to(skill["path"])) for r in records})
                for record in records:
                    file = installed / Path(record["path"]).relative_to(skill["path"])
                    self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), record["sha256"])
                    self.assertEqual(bool(file.stat().st_mode & 0o111), record["executable"])
                status = cli("status", "--target", target, cwd=project)
                self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
                self.assertIn("Total installed: 1", status.stdout)
                removed = cli("uninstall", skill["id"], "--target", target, cwd=project)
                self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                self.assertFalse(installed.exists())
                self.assertEqual(json.loads((destination / ".vas-manifest.json").read_text()), {})

    def test_namespaced_workflows_coexist_with_both_existing_skills(self):
        identifiers = ["performance-optimization", "blender-skills/godot-export",
                       "gamedev-performance-optimization", "gamedev-godot-export"]
        with tempfile.TemporaryDirectory(prefix="vas-gamedev-coexist-") as temp:
            project = Path(temp)
            for identifier in identifiers:
                result = cli("install", identifier, "--target", "cursor", "--mode", "copy", cwd=project)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            destination = project / ".cursor/skills"
            ledger = json.loads((destination / ".vas-manifest.json").read_text())
            self.assertEqual(set(ledger), set(identifiers))
            self.assertEqual(len({entry["target_name"] for entry in ledger.values()}), 4)
            old = {key: ledger[key] for key in identifiers[:2]}
            for identifier in identifiers[2:]:
                result = cli("uninstall", identifier, "--target", "cursor", cwd=project)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads((destination / ".vas-manifest.json").read_text()), old)
            self.assertTrue((destination / "performance-optimization/SKILL.md").is_file())
            self.assertTrue((destination / "godot-export/SKILL.md").is_file())

    def test_every_manifest_inventory_and_quick_receipt_works_with_cli(self):
        manifests = PAGES.installation_manifests(ROOT)
        for skill in self.skills:
            manifest = manifests[skill["id"]]
            self.assertEqual(manifest["skill_id"], skill["id"])
            self.assertEqual(manifest["target_name"], skill["id"])
            self.assertNotEqual(manifest["revision"], self.imported["revision"])
            records = {str(Path(r["path"]).relative_to(skill["path"])): r
                       for r in self.records if r["path"].startswith(skill["path"] + "/")}
            self.assertEqual({f["path"] for f in manifest["files"]}, set(records))
            with tempfile.TemporaryDirectory(prefix="vas-gamedev-receipt-") as temp:
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
                ledger_path = destination / receipt["filename"]
                ledger = {receipt["key"]: {**receipt["entry"], "installed_at": int(time.time())},
                          "keep": {"target_name": "keep", "mode": "copy"}}
                ledger_path.write_text(json.dumps(ledger))
                for action in ("status", "uninstall"):
                    args = [action] + ([skill["id"]] if action == "uninstall" else [])
                    result = cli(*args, "--target", "cursor", cwd=project)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn(skill["id"], result.stdout)
                self.assertEqual(json.loads(ledger_path.read_text()), {"keep": ledger["keep"]})


if __name__ == "__main__":
    unittest.main()
