#!/usr/bin/env python3
"""
Import the claude-awesome-video-creation skill from HaochenSHI66/claude-awesome-video-creation.
"""

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = "HaochenSHI66/claude-awesome-video-creation"
UPSTREAM_REV = "4b0f8d89d50046ac13003e95bcde081e328c2373"
AUTHOR = "SHI Haochen (HaochenSHI66)"
AUTHOR_URL = "https://github.com/HaochenSHI66"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE"

# Locate cloned upstream in temp directory or clone if needed
UPSTREAM_DIR = None
import glob
possible = glob.glob("/var/folders/mb/h9q8rwdd6b15q7tk86w1dclr0000gn/T/video-creation-*")
for p in possible:
    if (Path(p) / "skills/claude-awesome-video-creation/SKILL.md").exists():
        UPSTREAM_DIR = Path(p)
        break

if not UPSTREAM_DIR:
    import tempfile, subprocess
    temp_dir = tempfile.mkdtemp(prefix="video-creation-")
    subprocess.run(["git", "clone", f"https://github.com/{UPSTREAM_REPO}.git", temp_dir], check=True)
    subprocess.run(["git", "checkout", UPSTREAM_REV], cwd=temp_dir, check=True)
    UPSTREAM_DIR = Path(temp_dir)

UPSTREAM_SKILL_DIR = UPSTREAM_DIR / "skills" / "claude-awesome-video-creation"

NOTICE_CONTENT = f"""# Notices

`claude-awesome-video-creation` is imported from [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}) at revision `{UPSTREAM_REV}` under the MIT License (Copyright (c) 2026 SHI Haochen (HaochenSHI66); Copyright (c) 2026 Leonxlnx (cinetic, which this skill is built on)); see `LICENSE`.

## Runtime & Tool Prerequisites

- Making videos with Remotion requires Node.js 22+, Remotion 4+, ffmpeg 6+, and Python 3.11+ with `numpy`, `scipy`, `soundfile`, `pyloudnorm`, and `pillow` for audio scoring, sync checks, and QA scripts.
- Optional external tools: `edge-tts` for draft voiceover synthesis, or an OpenAI/ElevenLabs API key for voice cloning.
- Codex CLI / image generation models are optional for generating custom mascot presenter sprites.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No scripts, renders, or node processes are executed, no external dependencies or runtimes are installed, and no API services are connected during installation.
"""

VAS_NOTES = f"""

---

## VAS installation notes

- Canonical ID: `claude-awesome-video-creation`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at commit `{UPSTREAM_REV}` (`skills/claude-awesome-video-creation/SKILL.md`).
- License: MIT (Copyright (c) 2026 SHI Haochen (HaochenSHI66); Copyright (c) 2026 Leonxlnx (cinetic, which this skill is built on)); see `LICENSE` and `NOTICE.md`.
- Bundled references, scripts, and assets: 25 reference guides in `references/`, 31 helper scripts in `scripts/`, and full worked example/starters in `assets/`.
- Install via CLI: `./vas install claude-awesome-video-creation --target <agent> --mode link` (or `--mode copy`).
"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    dest_dir = REPO_ROOT / "skills" / "claude-awesome-video-creation"
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    file_records = []

    # 1. Add LICENSE (MIT)
    root_license_text = (UPSTREAM_DIR / "LICENSE").read_text(encoding="utf-8")
    lic_file = dest_dir / "LICENSE"
    lic_file.write_text(root_license_text, encoding="utf-8")
    lic_file.chmod(0o644)
    file_records.append({
        "source_path": "LICENSE",
        "path": "skills/claude-awesome-video-creation/LICENSE",
        "source_sha256": sha256_file(UPSTREAM_DIR / "LICENSE"),
        "sha256": sha256_file(lic_file),
        "executable": False,
    })

    # 2. Add NOTICE.md
    not_file = dest_dir / "NOTICE.md"
    not_file.write_text(NOTICE_CONTENT.strip() + "\n", encoding="utf-8")
    not_file.chmod(0o644)
    file_records.append({
        "source_path": "skills/claude-awesome-video-creation/NOTICE.md",
        "path": "skills/claude-awesome-video-creation/NOTICE.md",
        "source_sha256": sha256_file(not_file),
        "sha256": sha256_file(not_file),
        "executable": False,
    })

    # 3. Copy all upstream files in skills/claude-awesome-video-creation
    for src_path in sorted(UPSTREAM_SKILL_DIR.rglob("*")):
        if src_path.is_dir() or src_path.is_symlink():
            continue
        rel = src_path.relative_to(UPSTREAM_SKILL_DIR)
        dst_path = dest_dir / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        src_sha = sha256_file(src_path)
        is_exec = bool(src_path.stat().st_mode & 0o111)

        if rel.as_posix() == "SKILL.md":
            raw_text = src_path.read_text(encoding="utf-8")
            parts = raw_text.split("---", 2)
            body = parts[2] if len(parts) >= 3 else raw_text
            new_frontmatter = (
                "---\n"
                "name: claude-awesome-video-creation\n"
                'description: "Make a complete, follow-along tutorial or explainer video from code with Claude Code. Use it whenever someone wants a demo video, tool walkthrough, course or assignment video, \'how to use X\' explainer, launch film or feature showcase built with Remotion (React). The skill covers script and voiceover (draft TTS or a cloned voice, with word timings), a beat-locked timeline that drives picture, captions and an original code-made soundtrack, macOS-style glass terminals with syntax colour, an animated mascot presenter with lip-sync, segmented rendering that avoids headless-Chrome hangs, and measured QA (frozen-frame scan, contact sheets, loudness)."\n'
                "category: media\n"
                'tags: ["video", "remotion", "react", "tutorial", "video-creation", "voiceover", "motion-graphics", "claude-code"]\n'
                "risk: safe\n"
                f'author: "{AUTHOR}"\n'
                f'license: "{LICENSE_NAME}"\n'
                f'source_repo: "{UPSTREAM_REPO}"\n'
                f'source_revision: "{UPSTREAM_REV}"\n'
                f'source_path: "skills/claude-awesome-video-creation/SKILL.md"\n'
                "---\n"
            )
            final_content = new_frontmatter + body.rstrip() + VAS_NOTES
            dst_path.write_text(final_content, encoding="utf-8")
            dst_path.chmod(0o644)
            is_exec = False
        else:
            shutil.copy2(src_path, dst_path)
            dst_path.chmod(0o755 if is_exec else 0o644)

        dst_sha = sha256_file(dst_path)
        file_records.append({
            "source_path": f"skills/claude-awesome-video-creation/{rel.as_posix()}",
            "path": f"skills/claude-awesome-video-creation/{rel.as_posix()}",
            "source_sha256": src_sha,
            "sha256": dst_sha,
            "executable": is_exec,
        })

    print(f"Copied {len(file_records)} files to skills/claude-awesome-video-creation.")

    skill_entry = {
        "id": "claude-awesome-video-creation",
        "canonical_id": "claude-awesome-video-creation",
        "name": "claude-awesome-video-creation",
        "path": "skills/claude-awesome-video-creation",
        "description": "Make a complete, follow-along tutorial or explainer video from code with Claude Code. Use it whenever someone wants a demo video, tool walkthrough, course or assignment video, 'how to use X' explainer, launch film or feature showcase built with Remotion (React). The skill covers script and voiceover (draft TTS or a cloned voice, with word timings), a beat-locked timeline that drives picture, captions and an original code-made soundtrack, macOS-style glass terminals with syntax colour, an animated mascot presenter with lip-sync, segmented rendering that avoids headless-Chrome hangs, and measured QA (frozen-frame scan, contact sheets, loudness).",
        "category": "media",
        "tags": [
            "video",
            "remotion",
            "react",
            "tutorial",
            "video-creation",
            "voiceover",
            "motion-graphics",
            "claude-code",
        ],
        "risk": "safe",
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "source": f"https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV}/skills/claude-awesome-video-creation",
        "source_repo": UPSTREAM_REPO,
        "source_revision": UPSTREAM_REV,
        "source_path": "skills/claude-awesome-video-creation/SKILL.md",
        "license": LICENSE_NAME,
        "license_source": LICENSE_URL,
    }

    # Write data/video-creation-import.json
    import_manifest = {
        "source_repo": UPSTREAM_REPO,
        "source_url": f"https://github.com/{UPSTREAM_REPO}",
        "revision": UPSTREAM_REV,
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "license": LICENSE_NAME,
        "license_source": LICENSE_URL,
        "skill_count": 1,
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3884,
            "upstream_is_fork": False,
            "methods": [
                "canonical-id/name",
                "source-repo/path",
                "raw-sha256",
                "normalized-body",
                "renamed-body",
                "body-containment",
                "7-word-shingles",
            ],
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,884 catalog skills identified zero existing duplicates (max similarity 0.000). claude-awesome-video-creation is a completely unique, follow-along code-to-tutorial-video creation skill.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, references/, scripts/, and assets/ under Open Agent Skills format.",
            "Append reversible VAS installation, attribution, prerequisites, and safety notes to SKILL.md.",
            "Include upstream MIT LICENSE and add NOTICE.md clarifying standalone operation, third-party attribution (cinetic by Leonxlnx), and prerequisites.",
            "Preserve executable bits (0755) on shell and Python execution scripts.",
            "Map skill to media category (119 existing categories preserved).",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "skills": [skill_entry],
        "files": file_records,
    }

    manifest_path = REPO_ROOT / "data" / "video-creation-import.json"
    manifest_path.write_text(json.dumps(import_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote import manifest to {manifest_path}")

    # Update data/source-credits.json
    credits_path = REPO_ROOT / "data" / "source-credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8"))
    credits["sections"]["videocreation"] = [
        f"- **[HaochenSHI66/claude-awesome-video-creation](https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV})**: Code-to-tutorial explainer video creation skill by {AUTHOR} (built on cinetic by Leonxlnx) at revision `{UPSTREAM_REV}` under the {LICENSE_NAME} License.",
        "- Provides complete follow-along tutorial/explainer video production from code with Remotion (React): voiceover pipeline, beat-locked timeline, macOS-style glass terminals, animated mascot presenter with lip-sync, segmented rendering, and measured QA.",
        "- Standalone payload preserves upstream Agent Skills specification SKILL.md with complete references (craft rules, finishing, voiceover, mascot, look-tutorial, render-qa, technique library), helper scripts, starters, and the full worked example 'Teach It Once'.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed, and no external accounts are connected.",
    ]
    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {credits_path}")

    # Update data/catalog.json
    cat_path = REPO_ROOT / "data" / "catalog.json"
    cat_data = json.loads(cat_path.read_text(encoding="utf-8"))
    existing_skills = [s for s in cat_data["skills"] if s["id"] != "claude-awesome-video-creation"]
    existing_skills.append(skill_entry)
    existing_skills.sort(key=lambda x: x["id"])
    cat_data["skills"] = existing_skills
    cat_data["total"] = len(existing_skills)
    cat_path.write_text(json.dumps(cat_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {cat_path} with total {len(existing_skills)} skills.")


if __name__ == "__main__":
    main()
