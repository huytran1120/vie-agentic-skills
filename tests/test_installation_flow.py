"""Execute website-generated commands against the real CLI in disposable projects."""

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallationFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("node"):
            if os.environ.get("CI"):
                raise RuntimeError("Node is required for website-to-CLI integration tests")
            raise unittest.SkipTest("Node not installed; website command tests unavailable")
        cls.targets = [
            "antigravity", "codex", "claude", "cursor", "windsurf", "cline", "copilot",
        ]

    def round_trip(self, skill_id, target, scope, mode):
        with tempfile.TemporaryDirectory(prefix="vie-web-install-") as temp:
            root = Path(temp)
            home = root / "home"
            home.mkdir()
            options = {
                "scope": scope, "mode": mode,
                "projectPath": str(root / "project with space's"),
            }
            generated = subprocess.run(
                ["node", "-e",
                 "const c=require(process.argv[2]);"
                 "console.log(JSON.stringify(c.installationPlan(...JSON.parse(process.argv[1]))));",
                 json.dumps([skill_id, target, options]), str(ROOT / "docs/catalog.js")],
                capture_output=True, text=True, timeout=30, check=True,
            )
            plan = json.loads(generated.stdout)
            environment = {**os.environ, "HOME": str(home)}

            def execute(commands):
                output = ""
                for command in commands.splitlines():
                    arguments = shlex.split(command)
                    self.assertEqual(arguments[0], "./vas")
                    result = subprocess.run(
                        [sys.executable, "-B", str(ROOT / "vas.py"), *arguments[1:]],
                        cwd=root, env=environment, capture_output=True, text=True,
                        timeout=30,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    output += result.stdout
                return output

            execute(plan["install"])
            paths = [
                Path(path.replace("~", str(home), 1)) if path.startswith("~/")
                else (root / path if scope == "repository" else Path(path))
                for path in plan["paths"]
            ]
            for path in paths:
                self.assertTrue(path.is_file(), path)
                self.assertEqual(path.parent.is_symlink(), mode == "link")
                manifest = json.loads(
                    (path.parent.parent / ".vas-manifest.json").read_text()
                )
                self.assertEqual(manifest[skill_id]["target_name"], path.parent.name)
            for path in plan["paths"]:
                self.assertIn(path, plan["prompt"])
            self.assertIn(skill_id.rsplit("/", 1)[-1], execute(plan["status"]))
            execute(plan["uninstall"])
            for path in paths:
                self.assertFalse(path.parent.exists(), path.parent)
                manifest = json.loads(
                    (path.parent.parent / ".vas-manifest.json").read_text()
                )
                self.assertNotIn(skill_id, manifest)

    def test_project_and_global_commands_for_every_agent_and_mode(self):
        for target in self.targets:
            for mode in ("link", "copy"):
                for scope in ("project", "global"):
                    with self.subTest(target=target, mode=mode, scope=scope):
                        self.round_trip("code-review", target, scope, mode)

    def test_all_agents_and_namespaced_skills(self):
        for mode in ("link", "copy"):
            for scope in ("repository", "project"):
                with self.subTest(mode=mode, scope=scope):
                    self.round_trip("blender-skills/blender-director", "all", scope, mode)


if __name__ == "__main__":
    unittest.main()
