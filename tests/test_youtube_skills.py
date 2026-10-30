import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from test_local_project import ROOT, cli


class YouTubeSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = ROOT / "skills/youtube-agent-skill"
        cls.index = json.loads((ROOT / "skills_index.json").read_text())
        cls.skills = [s for s in cls.index if s["id"].startswith("youtube-agent-skill/")]
        cls.manifest = json.loads((ROOT / "data/youtube-import.json").read_text())

    def test_canonical_skills_and_source_metadata_preserve_provenance(self):
        expected = {
            "yt-audit", "yt-chapters", "yt-comment", "yt-edit", "yt-package",
            "yt-plan", "yt-retention", "yt-script", "yt-seo", "yt-shorts", "yt-viral",
        }
        self.assertEqual({s["name"] for s in self.skills}, expected)
        self.assertEqual(len(self.skills), self.manifest["skill_count"])
        self.assertEqual(len(self.index) - len(self.skills), 3082)
        self.assertEqual(self.manifest["source_repo"], "Jakeschincariol/youtube-agent-skill")
        self.assertEqual(self.manifest["revision"], "a2feb2104981a375ffd4f87ee04f4f5344ac43c6")
        for skill in self.skills:
            self.assertEqual(skill["canonical_id"], skill["id"])
            self.assertEqual(skill["category"], "content")
            self.assertEqual(skill["license"], "MIT")
            self.assertEqual(skill["author"], "Jake Schincariol")
            self.assertEqual(skill["source_repo"], self.manifest["source_repo"])
            self.assertEqual(skill["source_revision"], self.manifest["revision"])
            self.assertEqual(skill["source_path"], f"skills/{skill['name']}/SKILL.md")
            self.assertIn("youtube", skill["tags"])
            self.assertGreater(len(skill["description"]), 40)
        for filename in ("data/catalog.json", "data/skills_index.json"):
            source = json.loads((ROOT / filename).read_text())
            rows = source["skills"] if isinstance(source, dict) else source
            by_id = {row["id"]: row for row in rows}
            for skill in self.skills:
                for key in ("canonical_id", "description", "category", "source_repo",
                            "source_revision", "source_path", "license", "author"):
                    self.assertEqual(by_id[skill["id"]][key], skill[key])
        credits = json.loads((ROOT / "data/source-credits.json").read_text())
        self.assertIn(self.manifest["revision"], credits["sections"]["youtube"][0])

    def test_all_vendored_files_have_reversible_documented_adaptations(self):
        recorded = set()
        for record in self.manifest["files"]:
            with self.subTest(path=record["path"]):
                path = ROOT / record["path"]
                self.assertTrue(path.resolve().is_relative_to(self.pack))
                content = path.read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"])
                original = content.decode("utf-8")
                if path.name == "SKILL.md":
                    notes = self.manifest["skill_notes"]
                    self.assertTrue(original.endswith(notes))
                    original = original[:-len(notes)]
                for replacement in reversed(record.get("replacements", [])):
                    self.assertEqual(original.count(replacement["new"]), 1)
                    original = original.replace(replacement["new"], replacement["old"])
                self.assertEqual(
                    hashlib.sha256(original.encode("utf-8")).hexdigest(),
                    record["source_sha256"],
                )
                self.assertNotIn(path, recorded)
                recorded.add(path)
        files = {path for path in self.pack.rglob("*") if path.is_file()}
        self.assertEqual(recorded, files - {self.pack / "README.md"})

    def test_each_skill_contains_license_template_and_local_references(self):
        license_text = (self.pack / "LICENSE").read_text()
        self.assertIn("Copyright (c) 2026 Jake Schincariol", license_text)
        self.assertIn("MIT License", license_text)
        for skill in self.skills:
            directory = ROOT / skill["path"]
            text = (directory / "SKILL.md").read_text()
            self.assertEqual((directory / "LICENSE").read_text(), license_text)
            self.assertEqual(
                (directory / "templates/voice.md").read_bytes(),
                (self.pack / "templates/voice.md").read_bytes(),
            )
            self.assertNotRegex(text, r"\.\./yt-[\w-]+/")
            for reference in re.findall(r"shared-tools/[\w.-]+", text):
                self.assertTrue((directory / reference).is_file(), reference)
            self.assertFalse((directory / ".claude-plugin").exists())
        for path in self.pack.rglob("hooks.json"):
            formulas = json.loads(path.read_text())["hooks"]
            self.assertEqual(len(formulas), 21)
            self.assertEqual(len({formula["id"] for formula in formulas}), 21)
            for formula in formulas:
                for pattern in formula["match"]:
                    re.compile(pattern)

    def exercise_helpers(self, directory, work):
        hook = ["--hook", "Why your first 30 seconds cost you viewers", "--json"]
        title = ["--title", "5 camera mistakes you can fix today", "--thumb", "LIGHT IT RIGHT", "--json"]
        tools = {
            "yt-script": [("hookscore.py", hook)],
            "yt-package": [("title.py", title)],
            "yt-edit": [("deadair.py", [str(work / "transcript.srt"), "--json"])],
            "yt-chapters": [("chapters.py", [str(work / "transcript.srt"), "--target", "3", "--json"])],
            "yt-retention": [("retention.py", [
                str(work / "retention.csv"), "--duration", "180",
                "--transcript", str(work / "transcript.srt"), "--json",
            ])],
            "yt-viral": [("swipe.py", [str(work / "videos.json"), "--min", "2.0", "--json"])],
            "yt-audit": [("shared-tools/title.py", title), ("shared-tools/hookscore.py", hook)],
            "yt-shorts": [("shared-tools/hookscore.py", hook)],
        }
        for relative, arguments in tools.get(directory.name, []):
            result = subprocess.run(
                [sys.executable, "-B", str(directory / relative), *arguments],
                cwd=work, text=True, capture_output=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            if relative.endswith("hookscore.py"):
                self.assertEqual(len(report), 1)
                self.assertTrue(0 <= report[0]["verdict"] <= 100)
            elif relative.endswith("title.py"):
                self.assertEqual(len(report), 1)
                self.assertTrue(0 <= report[0]["score"] <= 100)
            elif relative == "deadair.py":
                self.assertEqual(report["duration"], 175)
                self.assertTrue(report["cuts"])
            elif relative == "chapters.py":
                self.assertTrue(report["valid"])
                self.assertEqual(len(report["chapters"]), 3)
                self.assertEqual(report["chapters"][0]["start"], 0)
                self.assertTrue(all(chapter["seconds"] >= 10 for chapter in report["chapters"]))
            elif relative == "retention.py":
                self.assertEqual(report["points"], 11)
                self.assertTrue(any(report["said"].values()))
            elif relative == "swipe.py":
                self.assertEqual(len(report["outliers"]), 1)
                self.assertEqual(report["outliers"][0]["multiple"], 10)

    def test_every_skill_runs_in_isolation_and_round_trips_in_both_modes(self):
        for mode in ("copy", "link"):
            for skill in self.skills:
                with self.subTest(mode=mode, skill=skill["id"]), tempfile.TemporaryDirectory(prefix="vie-youtube-") as temp:
                    work = Path(temp)
                    destination = work / "project with spaces/skills"
                    cues = []
                    for number in range(12):
                        start = number * 15
                        end = start + 10
                        cues.append(
                            f"{number + 1}\n00:{start // 60:02}:{start % 60:02},000 --> "
                            f"00:{end // 60:02}:{end % 60:02},000\n"
                            f"Camera lesson {number + 1} explains lighting and framing.\n"
                        )
                    (work / "transcript.srt").write_text("\n".join(cues))
                    retention = [100, 95, 90, 75, 73, 71, 68, 66, 64, 62, 60]
                    (work / "retention.csv").write_text(
                        "position,retention\n" + "".join(f"{i * 10},{value}\n" for i, value in enumerate(retention))
                    )
                    (work / "videos.json").write_text(json.dumps([
                        {"channel": "Fixture", "title": f"Camera lesson {i}", "views": views}
                        for i, views in enumerate([100, 100, 100, 100, 1000])
                    ]))
                    result = cli("install", skill["id"], "--target", "codex", "--mode", mode, "--dest", str(destination))
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    installed = destination / skill["name"]
                    self.assertEqual(installed.is_symlink(), mode == "link")
                    self.assertEqual(list(destination.glob("yt-*")), [installed])
                    manifest = json.loads((destination / ".vas-manifest.json").read_text())
                    self.assertEqual(set(manifest), {skill["id"]})
                    source = ROOT / skill["path"]
                    for path in source.rglob("*"):
                        if path.is_file():
                            self.assertEqual((installed / path.relative_to(source)).read_bytes(), path.read_bytes())
                    self.exercise_helpers(installed, work)
                    status = cli("status", "--dest", str(destination))
                    self.assertEqual(status.returncode, 0, status.stderr)
                    self.assertIn("Total installed: 1", status.stdout)
                    removed = cli("uninstall", skill["id"], "--dest", str(destination))
                    self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
                    self.assertEqual(list(destination.iterdir()), [destination / ".vas-manifest.json"])


if __name__ == "__main__":
    unittest.main()
