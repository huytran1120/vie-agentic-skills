import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

from test_local_project import ROOT


WORKER = """
from pathlib import Path
import sys
import time

catalog, started, loaded, release, *arguments = sys.argv[1:]
sys.path.insert(0, catalog)
import vas

original_load = vas.load_manifest
def paused_load(destination):
    manifest = original_load(destination)
    Path(loaded).touch()
    deadline = time.monotonic() + 20
    while not Path(release).exists():
        if time.monotonic() >= deadline:
            raise TimeoutError("Test did not release the manifest reader")
        time.sleep(0.01)
    return manifest

vas.load_manifest = paused_load
sys.argv = ["vas", *arguments]
Path(started).touch()
vas.main()
"""


class CliConcurrencyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="vas-concurrency-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.catalog = self.root / "catalog"
        self.catalog.mkdir()
        shutil.copy2(ROOT / "vas.py", self.catalog / "vas.py")
        skills = []
        for skill_id in ("pdf", "docx", "xlsx"):
            source = self.catalog / "skills" / skill_id
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text(
                f"---\nname: {skill_id}\ndescription: Concurrency fixture\n---\n",
                encoding="utf-8",
            )
            skills.append({"id": skill_id, "path": f"skills/{skill_id}", "category": "general"})
        (self.catalog / "skills_index.json").write_text(json.dumps(skills), encoding="utf-8")
        self.worker_count = 0

    def run_cli(self, destination, *arguments):
        return subprocess.run(
            [sys.executable, "-B", str(self.catalog / "vas.py"), *arguments,
             "--dest", str(destination)],
            capture_output=True, text=True, timeout=15,
        )

    def stop(self, process):
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=10)

    def start(self, destination, *arguments):
        self.worker_count += 1
        started, loaded, release = [
            self.root / f"worker-{self.worker_count}-{suffix}"
            for suffix in ("started", "loaded", "release")
        ]
        process = subprocess.Popen(
            [sys.executable, "-B", "-c", WORKER, str(self.catalog),
             str(started), str(loaded), str(release), *arguments, "--dest", str(destination)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        self.addCleanup(self.stop, process)
        self.assertTrue(self.wait_for(started), "Worker did not start")
        return process, loaded, release

    def wait_for(self, path, timeout=10):
        deadline = time.monotonic() + timeout
        while not path.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        return path.exists()

    def finish(self, process):
        stdout, stderr = process.communicate(timeout=15)
        self.assertEqual(process.returncode, 0, stdout + stderr)

    def assert_installed(self, destination, expected, mode):
        receipt = json.loads((destination / ".vas-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(receipt), set(expected))
        self.assertEqual(
            {path.name for path in destination.iterdir() if not path.name.startswith(".")},
            set(expected),
        )
        for skill_id in expected:
            self.assertEqual((destination / skill_id).is_symlink(), mode == "link")
            self.assertEqual(
                (destination / skill_id / "SKILL.md").read_bytes(),
                (self.catalog / "skills" / skill_id / "SKILL.md").read_bytes(),
            )

    def overlapping(self, first, second, initial, expected):
        for mode in ("link", "copy"):
            with self.subTest(mode=mode):
                destination = self.root / mode
                if initial:
                    result = self.run_cli(destination, "install", *initial, "--mode", mode)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                first_args = [*first, *(["--mode", mode] if first[0] == "install" else [])]
                second_args = [*second, *(["--mode", mode] if second[0] == "install" else [])]
                writer, writer_loaded, release_writer = self.start(destination, *first_args)
                self.assertTrue(self.wait_for(writer_loaded))
                waiter, waiter_loaded, release_waiter = self.start(destination, *second_args)
                read_before_commit = self.wait_for(waiter_loaded, timeout=0.5)
                release_writer.touch()
                self.finish(writer)
                self.assertTrue(self.wait_for(waiter_loaded))
                release_waiter.touch()
                self.finish(waiter)
                self.assert_installed(destination, expected, mode)
                self.assertFalse(read_before_commit, "Another operation read an uncommitted manifest")

    def test_parallel_installs_keep_both_receipts(self):
        self.overlapping(("install", "pdf"), ("install", "docx"), (), ("pdf", "docx"))

    def test_parallel_uninstalls_do_not_restore_removed_receipts(self):
        self.overlapping(
            ("uninstall", "pdf"), ("uninstall", "docx"), ("pdf", "docx", "xlsx"), ("xlsx",),
        )

    def test_uninstall_waits_for_install_and_keeps_its_receipt(self):
        self.overlapping(
            ("install", "docx"), ("uninstall", "pdf"), ("pdf", "xlsx"), ("docx", "xlsx"),
        )

    def test_install_waits_for_uninstall_without_restoring_its_receipt(self):
        self.overlapping(
            ("uninstall", "pdf"), ("install", "docx"), ("pdf", "xlsx"), ("docx", "xlsx"),
        )

    def test_independent_destinations_do_not_block_each_other(self):
        first = self.root / "first"
        second = self.root / "second"
        writer, loaded, release = self.start(first, "install", "pdf", "--mode", "copy")
        self.assertTrue(self.wait_for(loaded))
        other, other_loaded, other_release = self.start(second, "install", "docx", "--mode", "copy")
        self.assertTrue(self.wait_for(other_loaded))
        other_release.touch()
        self.finish(other)
        self.assertIsNone(writer.poll())
        release.touch()
        self.finish(writer)
        self.assert_installed(first, ("pdf",), "copy")
        self.assert_installed(second, ("docx",), "copy")

    def test_waiter_recovers_when_lock_holder_exits(self):
        destination = self.root / "installed"
        writer, loaded, release = self.start(destination, "install", "pdf", "--mode", "copy")
        self.assertTrue(self.wait_for(loaded))
        waiter, waiter_loaded, waiter_release = self.start(
            destination, "install", "docx", "--mode", "copy",
        )
        read_before_exit = self.wait_for(waiter_loaded, timeout=0.5)
        self.stop(writer)
        self.assertTrue(self.wait_for(waiter_loaded))
        waiter_release.touch()
        self.finish(waiter)
        self.assert_installed(destination, ("docx",), "copy")
        self.assertFalse(read_before_exit)

    def test_lock_file_is_reused_and_cannot_be_owned_by_a_skill(self):
        destination = self.root / "installed"
        result = self.run_cli(destination, "install", "pdf")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        lock = destination / ".vas.lock"
        self.assertTrue(lock.is_file())
        inode = lock.stat().st_ino
        result = self.run_cli(destination, "install", "docx")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(lock.stat().st_ino, inode)
        receipt = destination / ".vas-manifest.json"
        for target_name in (".vas.lock", ".VAS.LOCK", ".vas.lock. "):
            with self.subTest(target_name=target_name):
                receipt.write_text(json.dumps({"pdf": {"mode": "copy", "target_name": target_name}}))
                before = receipt.read_bytes()
                result = self.run_cli(destination, "uninstall", "pdf")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(lock.stat().st_ino, inode)
                self.assertEqual(receipt.read_bytes(), before)

    def test_nonregular_lock_files_fail_without_touching_installations(self):
        outside = self.root / "outside.txt"
        outside.write_text("Preserve outside contents", encoding="utf-8")
        for command in ("install", "uninstall"):
            for kind in ("symlink", "directory"):
                with self.subTest(command=command, kind=kind):
                    destination = self.root / f"{command}-{kind}"
                    shutil.copytree(self.catalog / "skills/pdf", destination / "pdf")
                    ledger = destination / ".vas-manifest.json"
                    ledger.write_text(json.dumps({"pdf": {"mode": "copy", "target_name": "pdf"}}))
                    before = ledger.read_bytes()
                    lock = destination / ".vas.lock"
                    if kind == "symlink":
                        lock.symlink_to(outside)
                    else:
                        lock.mkdir()
                    result = self.run_cli(destination, command, "pdf")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(ledger.read_bytes(), before)
                    self.assertTrue((destination / "pdf/SKILL.md").is_file())
                    self.assertEqual(outside.read_text(), "Preserve outside contents")


if __name__ == "__main__":
    unittest.main()
