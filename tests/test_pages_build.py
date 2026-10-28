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
            '<html data-skill-base=".."><a href="../README.md">Read</a></html>'
        )
        (root / "docs/assets/test.svg").write_text("<svg/>")
        for name in ("README.md", "README_EN.md", "CATALOG.md", "LICENSE"):
            (root / name).write_text(name)
        skill = root / "skills/blender-skills/example"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("Example")
        (skill / "reference.md").write_text("Reference")

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
                         "skills/blender-skills/example/reference.md", ".nojekyll"):
                self.assertTrue((output / path).is_file(), path)
            (output / "stale.txt").touch()
            PAGES.build(root)
            self.assertFalse((output / "stale.txt").exists())

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
