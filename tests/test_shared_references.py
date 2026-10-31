"""Shared guides remain available when a skill is installed without the repository."""

from hashlib import sha256
import json
from pathlib import Path
import re
import tempfile
import unittest

from test_local_project import ROOT, cli
from test_pages_build import PAGES, REVISION


SHARED_GUIDES = {
    "using-agent-skills": {"definition-of-done.md": "definition-of-done.md"},
    "test-driven-development": {"testing-patterns.md": "testing-patterns.md"},
    "planning-and-task-breakdown": {"definition-of-done.md": "definition-of-done.md"},
    "incremental-implementation": {"definition-of-done.md": "definition-of-done.md"},
    "frontend-ui-engineering": {"accessibility-checklist.md": "accessibility-checklist.md"},
    "shipping-and-launch": {
        "definition-of-done.md": "definition-of-done.md",
        "security-checklist.md": "security-checklist.md",
        "performance-checklist.md": "performance-checklist.md",
        "accessibility-checklist.md": "accessibility-checklist.md",
    },
    "code-review-and-quality": {
        "security-checklist.md": "security-checklist.md",
        "performance-checklist.md": "performance-checklist.md",
    },
    "security-and-hardening": {"security-checklist.md": "shared-security-checklist.md"},
    "observability-and-instrumentation": {"observability-checklist.md": "shared-observability-checklist.md"},
    "doubt-driven-development": {"orchestration-patterns.md": "orchestration-patterns.md"},
    "performance-optimization": {"performance-checklist.md": "performance-checklist.md"},
}


class SharedReferenceTests(unittest.TestCase):
    def test_copy_install_keeps_every_linked_shared_guide_and_license(self):
        with tempfile.TemporaryDirectory(prefix="vas-shared-reference-") as temp:
            project = Path(temp)
            destination = project / ".codex/skills"
            result = cli("install", *SHARED_GUIDES, "--target", "codex", "--mode", "copy",
                         "--dest", str(destination), cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads((destination / ".vas-manifest.json").read_text())
            self.assertEqual(set(manifest), set(SHARED_GUIDES))
            for skill_id, guides in SHARED_GUIDES.items():
                with self.subTest(skill=skill_id):
                    skill = destination / skill_id
                    self.assertFalse(skill.is_symlink())
                    runbook = (skill / "SKILL.md").read_text()
                    self.assertNotIn("../../references/", runbook)
                    for original, bundled in guides.items():
                        path = Path("references") / bundled
                        self.assertIn(path.as_posix(), runbook)
                        self.assertEqual((skill / path).read_bytes(),
                                         (ROOT / "references" / original).read_bytes())
                    self.assertEqual((skill / "UPSTREAM-LICENSE.txt").read_bytes(),
                                     (ROOT / "skills/using-agent-skills/UPSTREAM-LICENSE.txt").read_bytes())
                    self.assertEqual((skill / "VAS-LICENSE.txt").read_bytes(),
                                     (ROOT / "LICENSE").read_bytes())
                    self.assertTrue((skill / "SHARED-REFERENCES-NOTICE.md").is_file())

    def test_website_installation_inventory_includes_guides_and_notices(self):
        manifests = PAGES.installation_manifests(ROOT, revision=REVISION)
        for skill_id, guides in SHARED_GUIDES.items():
            with self.subTest(skill=skill_id):
                inventory = {record["path"]: record for record in manifests[skill_id]["files"]}
                for original, bundled in guides.items():
                    content = (ROOT / "references" / original).read_bytes()
                    record = inventory[f"references/{bundled}"]
                    self.assertEqual(record["sha256"], sha256(content).hexdigest())
                    self.assertEqual(record["bytes"], len(content))
                    self.assertTrue(record["url"].endswith(f"/{skill_id}/references/{bundled}"))
                for name in ("UPSTREAM-LICENSE.txt", "VAS-LICENSE.txt", "SHARED-REFERENCES-NOTICE.md"):
                    self.assertIn(name, inventory)

    def test_runbooks_do_not_reach_outside_their_payload_for_existing_shared_guides(self):
        # Explicitly unavailable external prerequisites are not local shared guides.
        for runbook in (ROOT / "skills").rglob("SKILL.md"):
            for reference in re.findall(r"\.\./\.\./references/[^`\s)\]\"<>]+", runbook.read_text()):
                self.assertFalse((runbook.parent / reference).is_file(),
                                 f"{runbook}: bundle the shared guide {reference} inside the skill")

    def test_existing_short_checklists_are_preserved(self):
        for skill_id, title in (
            ("security-and-hardening", "# Application security review checklist"),
            ("observability-and-instrumentation", "# Instrumentation acceptance checklist"),
        ):
            with self.subTest(skill=skill_id):
                original = ROOT / "skills" / skill_id / "references" / next(iter(SHARED_GUIDES[skill_id]))
                self.assertTrue(original.read_text().startswith(title))


if __name__ == "__main__":
    unittest.main()
