from hashlib import sha256
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_pages", ROOT / "scripts/build_pages.py")
PAGES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PAGES)


class PagesBuildTests(unittest.TestCase):
    def fixture(self, root):
        (root / "docs/assets").mkdir(parents=True)
        (root / "docs/index.html").write_text(
            '<html data-skill-base=".."><link rel="stylesheet" href="./catalog.css">'
            '<script src="./i18n.js" defer></script>'
            '<script src="./motion.js" defer></script><script src="catalog.js" defer></script>'
            '<a href="../README.md">Read</a></html>'
        )
        (root / "docs/catalog.css").write_text("body { margin: 0; }")
        (root / "docs/i18n.js").write_text("window.VASI18n = {};")
        (root / "docs/motion.js").write_text("window.motionReady = true;")
        (root / "docs/catalog.js").write_text("window.catalogReady = true;")
        (root / "docs/assets/test.svg").write_text("<svg/>")
        for name in ("README.md", "README_EN.md", "CATALOG.md", "LICENSE"):
            (root / name).write_text(name)
        skill = root / "skills/blender-skills/example"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("Example")
        (skill / "reference.md").write_text("Reference")
        youtube = root / "skills/youtube-agent-skill/yt-chapters"
        (youtube / "shared-tools").mkdir(parents=True)
        (youtube / "templates").mkdir()
        (youtube / "SKILL.md").write_text("YouTube chapters")
        (youtube / "LICENSE").write_text("MIT License")
        (youtube / "shared-tools/deadair.py").write_text("def load(path): return []")
        (youtube / "templates/voice.md").write_text("Voice template")

    def test_artifact_contains_runbooks_references_assets_and_correct_base(self):
        with tempfile.TemporaryDirectory(prefix="vie-pages-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root)
            html = (output / "index.html").read_text()
            self.assertIn('data-skill-base="."', html)
            self.assertIn('href="./README.md"', html)
            self.assertIn('data-skill-base=".."', (root / "docs/index.html").read_text())
            for path in ("README.md", "README_EN.md", "CATALOG.md", "LICENSE",
                         "assets/test.svg", "skills/blender-skills/example/SKILL.md",
                         "skills/blender-skills/example/reference.md", ".nojekyll",
                         "skills/youtube-agent-skill/yt-chapters/SKILL.md",
                         "skills/youtube-agent-skill/yt-chapters/LICENSE",
                         "skills/youtube-agent-skill/yt-chapters/shared-tools/deadair.py",
                         "skills/youtube-agent-skill/yt-chapters/templates/voice.md"):
                self.assertTrue((output / path).is_file(), path)
            (output / "stale.txt").touch()
            PAGES.build(root)
            self.assertFalse((output / "stale.txt").exists())

    def test_asset_versions_change_only_when_their_content_changes(self):
        with tempfile.TemporaryDirectory(prefix="vie-pages-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root)
            original = (output / "index.html").read_text()
            for name, prefix in (("catalog.css", "./"), ("i18n.js", "./"),
                                 ("motion.js", "./"), ("catalog.js", "")):
                version = sha256((root / "docs" / name).read_bytes()).hexdigest()[:12]
                self.assertIn(f'"{prefix}{name}?v={version}"', original)
                self.assertIn(f'"{prefix}{name}"', (root / "docs/index.html").read_text())
            PAGES.build(root)
            self.assertEqual(original, (output / "index.html").read_text())
            (root / "docs/catalog.css").write_text("body { margin: 1px; }")
            PAGES.build(root)
            updated = (output / "index.html").read_text()
            self.assertNotEqual(original, updated)
            script_version = sha256((root / "docs/motion.js").read_bytes()).hexdigest()[:12]
            self.assertIn(f'"./motion.js?v={script_version}"', updated)

    def test_symlinks_and_missing_marker_fail_without_removing_existing_artifact(self):
        with tempfile.TemporaryDirectory(prefix="vie-pages-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root)
            link = root / "skills/linked"
            link.symlink_to(root / "README.md")
            with self.assertRaisesRegex(ValueError, "symlinks"):
                PAGES.build(root)
            self.assertTrue((output / "index.html").is_file())
            link.unlink()
            (root / "docs/index.html").write_text("<html/>")
            with self.assertRaisesRegex(ValueError, "skill-root"):
                PAGES.build(root)
            self.assertTrue((output / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
