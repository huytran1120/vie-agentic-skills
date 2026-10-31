"""Receipt failures and filesystem boundaries must preserve existing user data."""

import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_local_project import ROOT, cli


SPEC = importlib.util.spec_from_file_location("transaction_vas", ROOT / "vas.py")
VAS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VAS)


class CliTransactionTests(unittest.TestCase):
    def arguments(self, destination, mode="copy"):
        return argparse.Namespace(target="codex", dest=str(destination), is_global=False,
                                  skill_ids=["pdf"], all=False, category=None, tag=None, mode=mode)

    def test_receipt_cannot_traverse_an_intermediate_directory_link(self):
        with tempfile.TemporaryDirectory(prefix="vas-receipt-boundary-") as temporary:
            base = Path(temporary)
            destination = base / "project/skills"
            destination.mkdir(parents=True)
            outside = base / "outside"
            (outside / "anchor").mkdir(parents=True)
            victim = outside / "victim"
            victim.mkdir()
            (victim / "notes.txt").write_text("Keep outside data")
            (destination / "a").symlink_to(outside / "anchor", target_is_directory=True)
            ledger = destination / VAS.MANIFEST_NAME
            before = json.dumps({"pdf": {"target_name": "a/../victim", "mode": "copy"}})
            ledger.write_text(before)

            result = cli("uninstall", "pdf", "--dest", str(destination))

            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual((victim / "notes.txt").read_text(), "Keep outside data")
            self.assertEqual(ledger.read_text(), before)
            self.assertTrue((destination / "a").is_symlink())

    def test_atomic_receipt_write_keeps_previous_bytes_on_failure(self):
        with tempfile.TemporaryDirectory(prefix="vas-receipt-write-") as temporary:
            destination = Path(temporary)
            before = {"pdf": {"target_name": "pdf", "mode": "copy"}}
            VAS.save_manifest(destination, before)
            ledger = destination / VAS.MANIFEST_NAME
            original = ledger.read_bytes()
            with patch.object(VAS.os, "replace", side_effect=OSError("Receipt storage unavailable")):
                with self.assertRaises(OSError):
                    VAS.save_manifest(destination, {})
            self.assertEqual(ledger.read_bytes(), original)
            self.assertEqual(list(destination.iterdir()), [ledger])

    def test_install_restores_old_payload_and_receipt_when_save_fails(self):
        for mode in ("link", "copy"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix="vas-install-rollback-") as temporary:
                destination = Path(temporary)
                self.assertEqual(cli("install", "pdf", "--mode", "copy", "--dest", temporary).returncode, 0)
                marker = destination / "pdf/local-notes.txt"
                marker.write_text("Keep original installation")
                ledger = destination / VAS.MANIFEST_NAME
                before = ledger.read_bytes()
                with patch.object(VAS, "save_manifest", side_effect=OSError("Receipt storage unavailable")), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as result:
                        VAS.cmd_install(self.arguments(destination, mode))
                self.assertEqual(result.exception.code, 1)
                self.assertEqual(marker.read_text(), "Keep original installation")
                self.assertEqual(ledger.read_bytes(), before)
                self.assertEqual({path.name for path in destination.iterdir()}, {"pdf", VAS.MANIFEST_NAME})

    def test_uninstall_restores_payload_when_save_fails(self):
        for mode in ("link", "copy"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix="vas-uninstall-rollback-") as temporary:
                destination = Path(temporary)
                self.assertEqual(cli("install", "pdf", "--mode", mode, "--dest", temporary).returncode, 0)
                payload = (destination / "pdf/SKILL.md").read_bytes()
                ledger = destination / VAS.MANIFEST_NAME
                before = ledger.read_bytes()
                with patch.object(VAS, "save_manifest", side_effect=OSError("Receipt storage unavailable")), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as result:
                        VAS.cmd_uninstall(self.arguments(destination))
                self.assertEqual(result.exception.code, 1)
                self.assertEqual((destination / "pdf/SKILL.md").read_bytes(), payload)
                self.assertEqual((destination / "pdf").is_symlink(), mode == "link")
                self.assertEqual(ledger.read_bytes(), before)
                self.assertEqual({path.name for path in destination.iterdir()}, {"pdf", VAS.MANIFEST_NAME})


if __name__ == "__main__":
    unittest.main()
