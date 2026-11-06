#!/usr/bin/env python3
"""Run the dependency-free Vercel UI preflight; require a real browser."""

import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main():
    node = shutil.which("node")
    if not node:
        print("Node.js is required for the Vercel UI preflight.", file=sys.stderr)
        return 1
    commands = [
        [node, "--test", "tests/pages.test.cjs", "tests/ui-contract.test.cjs"],
        *([
            sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", pattern,
        ] for pattern in ("test_pages_build.py", "test_blog_pages.py", "test_pages_layout.py")),
    ]
    environment = dict(os.environ, VAS_REQUIRE_BROWSER="1")
    for command in commands:
        print("Checking: " + " ".join(command[1:]), flush=True)
        try:
            result = subprocess.run(command, cwd=ROOT, env=environment, timeout=300)
        except subprocess.TimeoutExpired:
            print("Vercel UI preflight timed out; do not publish this candidate.", file=sys.stderr)
            return 1
        if result.returncode:
            return result.returncode
    print("Vercel UI preflight passed. Review the manual checks before publishing UI changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
