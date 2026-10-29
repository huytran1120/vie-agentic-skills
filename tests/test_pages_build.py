import functools
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import time
import unittest
from urllib.parse import urlparse
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
REVISION = "a" * 40
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
        (youtube / "shared-tools/deadair.py").chmod(0o755)
        (youtube / "templates/a (binary)'s.bin").write_bytes(bytes(range(256)))
        (root / "skills_index.json").write_text(json.dumps([
            {"id": "blender-skills/example", "path": "skills/blender-skills/example",
             "category": "blender", "license": "MIT"},
            {"id": "youtube-agent-skill/yt-chapters",
             "path": "skills/youtube-agent-skill/yt-chapters", "category": "content",
             "source_repo": "Jakeschincariol/youtube-agent-skill", "license": "MIT"},
        ]))

    def test_artifact_contains_runbooks_references_assets_and_correct_base(self):
        with tempfile.TemporaryDirectory(prefix="vie-pages-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root, revision=REVISION)
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
            PAGES.build(root, revision=REVISION)
            self.assertFalse((output / "stale.txt").exists())

    def test_asset_versions_change_only_when_their_content_changes(self):
        with tempfile.TemporaryDirectory(prefix="vie-pages-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root, revision=REVISION)
            original = (output / "index.html").read_text()
            for name, prefix in (("catalog.css", "./"), ("i18n.js", "./"),
                                 ("motion.js", "./"), ("catalog.js", "")):
                version = sha256((root / "docs" / name).read_bytes()).hexdigest()[:12]
                self.assertIn(f'"{prefix}{name}?v={version}"', original)
                self.assertIn(f'"{prefix}{name}"', (root / "docs/index.html").read_text())
            PAGES.build(root, revision=REVISION)
            self.assertEqual(original, (output / "index.html").read_text())
            (root / "docs/catalog.css").write_text("body { margin: 1px; }")
            PAGES.build(root, revision=REVISION)
            updated = (output / "index.html").read_text()
            self.assertNotEqual(original, updated)
            script_version = sha256((root / "docs/motion.js").read_bytes()).hexdigest()[:12]
            self.assertIn(f'"./motion.js?v={script_version}"', updated)

    def test_symlinks_and_missing_marker_fail_without_removing_existing_artifact(self):
        with tempfile.TemporaryDirectory(prefix="vie-pages-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root, revision=REVISION)
            link = root / "skills/linked"
            link.symlink_to(root / "README.md")
            with self.assertRaisesRegex(ValueError, "symlinks"):
                PAGES.build(root, revision=REVISION)
            self.assertTrue((output / "index.html").is_file())
            link.unlink()
            (root / "docs/index.html").write_text("<html/>")
            with self.assertRaisesRegex(ValueError, "skill-root"):
                PAGES.build(root, revision=REVISION)
            self.assertTrue((output / "index.html").is_file())

    def test_manifests_inventory_complete_files_and_immutable_encoded_urls(self):
        with tempfile.TemporaryDirectory(prefix="vie-manifest-") as temp:
            root = Path(temp)
            self.fixture(root)
            skill = root / "skills/youtube-agent-skill/yt-chapters"
            (skill / "__pycache__").mkdir()
            (skill / "__pycache__/cached.pyc").write_bytes(b"cache")
            (skill / ".DS_Store").touch()
            output = PAGES.build(root, revision=REVISION)
            manifest = json.loads((output / "install-manifests/youtube-agent-skill/yt-chapters.json").read_text())
            self.assertTrue(manifest["available"])
            self.assertEqual(manifest["revision"], REVISION)
            self.assertEqual(manifest["target_name"], "yt-chapters")
            self.assertEqual(manifest["provenance"]["license"], "MIT")
            self.assertEqual(manifest["receipt"]["key"], manifest["skill_id"])
            self.assertEqual(manifest["receipt"]["entry"]["mode"], "copy")
            files = {file["path"]: file for file in manifest["files"]}
            self.assertEqual(set(files), {"SKILL.md", "LICENSE", "shared-tools/deadair.py",
                                          "templates/voice.md", "templates/a (binary)'s.bin"})
            for name, file in files.items():
                data = (skill / name).read_bytes()
                self.assertEqual(file["bytes"], len(data))
                self.assertEqual(file["sha256"], sha256(data).hexdigest())
                self.assertIn(f"/{REVISION}/skills/youtube-agent-skill/yt-chapters/", file["url"])
                self.assertEqual((output / "skills/youtube-agent-skill/yt-chapters" / name).read_bytes(), data)
            self.assertIn("a%20%28binary%29%27s.bin", files["templates/a (binary)'s.bin"]["url"])
            self.assertTrue(files["shared-tools/deadair.py"]["executable"])
            self.assertFalse(files["templates/voice.md"]["executable"])

    def test_invalid_identity_and_source_paths_preserve_previous_artifact(self):
        with tempfile.TemporaryDirectory(prefix="vie-manifest-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root, revision=REVISION)
            index = json.loads((root / "skills_index.json").read_text())
            for field in ("id", "path"):
                for bad in ("../outside", "/absolute", "skills/../outside", "a\\b", "a//b", "C:/outside", "a\nb"):
                    changed = [dict(index[0], **{field: bad})]
                    (root / "skills_index.json").write_text(json.dumps(changed))
                    with self.assertRaises((ValueError, KeyError)):
                        PAGES.build(root, revision=REVISION)
                    self.assertTrue((output / "index.html").is_file())
            (root / "skills_index.json").write_text(json.dumps([index[0], index[0]]))
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                PAGES.build(root, revision=REVISION)
            with self.assertRaisesRegex(ValueError, "commit SHA"):
                PAGES.build(root, revision="main")

    def test_local_unpublished_skills_never_advertise_nonexistent_snapshot_urls(self):
        with tempfile.TemporaryDirectory(prefix="vie-manifest-") as temp:
            root = Path(temp)
            self.fixture(root)
            commands = [
                ["git", "-c", "init.defaultBranch=main", "init", "-q"],
                ["git", "add", "skills", "skills_index.json"],
                ["git", "-c", "user.name=VAS Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qm",
                 "Fixture\n\nCo-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"],
            ]
            for command in commands:
                subprocess.run(command, cwd=root, check=True, capture_output=True)
            self.assertTrue(PAGES.installation_manifests(root)["blender-skills/example"]["available"])
            (root / "skills/blender-skills/example/new.txt").write_text("Not published")
            manifest = PAGES.installation_manifests(root)["blender-skills/example"]
            self.assertFalse(manifest["available"])
            self.assertEqual(manifest["unavailable_reason"], "unpublished_local_changes")
            self.assertTrue(all("url" not in file for file in manifest["files"]))

    def test_every_catalog_skill_has_a_complete_manifest_accepted_by_the_website(self):
        manifests = PAGES.installation_manifests(ROOT, revision=REVISION)
        index = json.loads((ROOT / "skills_index.json").read_text())
        self.assertEqual(set(manifests), {skill["id"] for skill in index})
        for skill in index:
            manifest = manifests[skill["id"]]
            directory = ROOT / skill["path"]
            expected = {
                path.relative_to(directory).as_posix() for path in directory.rglob("*")
                if path.is_file() and not PAGES.EXCLUDED.intersection(path.relative_to(directory).parts)
            }
            self.assertEqual({file["path"] for file in manifest["files"]}, expected, skill["id"])
        self.assertEqual(manifests["lookdev"]["target_name"], manifests["blender-skills/lookdev"]["target_name"])
        validation = subprocess.run(
            ["node", "-e",
             "const c=require('./docs/catalog.js'); let s='';"
             "process.stdin.on('data',d=>s+=d); process.stdin.on('end',()=>{"
             "for(const m of JSON.parse(s)) c.validateInstallManifest(m,{id:m.skill_id,path:m.source_path});"
             "});"],
            cwd=ROOT, input=json.dumps(list(manifests.values())), text=True, capture_output=True,
        )
        self.assertEqual(validation.returncode, 0, validation.stderr)

    def test_http_file_inventory_roundtrip_and_receipt_work_with_existing_cli(self):
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

        with tempfile.TemporaryDirectory(prefix="vie-http-install-") as temp:
            root = Path(temp)
            self.fixture(root)
            output = PAGES.build(root, revision=REVISION)
            server = ThreadingHTTPServer(
                ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(output)),
            )
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                origin = f"http://127.0.0.1:{server.server_port}"
                with urlopen(origin + "/install-manifests/youtube-agent-skill/yt-chapters.json") as response:
                    manifest = json.load(response)
                project = root / "consumer-project"
                staging = project / "staging"

                def download_and_verify():
                    payloads = {}
                    for file in manifest["files"]:
                        source = urlparse(file["url"]).path.split(f"/{REVISION}/", 1)[1]
                        with urlopen(f"{origin}/{source}") as response:
                            data = response.read()
                        if len(data) != file["bytes"] or sha256(data).hexdigest() != file["sha256"]:
                            raise ValueError(f"File checksum mismatch: {file['path']}")
                        payloads[file["path"]] = data
                    for name, data in payloads.items():
                        destination = staging / name
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        destination.write_bytes(data)
                    return payloads

                payloads = download_and_verify()
                destination = project / ".claude/skills"
                destination.mkdir(parents=True)
                shutil.move(str(staging), destination / manifest["target_name"])
                receipt = manifest["receipt"]
                entry = {**receipt["entry"], "installed_at": int(time.time())}
                ledger = {receipt["key"]: entry, "keep": {"target_name": "keep", "mode": "copy"}}
                ledger_path = destination / receipt["filename"]
                ledger_path.write_text(json.dumps(ledger))
                for name, data in payloads.items():
                    self.assertEqual((destination / "yt-chapters" / name).read_bytes(), data)
                # The manifest is a protocol for existing agent tools, not a new installer.
                (output / "skills/youtube-agent-skill/yt-chapters/SKILL.md").write_text("Corrupted response")
                with self.assertRaisesRegex(ValueError, "checksum"):
                    download_and_verify()
                self.assertFalse(staging.exists())
                self.assertEqual((destination / "yt-chapters/SKILL.md").read_bytes(), payloads["SKILL.md"])
                environment = {**os.environ, "HOME": str(project / "home")}
                for action in ("status", "uninstall"):
                    command = ["python3", "-B", str(ROOT / "vas.py"), action]
                    if action == "uninstall":
                        command.append(manifest["skill_id"])
                    command.extend(["--target", "claude", "--dest", str(destination)])
                    result = subprocess.run(command, env=environment, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                    self.assertIn("yt-chapters", result.stdout)
                self.assertFalse((destination / "yt-chapters").exists())
                self.assertEqual(json.loads(ledger_path.read_text()), {"keep": ledger["keep"]})
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
