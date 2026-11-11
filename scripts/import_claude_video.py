#!/usr/bin/env python3
"""
Import watch skill from bradautomates/claude-video.
Validates upstream files, copies into skills/watch,
adds VAS installation notes, NOTICE.md, LICENSE,
records provenance to data/claude-video-import.json,
and updates data/catalog.json and data/source-credits.json.
"""

import hashlib
import json
import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = "bradautomates/claude-video"
UPSTREAM_REV = "03ceb42f7fa2c4439aca01752118044baabffb8f"
AUTHOR = "Bradley Bonanno"
AUTHOR_URL = "https://github.com/bradautomates"

UPSTREAM_DIR = Path("/tmp/claude-video-temp")
if not UPSTREAM_DIR.exists() or not (UPSTREAM_DIR / "skills/watch/SKILL.md").exists():
    raise RuntimeError(f"Upstream clone not found at {UPSTREAM_DIR}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    skill_id = "watch"
    target_dir = REPO_ROOT / "skills" / skill_id
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy upstream license as LICENSE
    license_src = UPSTREAM_DIR / "LICENSE"
    license_dst = target_dir / "LICENSE"
    shutil.copy2(license_src, license_dst)

    # 2. Generate NOTICE.md
    notice_text = f"""# Notice for {skill_id}

This skill payload is adapted from upstream repository [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO})
at commit revision `{UPSTREAM_REV}`.

- Author: {AUTHOR}
- Upstream License: MIT License (see bundled LICENSE)
- Upstream Source Path: `skills/watch`
- Adapted for Vie Agentic Skill (VAS) distribution.

## Bundled Components and Provenance

- `SKILL.md`: Core runbook and Agent Skills specification for video inspection, multimodal understanding, frame extraction, and transcription.
- `scripts/`: Standalone Python scripts implementing the watch pipeline (`watch.py`, `setup.py`, `frames.py`, `download.py`, `transcribe.py`, `whisper.py`, `local_whisperx.py`, `gemini.py`, `config.py`, `runtime.py`, `build-skill.sh`).
  - Base runtime operates entirely on Python's standard library (Python 3.10+).
  - External binaries (`ffmpeg`, `yt-dlp`) and optional models (`whisperx`, `groq`, `openai`, `gemini`) are user-configured prerequisites and are never executed or downloaded during VAS skill installation.

## VAS Adaptation Notes

- Preserves upstream directory structure and standalone execution semantics.
- Appended standard VAS installation, attribution, and safety notes to `SKILL.md`.
- Mapped to existing `media` category to preserve the exact 119-category taxonomy.
- Managed by Vie Agentic Skill (VAS) with zero external package manager dependencies (no NPX).
"""
    notice_dst = target_dir / "NOTICE.md"
    notice_dst.write_text(notice_text, encoding="utf-8")

    # 3. Copy .gitattributes and .skillignore
    for dotfile in [".gitattributes", ".skillignore"]:
        src_dot = UPSTREAM_DIR / "skills/watch" / dotfile
        if src_dot.is_file():
            shutil.copy2(src_dot, target_dir / dotfile)

    # 4. Copy scripts/ directory
    src_scripts = UPSTREAM_DIR / "skills/watch/scripts"
    dst_scripts = target_dir / "scripts"
    dst_scripts.mkdir(parents=True, exist_ok=True)
    for p in src_scripts.iterdir():
        if p.is_file():
            target_p = dst_scripts / p.name
            shutil.copy2(p, target_p)
            # preserve executable permissions
            if os.access(p, os.X_OK):
                target_p.chmod(0o755)
            else:
                target_p.chmod(0o644)

    # 5. Process SKILL.md
    raw_skill_md_path = UPSTREAM_DIR / "skills/watch/SKILL.md"
    raw_skill_md = raw_skill_md_path.read_text(encoding="utf-8")
    raw_sha = sha256_file(raw_skill_md_path)

    # Inject category and tags into frontmatter if not present
    if "category:" not in raw_skill_md:
        frontmatter_replacement = """---
name: watch
description: Watch a video (URL or local path). Downloads with yt-dlp, extracts auto-scaled frames with ffmpeg, pulls the transcript from captions (or local WhisperX / cloud Whisper fallback), and hands the result to the agent so it can answer questions about what's in the video. With a Gemini API key, Google's agentic video model watches the full video instead.
category: media
tags:
  - video
  - watch
  - youtube
  - multimodal
  - transcription
  - whisper
  - gemini
  - ffmpeg
  - yt-dlp
license: MIT
allowed-tools: Bash, Read, AskUserQuestion
metadata:
  author: Bradley Bonanno
  version: "0.3.2"
---"""
        if raw_skill_md.startswith("---"):
            _, _, rest = raw_skill_md[3:].partition("---")
            skill_body = rest.lstrip("\r\n")
        else:
            skill_body = raw_skill_md
        modified_skill_md = frontmatter_replacement + "\n\n" + skill_body
    else:
        modified_skill_md = raw_skill_md

    vas_notes = f"""

## VAS installation notes

This skill is curated and verified by **Vie Agentic Skill (VAS)** from [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}).
- Canonical ID: `{skill_id}`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) (revision `{UPSTREAM_REV}`, path `skills/{skill_id}`)
- Author: {AUTHOR}
- License: MIT (see bundled `LICENSE` and `NOTICE.md`)
- Role: Video inspection, frame extraction, caption parsing, and multimodal video understanding workflow for AI coding agents.
- Prerequisites: Python 3.10+; optional `ffmpeg` and `yt-dlp` for local media extraction, optional `GEMINI_API_KEY` for Google Gemini multimodal video engine, optional `whisperx` / `groq` / `openai` for audio transcription fallbacks.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""
    adapted_skill_md = modified_skill_md.rstrip() + vas_notes
    skill_md_dst = target_dir / "SKILL.md"
    skill_md_dst.write_text(adapted_skill_md, encoding="utf-8")

    # Record all packaged files
    packaged_files = []
    for p in sorted(target_dir.rglob("*")):
        if p.is_file():
            rel_path = p.relative_to(REPO_ROOT).as_posix()
            upstream_rel = p.relative_to(target_dir).as_posix()
            if upstream_rel == "LICENSE":
                src_path = "LICENSE"
                src_sha = sha256_file(license_src)
            elif upstream_rel == "NOTICE.md":
                src_path = f"skills/{skill_id}/NOTICE.md (generated by VAS)"
                src_sha = sha256_file(notice_dst)
            elif upstream_rel == "SKILL.md":
                src_path = f"skills/{skill_id}/SKILL.md"
                src_sha = raw_sha
            else:
                upstream_file = UPSTREAM_DIR / "skills/watch" / upstream_rel
                src_path = f"skills/{skill_id}/{upstream_rel}"
                src_sha = sha256_file(upstream_file)

            packaged_files.append({
                "skill_id": skill_id,
                "source_path": src_path,
                "path": rel_path,
                "source_sha256": src_sha,
                "sha256": sha256_file(p),
                "executable": bool(os.stat(p).st_mode & 0o111),
            })

    import_manifest = {
        "source_repo": UPSTREAM_REPO,
        "source_url": f"https://github.com/{UPSTREAM_REPO}",
        "revision": UPSTREAM_REV,
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "license": "MIT",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
        "skill_count": 1,
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 4077,
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
            "collision_rationale": "Exact and shingle similarity comparison against all 4,077 catalog skills identified zero existing duplicates (0.0002 max 7-word shingle Jaccard similarity). `watch` is a genuinely new skill from Bradley Bonanno establishing a comprehensive multimodal video understanding, frame extraction, caption parsing, and transcription pipeline for coding agents.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md and scripts/ under Open Agent Skills format.",
            "Include upstream MIT LICENSE and add NOTICE.md clarifying standalone operation.",
            "Append reversible VAS installation, attribution, and prerequisites notes to SKILL.md.",
            "Map `watch` to the existing `media` category to preserve the 119-category taxonomy.",
            "Base runtime operates entirely on Python standard library without requiring external package managers (no NPX).",
        ],
        "skills": [
            {
                "id": skill_id,
                "canonical_id": skill_id,
                "name": skill_id,
                "path": f"skills/{skill_id}",
                "description": "Watch a video (URL or local path). Downloads with yt-dlp, extracts auto-scaled frames with ffmpeg, pulls the transcript from captions (or local WhisperX / cloud Whisper fallback), and hands the result to the agent so it can answer questions about what's in the video. With a Gemini API key, Google's agentic video model watches the full video instead.",
                "category": "media",
                "tags": [
                    "video",
                    "watch",
                    "youtube",
                    "multimodal",
                    "transcription",
                    "whisper",
                    "gemini",
                    "ffmpeg",
                    "yt-dlp",
                ],
                "risk": "safe",
                "author": AUTHOR,
                "author_url": AUTHOR_URL,
                "source": f"https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV}/skills/{skill_id}",
                "source_repo": UPSTREAM_REPO,
                "source_revision": UPSTREAM_REV,
                "source_path": f"skills/{skill_id}",
                "license": "MIT",
                "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
            }
        ],
        "files": packaged_files,
    }

    manifest_path = REPO_ROOT / "data/claude-video-import.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"✓ Saved import manifest: {manifest_path}")

    # Update data/catalog.json
    catalog_path = REPO_ROOT / "data/catalog.json"
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    catalog["skills"] = [s for s in catalog["skills"] if s["id"] != skill_id]
    catalog["skills"].append(import_manifest["skills"][0])
    catalog["total"] = len(catalog["skills"])
    catalog["total_skills"] = len(catalog["skills"])
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"✓ Updated {catalog_path} with skill {skill_id} (total: {catalog['total']})")

    # Update data/source-credits.json
    credits_path = REPO_ROOT / "data/source-credits.json"
    with open(credits_path, "r", encoding="utf-8") as f:
        credits = json.load(f)

    credits["sections"]["claudevideo"] = [
        f"- **[{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV})**: Video inspection, frame extraction, caption parsing, and multimodal video understanding skill (`watch`) by {AUTHOR} at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Gives AI agents multimodal video evidence: downloads via yt-dlp, extracts auto-scaled scene-aware frames with ffmpeg, parses native captions (VTT) or transcribes speech via local WhisperX or cloud Whisper (Groq/OpenAI), and supports full-video direct analysis via Google Gemini API.",
        "- Standalone payload preserves upstream Agent Skills specification SKILL.md with complete scripts (`watch.py`, `setup.py`, `frames.py`, `download.py`, `transcribe.py`, `whisper.py`, `local_whisperx.py`, `gemini.py`, `config.py`, `runtime.py`, `build-skill.sh`).",
        "- Base runtime operates entirely on Python's standard library (Python 3.10+). External binaries (`ffmpeg`, `yt-dlp`) and optional models (`whisperx`, `groq`, `openai`, `gemini`) run as user-configured prerequisites.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed, and no external accounts are connected.",
    ]
    with open(credits_path, "w", encoding="utf-8") as f:
        json.dump(credits, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"✓ Updated {credits_path} with section 'claudevideo'")


if __name__ == "__main__":
    main()
