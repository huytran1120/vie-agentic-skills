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
            if os.environ.get("CI"):
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

    def check_layout(self, reduced_motion):
        with tempfile.TemporaryDirectory(prefix="vas-browser-layout-") as temp:
            command = [
                CHROME, "--headless", "--no-first-run", "--no-default-browser-check",
                f"--user-data-dir={temp}", "--dump-dom", "--window-size=1600,1100",
                "--virtual-time-budget=25000",
            ]
            if reduced_motion:
                command.append("--force-prefers-reduced-motion")
            command.append(
                f"http://127.0.0.1:{self.server.server_port}/tests/pages-layout.html"
                + ("?artifact" if reduced_motion else "")
            )
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr[-3000:])
            match = re.search(
                r'<pre id="layout-result">([\s\S]*?)</pre>', result.stdout
            )
            self.assertIsNotNone(match, result.stderr[-3000:])
            self.assertIn('data-layout-complete="true"', result.stdout)
            report = json.loads(html.unescape(match[1]))
            self.assertEqual(report["errors"], [], json.dumps(report, indent=2))
            self.assertEqual(len(report["measurements"]), 10)
            self.assertEqual({row["language"] for row in report["measurements"]}, {"vi", "en"})

    def test_motion_layout_and_catalog_interactions(self):
        self.check_layout(reduced_motion=False)

    def test_reduced_motion_layout_and_catalog_interactions(self):
        self.check_layout(reduced_motion=True)


if __name__ == "__main__":
    unittest.main()
