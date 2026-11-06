"""Regression coverage for multiline descriptions and receipt-based status."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_local_project import ROOT, VAS, cli


class MetadataStatusTests(unittest.TestCase):
    def test_quoted_multiline_descriptions_fold_and_preserve_following_fields(self):
        fixtures = [
            ("'Write safe,\n  portable shell scripts.'", "Write safe, portable shell scripts."),
            ("'First paragraph.\n\n  Next paragraph.'", "First paragraph.\nNext paragraph."),
            ("'It''s safe\n  and portable.'", "It's safe and portable."),
            ('"Use \\"safe\\" scripts\n  with \\u0111ata."', 'Use "safe" scripts with đata.'),
            ('"Use \\"safe\\"\n  scripts."', 'Use "safe" scripts.'),
            ('"Join a long\\\n  word without a space."', 'Join a longword without a space.'),
            ('"Keep \\n as an escape\n  and \\\\ as a slash."', 'Keep \n as an escape and \\ as a slash.'),
        ]
        with tempfile.TemporaryDirectory(prefix="vas-description-") as temp:
            root = Path(temp)
            runbook = root / "skills/example/SKILL.md"
            runbook.parent.mkdir(parents=True)
            for value, expected in fixtures:
                with self.subTest(value=value):
                    runbook.write_text(f"---\nname: example\ndescription: {value}\ncategory: testing\ntags: [shell]\n---\nBody\n")
                    with patch.object(VAS, "REPO_ROOT", root):
                        metadata = VAS.extract_skill_metadata(runbook, "example", catalog_by_key={}, overrides={})
                    self.assertEqual(metadata["description"], expected)
                    self.assertEqual(metadata["category"], "testing")
                    self.assertEqual(metadata["tags"], ["shell"])

    def test_real_multiline_descriptions_are_searchable_in_both_indexes(self):
        index = VAS.load_index()
        website = json.loads((ROOT / "docs/skills.min.json").read_text())
        for data in (index, website):
            description = next(row["description"] for row in data if row["id"] == "bash-pro")
            self.assertIn("safe, portable, and testable shell", description)
            self.assertIn("scripts.", description)
        result = cli("search", "safe portable testable shell", "--limit", "100")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("bash-pro", result.stdout)

    def test_status_tracks_namespaced_receipts_even_when_the_payload_is_missing(self):
        with tempfile.TemporaryDirectory(prefix="vas-status-") as temp:
            root = Path(temp)
            destination = root / "installed"
            destination.mkdir()
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("Example")
            target = destination / "fixture"
            target.symlink_to(source, target_is_directory=True)
            ledger = destination / ".vas-manifest.json"
            receipt = {"collection/canonical": {"target_name": "fixture", "category": "testing", "mode": "link"}}
            ledger.write_text(json.dumps(receipt))
            for expected in ("installed", "broken-link", "missing"):
                if expected == "broken-link":
                    source.rename(root / "moved-source")
                elif expected == "missing":
                    target.unlink()
                before = ledger.read_bytes()
                result = cli("status", "--target", "codex", "--dest", str(destination))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("collection/canonical", result.stdout)
                self.assertIn(f"[{expected}]", result.stdout)
                self.assertIn("[testing]", result.stdout)
                self.assertNotIn("No skills currently installed", result.stdout)
                self.assertEqual(ledger.read_bytes(), before)

    def test_status_supports_legacy_namespaced_receipts_and_unmanaged_skills(self):
        with tempfile.TemporaryDirectory(prefix="vas-status-legacy-") as temp:
            destination = Path(temp)
            (destination / "fixture").symlink_to(destination / "absent", target_is_directory=True)
            (destination / ".vas-manifest.json").write_text(json.dumps({"collection/fixture": {"mode": "link"}}))
            (destination / "manual").mkdir()
            (destination / "manual/SKILL.md").write_text("Manual skill")
            result = cli("status", "--dest", str(destination))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("collection/fixture", result.stdout)
            self.assertIn("[broken-link]", result.stdout)
            self.assertIn("manual", result.stdout)
            self.assertIn("[installed]", result.stdout)

    def test_shared_agent_target_does_not_alias_codex_or_cline(self):
        self.assertEqual(VAS.resolve_target_dir("workspace"), Path(".agents/skills").resolve())
        self.assertNotIn("OpenCode", VAS.AGENT_TARGET_MAP["codex"][2])
        self.assertNotIn("Roo", VAS.AGENT_TARGET_MAP["cline"][2])


if __name__ == "__main__":
    unittest.main()
