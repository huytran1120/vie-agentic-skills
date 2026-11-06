"""Check real browser geometry and interactions with the system Chrome/Chromium.

Run: python3 -B -m unittest discover -s tests -p 'test_pages_layout.py'
For Safari/WebKit, serve the repository root and open /tests/pages-layout.html.
Build with python3 scripts/build_pages.py and add ?artifact to test publication
with content-versioned assets rather than potentially cached development assets.
"""

import functools
import html
import importlib.util
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHROME = next(
    (executable for executable in (
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ) if executable and Path(executable).is_file()),
    None,
)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class PagesLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CHROME:
            if os.environ.get("CI") or os.environ.get("VAS_REQUIRE_BROWSER") == "1":
                raise RuntimeError("Chrome or Chromium is required for CI layout tests")
            raise unittest.SkipTest("Chrome/Chromium not installed; browser layout tests unavailable")
        spec = importlib.util.spec_from_file_location("layout_build", ROOT / "scripts/build_pages.py")
        pages = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pages)
        pages.build(ROOT)
        handler = functools.partial(QuietHandler, directory=str(ROOT))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def check_layout(self, reduced_motion, fixture="pages-layout.html", page_count=1):
        with tempfile.TemporaryDirectory(prefix="vas-browser-layout-") as temp:
            command = [
                CHROME, "--headless", "--no-first-run", "--no-default-browser-check",
                "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                f"--user-data-dir={temp}", "--dump-dom", "--window-size=1600,1100",
                "--virtual-time-budget=25000",
            ]
            if reduced_motion:
                command.append("--force-prefers-reduced-motion")
            command.append(
                f"http://127.0.0.1:{self.server.server_port}/tests/{fixture}"
                + ("?artifact" if reduced_motion else "")
            )
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stderr[-3000:])
            match = re.search(
                r'<pre id="layout-result">([\s\S]*?)</pre>', result.stdout
            )
            self.assertIsNotNone(match, result.stderr[-3000:])
            self.assertIn('data-layout-complete="true"', result.stdout)
            report = json.loads(html.unescape(match[1]))
            self.assertEqual(report["errors"], [], json.dumps(report, indent=2))
            contract = json.loads((ROOT / "tests/fixtures/ui-contract.json").read_text())
            self.assertEqual(len(report["measurements"]), len(contract["widths"]) * len(contract["languages"]) * page_count)
            self.assertEqual({row["language"] for row in report["measurements"]}, set(contract["languages"]))
            self.assertEqual({row["width"] for row in report["measurements"]}, set(contract["widths"]))

    def test_blog_layout_and_navigation(self):
        # Count intended repository pages, including staged additions. Untracked
        # drafts in another task must not change this release's expected pages.
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "docs/blog"], cwd=ROOT,
            capture_output=True, text=True, check=True,
        ).stdout.split("\0")
        count = sum(Path(name).name == "index.html" for name in tracked if name)
        self.check_layout(reduced_motion=True, fixture="blog-layout.html", page_count=count)

    def test_motion_layout_and_catalog_interactions(self):
        self.check_layout(reduced_motion=False)

    def test_reduced_motion_layout_and_catalog_interactions(self):
        self.check_layout(reduced_motion=True)


if __name__ == "__main__":
    unittest.main()
