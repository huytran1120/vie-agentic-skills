"""Exercise CLI ownership and receipt handling in disposable local projects."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ".vas-manifest.json"


class CliSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="vas-cli-safety-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.catalog = self.root / "catalog"
        self.catalog.mkdir()
        self.cli = self.catalog / "vas.py"
        shutil.copy2(ROOT / "vas.py", self.cli)
        self.project = self.root / "project"
        self.project.mkdir()
        self.home = self.root / "home"
        self.home.mkdir()
        self.environment = {**os.environ, "HOME": str(self.home), "USERPROFILE": str(self.home)}

        skills = []
        for skill_id in ("pdf", "docx", "lookdev", "blender-skills/lookdev"):
            directory = self.catalog / "skills" / skill_id
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text(
                "---\nname: " + skill_id.rsplit("/", 1)[-1]
                + "\ndescription: Local fixture\ncategory: general\ntags: [fixture]\n"
                + "---\n# " + skill_id + "\n\nFixture body: " + skill_id + "\n",
                encoding="utf-8",
            )
            skills.append({
                "id": skill_id, "path": "skills/" + skill_id,
                "name": skill_id, "description": "Local fixture",
                "category": "general", "tags": ["fixture"],
            })
        (self.catalog / "skills_index.json").write_text(json.dumps(skills), encoding="utf-8")
        data = self.catalog / "data"
        data.mkdir()
        (data / "aliases.json").write_text(
            json.dumps({"aliases": {"legacy-pdf": "pdf"}}), encoding="utf-8",
        )

    def run_cli(self, *arguments, cwd=None):
        return subprocess.run(
            [sys.executable, "-B", str(self.cli), *arguments],
            cwd=cwd or self.project, env=self.environment,
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_refused(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def receipts(self, destination):
        return json.loads((destination / MANIFEST).read_text(encoding="utf-8"))

    def test_install_preserves_unmanaged_skill_directory(self):
        for mode in ("link", "copy"):
            with self.subTest(mode=mode):
                destination = self.project / mode / ".codex/skills"
                existing = destination / "pdf"
                existing.mkdir(parents=True)
                (existing / "SKILL.md").write_text("My independent PDF skill", encoding="utf-8")
                (existing / "notes.txt").write_text("Keep my notes", encoding="utf-8")

                result = self.run_cli("install", "pdf", "--mode", mode, "--dest", str(destination))

                self.assert_refused(result)
                self.assertFalse(existing.is_symlink())
                self.assertEqual((existing / "SKILL.md").read_text(), "My independent PDF skill")
                self.assertEqual((existing / "notes.txt").read_text(), "Keep my notes")

    def test_uninstall_preserves_unmanaged_skill_directory(self):
        destination = self.project / ".codex/skills"
        existing = destination / "pdf"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("My independent PDF skill", encoding="utf-8")
        (existing / "notes.txt").write_text("Keep my notes", encoding="utf-8")

        result = self.run_cli("uninstall", "pdf", "--dest", str(destination))

        self.assert_refused(result)
        self.assertEqual((existing / "SKILL.md").read_text(), "My independent PDF skill")
        self.assertEqual((existing / "notes.txt").read_text(), "Keep my notes")

    def test_managed_link_and_copy_reinstall_and_uninstall(self):
        for first_mode in ("link", "copy"):
            for second_mode in ("link", "copy"):
                with self.subTest(first=first_mode, second=second_mode):
                    destination = self.project / (first_mode + "-" + second_mode) / "skills"
                    self.assert_success(self.run_cli(
                        "install", "pdf", "docx", "--mode", first_mode, "--dest", str(destination),
                    ))
                    other_receipt = self.receipts(destination)["docx"]
                    source = self.catalog / "skills/pdf/SKILL.md"
                    source_before = source.read_bytes()

                    self.assert_success(self.run_cli(
                        "install", "legacy-pdf", "--mode", second_mode, "--dest", str(destination),
                    ))
                    self.assertEqual((destination / "pdf").is_symlink(), second_mode == "link")
                    self.assertEqual((destination / "pdf/SKILL.md").read_bytes(), source_before)
                    self.assertEqual(self.receipts(destination)["pdf"]["mode"], second_mode)
                    self.assertEqual(self.receipts(destination)["docx"], other_receipt)

                    self.assert_success(self.run_cli("uninstall", "legacy-pdf", "--dest", str(destination)))
                    self.assertFalse((destination / "pdf").exists())
                    self.assertFalse((destination / "pdf").is_symlink())
                    self.assertEqual(source.read_bytes(), source_before)
                    self.assertTrue((destination / "docx/SKILL.md").is_file())
                    self.assertEqual(self.receipts(destination), {"docx": other_receipt})

    def test_duplicate_basename_does_not_replace_another_skill(self):
        pairs = (("lookdev", "blender-skills/lookdev"), ("blender-skills/lookdev", "lookdev"))
        for mode in ("link", "copy"):
            for number, (owner, conflicting) in enumerate(pairs):
                with self.subTest(mode=mode, owner=owner):
                    destination = self.project / (mode + str(number)) / "skills"
                    self.assert_success(self.run_cli("install", owner, "--mode", mode, "--dest", str(destination)))
                    before = (destination / "lookdev/SKILL.md").read_bytes()
                    receipt_before = self.receipts(destination)

                    result = self.run_cli("install", conflicting, "--mode", mode, "--dest", str(destination))

                    self.assert_refused(result)
                    self.assertEqual((destination / "lookdev/SKILL.md").read_bytes(), before)
                    self.assertEqual(self.receipts(destination), receipt_before)
                    # A rejected second ID must not be allowed to uninstall the first owner either.
                    result = self.run_cli("uninstall", conflicting, "--dest", str(destination))
                    self.assert_refused(result)
                    self.assertEqual((destination / "lookdev/SKILL.md").read_bytes(), before)
                    self.assertEqual(self.receipts(destination), receipt_before)

    def test_malformed_receipts_fail_without_replacing_or_removing_data(self):
        invalid_receipts = {
            "invalid-json": b"{incomplete",
            "array": b"[]",
            "null": b"null",
            "entry-array": b'{"pdf": []}',
            "entry-string": b'{"pdf": "not a receipt"}',
            "target-number": b'{"pdf": {"target_name": 123, "mode": "copy"}}',
            "target-traversal": b'{"pdf": {"target_name": "nested/../pdf", "mode": "copy"}}',
            "target-backslash": b'{"pdf": {"target_name": "nested\\\\pdf", "mode": "copy"}}',
            "target-empty": b'{"pdf": {"target_name": "", "mode": "copy"}}',
            "target-dot": b'{"pdf": {"target_name": ".", "mode": "copy"}}',
            "bad-unrelated-entry": b'{"pdf": {"target_name": "pdf", "mode": "copy"}, '
                                   b'"other": {"target_name": "nested/../other", "mode": "copy"}}',
        }
        for command in ("install", "uninstall"):
            for name, payload in invalid_receipts.items():
                with self.subTest(command=command, receipt=name):
                    destination = self.project / command / name / "skills"
                    existing = destination / "pdf"
                    existing.mkdir(parents=True)
                    (existing / "SKILL.md").write_text("Preserve this local skill", encoding="utf-8")
                    (destination / MANIFEST).write_bytes(payload)

                    result = self.run_cli(command, "pdf", "--dest", str(destination))

                    self.assert_refused(result)
                    self.assertEqual((existing / "SKILL.md").read_text(), "Preserve this local skill")
                    self.assertEqual((destination / MANIFEST).read_bytes(), payload)

    def test_symlinked_receipt_is_refused_without_changing_its_target(self):
        for command in ("install", "uninstall", "status"):
            with self.subTest(command=command):
                destination = self.project / command / "skills"
                existing = destination / "pdf"
                existing.mkdir(parents=True)
                (existing / "SKILL.md").write_text("Keep this local skill", encoding="utf-8")
                outside_receipt = self.root / (command + "-settings.json")
                payload = json.dumps({"pdf": {"mode": "copy", "target_name": "pdf"}}).encode()
                outside_receipt.write_bytes(payload)
                (destination / MANIFEST).symlink_to(outside_receipt)
                arguments = [command]
                if command != "status":
                    arguments.append("pdf")

                result = self.run_cli(*arguments, "--dest", str(destination))

                self.assert_refused(result)
                self.assertEqual((existing / "SKILL.md").read_text(), "Keep this local skill")
                self.assertEqual(outside_receipt.read_bytes(), payload)
                self.assertTrue((destination / MANIFEST).is_symlink())

    def test_all_global_is_rejected_before_creating_agent_directories(self):
        for command in ("install", "uninstall", "status"):
            with self.subTest(command=command):
                project = self.project / command
                project.mkdir()
                arguments = [command]
                if command != "status":
                    arguments.append("pdf")
                result = self.run_cli(*arguments, "--target", "all", "--global", cwd=project)

                self.assert_refused(result)
                self.assertEqual(list(project.iterdir()), [])
                self.assertEqual(list(self.home.iterdir()), [])

    def test_agent_chat_copy_receipt_remains_manageable(self):
        destination = self.project / ".codex/skills"
        destination.mkdir(parents=True)
        shutil.copytree(self.catalog / "skills/pdf", destination / "pdf")
        receipt = {
            "pdf": {
                "mode": "copy", "target_name": "pdf", "category": "general",
                "source": "https://github.com/huytran1120/vie-agentic-skills/tree/"
                          + "1" * 40 + "/skills/pdf",
                "catalog_revision": "1" * 40, "installed_at": 1700000000,
            },
        }
        (destination / MANIFEST).write_text(json.dumps(receipt), encoding="utf-8")

        self.assert_success(self.run_cli("status", "--dest", str(destination)))
        self.assert_success(self.run_cli("install", "pdf", "--mode", "link", "--dest", str(destination)))
        self.assertTrue((destination / "pdf").is_symlink())
        source_before = (self.catalog / "skills/pdf/SKILL.md").read_bytes()
        self.assert_success(self.run_cli("uninstall", "pdf", "--dest", str(destination)))
        self.assertFalse((destination / "pdf").is_symlink())
        self.assertEqual((self.catalog / "skills/pdf/SKILL.md").read_bytes(), source_before)
        self.assertEqual(self.receipts(destination), {})

    def test_managed_broken_skill_symlink_can_be_uninstalled(self):
        destination = self.project / ".codex/skills"
        self.assert_success(self.run_cli("install", "pdf", "--mode", "link", "--dest", str(destination)))
        source = self.catalog / "skills/pdf"
        relocated = self.catalog / "skills/pdf-relocated"
        source.rename(relocated)
        self.assertTrue((destination / "pdf").is_symlink())
        self.assertFalse((destination / "pdf").exists())

        self.assert_success(self.run_cli("uninstall", "pdf", "--dest", str(destination)))

        self.assertFalse((destination / "pdf").is_symlink())
        self.assertTrue((relocated / "SKILL.md").is_file())
        self.assertEqual(self.receipts(destination), {})


if __name__ == "__main__":
    unittest.main()
