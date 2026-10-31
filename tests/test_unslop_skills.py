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


class UIUnslopSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = ROOT / "skills/heydamir-unslop"
        cls.imported = json.loads((ROOT / "data/unslop-import.json").read_text())
        cls.index = json.loads((ROOT / "skills_index.json").read_text())
        cls.skill = next(s for s in cls.index if s["id"] == "heydamir-unslop")

    def test_exact_identity_license_and_distinct_existing_prose_workflow(self):
        expected = {
            "canonical_id": "heydamir-unslop", "name": "heydamir-unslop",
            "path": "skills/heydamir-unslop", "category": "front-end", "risk": "unknown",
            "source_repo": "heydamir/unslop", "source_path": "skills/unslop/SKILL.md",
            "source_revision": "4652254daff586ff4739849395a127b56f7f8cc7",
            "author": "Damir Sokolovsky", "license": "CC-BY-4.0",
        }
        for key, value in expected.items():
            self.assertEqual(self.skill[key], value, key)
        self.assertEqual(self.imported["skill_count"], 1)
        self.assertEqual(self.imported["skipped"], [])
        self.assertEqual(self.imported["namespaces"], {"unslop": "heydamir-unslop"})
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3171)
        old = next(s for s in self.index if s["id"] == "unslop")
        self.assertEqual(old["source_repo"], "MohamedAbdallah-14/unslop")
        self.assertEqual(old["license"], "MIT")
        self.assertIn("prose", (ROOT / old["path"] / "SKILL.md").read_text())
        self.assertEqual([s["id"] for s in self.index if s.get("source_repo") == "heydamir/unslop"],
                         ["heydamir-unslop"])
        self.assertEqual(VAS.resolve_skill_id("heydamir-unslop", {s["id"]: s for s in self.index}),
                         "heydamir-unslop")
        for name in ("data/catalog.json", "data/skills_index.json"):
            data = json.loads((ROOT / name).read_text())
            rows = data["skills"] if isinstance(data, dict) else data
            new = [s for s in rows if s["id"] == self.skill["id"]]
            self.assertEqual(len(new), 1)
            for key in ("canonical_id", "description", "source_repo", "source_path",
                        "source_revision", "license", "author"):
                self.assertEqual(new[0][key], self.skill[key], key)
        license_text = (self.pack / "LICENSE").read_text()
        self.assertIn("Attribution 4.0 International", license_text)
        citation = (self.pack / "CITATION.cff").read_text()
        self.assertIn("Damir", citation)
        self.assertIn("Sokolovsky", citation)
        self.assertIn("CC-BY-4.0", citation)
        self.assertIn("heydamir/unslop", citation)
        credits = json.loads((ROOT / "data/source-credits.json").read_text())
        self.assertIn(self.skill["source_revision"], credits["sections"]["heydamir"][0])
        self.assertIn("CC-BY-4.0", credits["sections"]["heydamir"][0])

    def test_complete_inventory_and_reversible_names_and_helper_diagnostics(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 19)
        expected = {record["path"] for record in records}
        self.assertEqual(len(expected), len(records))
        self.assertEqual({p.relative_to(ROOT).as_posix() for p in self.pack.rglob("*") if p.is_file()},
                         expected)
        for record in records:
            path = ROOT / record["path"]
            content = path.read_bytes()
            self.assertFalse(path.is_symlink())
            self.assertFalse(record["executable"])
            self.assertFalse(path.stat().st_mode & 0o111)
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"], str(path))
            if record.get("generated"):
                self.assertEqual(content.decode(), self.imported["generated_notes"])
                self.assertIsNone(record["source_git_blob"])
                continue
            if record["appended_notes"]:
                notes = self.imported["skill_notes"].encode()
                self.assertTrue(content.endswith(notes))
                content = content[:-len(notes)]
            for change in reversed(self.imported["replacements"].get(record["path"], [])):
                before, after = change["before"].encode(), change["after"].encode()
                self.assertEqual(content.count(after), 1)
                content = content.replace(after, before, 1)
            self.assertEqual(hashlib.sha256(content).hexdigest(), record["source_sha256"], str(path))
            self.assertEqual(hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest(),
                             record["source_git_blob"], str(path))
        self.assertEqual(len(list((self.pack / "references").glob("*.md"))), 5)
        self.assertEqual(len(list((self.pack / "references/refs").glob("*.webp"))), 5)
        self.assertEqual(len(list((self.pack / "scripts").glob("*.mjs"))), 2)
        self.assertTrue((self.pack / "examples/assets/blob.webp").is_file())
        self.assertTrue((self.pack / "examples/dashboard.html").is_file())
        self.assertTrue((self.pack / "examples/hero.html").is_file())

    def test_standalone_local_links_helpers_and_approval_first_prerequisites(self):
        for document in self.pack.rglob("*.md"):
            content = re.sub(r"```.*?```", "", document.read_text(), flags=re.S)
            for target in re.findall(r"\]\(([^)\s]+)\)", content):
                if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|/)", target, re.I):
                    continue
                resolved = (document.parent / unquote(target.split("#")[0].split("?")[0])).resolve()
                self.assertTrue(resolved.is_relative_to(self.pack))
                self.assertTrue(resolved.is_file(), f"{document}: {target}")
        notes = (self.pack / "SKILL.md").read_text()
        for requirement in ("Damir Sokolovsky", "CC-BY-4.0", "No endorsement",
                            "never executes", "separate authorization", "Playwright", "ffmpeg", "CHROME_PATH"):
            self.assertIn(requirement, notes)
        for script in (self.pack / "scripts").glob("*.mjs"):
            text = script.read_text()
            self.assertNotIn("npx ", text)
            self.assertIn("Obtain approval", text)
            self.assertIn("ADAPTATIONS.md", text)
            self.assertIn('["playwright", "playwright-core"]', text)
            self.assertIn("process.exit(1)", text)
            self.assertIn('from "node:module"', text)
        self.assertIn('execFileSync("ffmpeg"', (self.pack / "scripts/story.mjs").read_text())
        for reference in (self.pack / "references").glob("*.md"):
            self.assertIn("Part of unslop by Damir Sokolovsky", reference.read_text())

    def test_workflow_is_not_a_renamed_or_normalized_catalog_duplicate(self):
        def body(text):
            text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
            return " ".join(text.partition("\n## VAS installation notes")[0].casefold().split())
        new = body((self.pack / "SKILL.md").read_text())
        for skill in self.index:
            if skill["id"] != "heydamir-unslop":
                self.assertNotEqual(new, body((ROOT / skill["path"] / "SKILL.md").read_text(errors="replace")),
                                    skill["id"])

    def test_every_agent_and_mode_installs_all_files_and_preserves_existing_unslop(self):
        targets = {
            "antigravity": ".agents/skills", "codex": ".codex/skills",
            "claude": ".claude/skills", "cursor": ".cursor/skills",
            "windsurf": ".windsurf/skills", "cline": ".cline/skills", "copilot": ".github/skills",
        }
        for agent, folder in targets.items():
            for mode in ("link", "copy"):
                with self.subTest(agent=agent, mode=mode), tempfile.TemporaryDirectory(prefix="vas-ui-unslop-") as temp:
                    project = Path(temp)
                    for identifier in ("unslop", "heydamir-unslop"):
                        result = cli("install", identifier, "--target", agent, "--mode", mode, cwd=project)
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    destination = project / folder
                    installed = destination / "heydamir-unslop"
                    self.assertEqual(installed.is_symlink(), mode == "link")
                    self.assertEqual({p.relative_to(installed).as_posix() for p in installed.rglob("*") if p.is_file()},
                                     {str(Path(r["path"]).relative_to(self.skill["path"])) for r in self.imported["files"]})
                    for record in self.imported["files"]:
                        file = installed / Path(record["path"]).relative_to(self.skill["path"])
                        self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), record["sha256"])
                        self.assertFalse(file.stat().st_mode & 0o111)
                    receipt_path = destination / ".vas-manifest.json"
                    ledger = json.loads(receipt_path.read_text())
                    self.assertEqual(set(ledger), {"unslop", "heydamir-unslop"})
                    self.assertEqual(ledger["heydamir-unslop"]["target_name"], "heydamir-unslop")
                    old = ledger["unslop"]
                    status = cli("status", "--target", agent, cwd=project)
                    self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
                    self.assertIn("Total installed: 2", status.stdout)
                    result = cli("uninstall", "heydamir-unslop", "--target", agent, cwd=project)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(json.loads(receipt_path.read_text()), {"unslop": old})
                    self.assertFalse(installed.exists())
                    self.assertTrue((destination / "unslop/SKILL.md").is_file())

    def test_complete_official_manifest_and_receipt_are_compatible_with_cli(self):
        manifest = PAGES.installation_manifests(ROOT)["heydamir-unslop"]
        self.assertEqual(manifest["skill_id"], "heydamir-unslop")
        self.assertEqual(manifest["target_name"], "heydamir-unslop")
        self.assertNotEqual(manifest["revision"], self.imported["revision"])
        self.assertEqual(manifest["provenance"]["source_repo"], "heydamir/unslop")
        self.assertEqual(manifest["provenance"]["license"], "CC-BY-4.0")
        records = {str(Path(r["path"]).relative_to(self.skill["path"])): r for r in self.imported["files"]}
        self.assertEqual({f["path"] for f in manifest["files"]}, set(records))
        with tempfile.TemporaryDirectory(prefix="vas-ui-unslop-receipt-") as temp:
            project = Path(temp)
            destination = project / ".cursor/skills"
            for file in manifest["files"]:
                content = (self.pack / file["path"]).read_bytes()
                self.assertEqual(file["bytes"], len(content))
                self.assertEqual(file["sha256"], records[file["path"]]["sha256"])
                self.assertFalse(file["executable"])
                if manifest["available"]:
                    self.assertIn("/" + manifest["revision"] + "/skills/heydamir-unslop/", file["url"])
                else:
                    self.assertEqual(manifest["unavailable_reason"], "unpublished_local_changes")
                    self.assertNotIn("url", file)
                target = destination / "heydamir-unslop" / file["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                target.chmod(0o644)
            receipt = manifest["receipt"]
            ledger = {receipt["key"]: {**receipt["entry"], "installed_at": int(time.time())},
                      "keep": {"target_name": "keep", "mode": "copy"}}
            receipt_path = destination / receipt["filename"]
            receipt_path.write_text(json.dumps(ledger))
            for action in ("status", "uninstall"):
                result = cli(action, *([manifest["skill_id"]] if action == "uninstall" else []),
                             "--target", "cursor", cwd=project)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("heydamir-unslop", result.stdout)
            self.assertEqual(json.loads(receipt_path.read_text()), {"keep": ledger["keep"]})
            self.assertFalse((destination / "heydamir-unslop").exists())


if __name__ == "__main__":
    unittest.main()
