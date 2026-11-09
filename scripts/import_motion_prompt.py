#!/usr/bin/env python3
"""
Import skill from showheyohtaki/motion-prompt:
Imports 1 genuinely new skill (`motion-prompt`) providing 192 named visual effects (#001-#192)
across 8 packs with runnable Canvas 2D reference implementations, timing/easing specs, and a
zero-dependency Node.js CLI helper.
"""

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = "showheyohtaki/motion-prompt"
UPSTREAM_REV = "7819d3879eb7d5a1475c11c001bedffb5cab64af"
AUTHOR = "Shohei Ohtaki (showheyohtaki)"
AUTHOR_URL = "https://github.com/showheyohtaki"

UPSTREAM_DIR = Path("/tmp/motion-prompt-inspect")
if not UPSTREAM_DIR.exists() or not (UPSTREAM_DIR / "skills/motion-prompt/SKILL.md").exists():
    raise RuntimeError(f"Upstream clone not found at {UPSTREAM_DIR}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    skill_id = "motion-prompt"
    source_dir_rel = "skills/motion-prompt"
    source_skill_md = "skills/motion-prompt/SKILL.md"
    final_cat = "design"
    tags = [
        "motion-prompt",
        "motion-graphics",
        "animation",
        "canvas-2d",
        "camera-moves",
        "ui-components",
        "landing-page",
        "photo-effects",
        "remotion",
        "design",
    ]
    description = (
        "Vocabulary of 192 named visual effects (#001-#192) across motion graphics, camera work & "
        "transitions, UI components, landing-page & web effects, and photo looks/lighting/styles, "
        "each with a runnable dependency-free Canvas 2D reference implementation and timing/easing spec. "
        "Use whenever the user names motion-prompt or any element/pack, asks to browse/pick/list visual "
        "effects, or asks to make, animate, edit, or style a video, motion graphic, title card, caption, "
        "camera move, transition, UI animation, landing page, hero section, scroll/hover effect, or photo look."
    )

    dest_dir = REPO_ROOT / "skills" / skill_id
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    file_records = []

    # 1. LICENSE
    src_lic = UPSTREAM_DIR / "LICENSE"
    lic_file = dest_dir / "LICENSE"
    shutil.copy2(src_lic, lic_file)
    lic_file.chmod(0o644)
    lic_sha = sha256_file(lic_file)
    file_records.append({
        "skill_id": skill_id,
        "source_path": "LICENSE",
        "path": f"skills/{skill_id}/LICENSE",
        "source_sha256": sha256_file(src_lic),
        "sha256": lic_sha,
        "executable": False,
    })

    # 2. THIRD-PARTY-NOTICES.md
    src_tpn = UPSTREAM_DIR / "THIRD-PARTY-NOTICES.md"
    tpn_file = dest_dir / "THIRD-PARTY-NOTICES.md"
    shutil.copy2(src_tpn, tpn_file)
    tpn_file.chmod(0o644)
    tpn_sha = sha256_file(tpn_file)
    file_records.append({
        "skill_id": skill_id,
        "source_path": "THIRD-PARTY-NOTICES.md",
        "path": f"skills/{skill_id}/THIRD-PARTY-NOTICES.md",
        "source_sha256": sha256_file(src_tpn),
        "sha256": tpn_sha,
        "executable": False,
    })

    # 3. NOTICE.md
    not_content = f"""# Notices

`{skill_id}` is imported from [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at revision `{UPSTREAM_REV}` (`{source_skill_md}`) under the MIT License (Copyright (c) 2026 Shohei Ohtaki); see `LICENSE` and `THIRD-PARTY-NOTICES.md`.

## Purpose & Bundled Payload

- Provides a shared vocabulary of 192 numbered visual and motion effects (`#001`–`#192`) across 8 packs (`motion`, `camera`, `ui`, `lp`, `photo`, `motion2`, `lp2`, `camera2`), each paired with a runnable dependency-free Canvas 2D reference implementation (`cells[i](k, w, h, u)`) and concrete timing/easing specifications.
- Standalone payload includes `SKILL.md`, `references/porting.md` (translation playbook for HTML/Canvas, Remotion, CSS/WAAPI, GSAP/Motion, ffmpeg/Python/Manim, After Effects/Premiere, and generative video/image prompts), `scripts/motion-prompt.mjs` (zero-dependency Node.js 18+ CLI for `pick`, `search`, `list`, `get`, `prompt`, `kit`, and `info`), `LICENSE`, and `THIRD-PARTY-NOTICES.md`.
- Interactive gallery and live Canvas 2D previews are available on the VAS guide `/blog/thu-vien-motion-prompt-192-hieu-ung-canvas-2d/` as well as upstream at `https://showheyohtaki.github.io/motion-prompt/`.

## Prerequisites & Safe Operation

- Runtime prerequisites when executing `scripts/motion-prompt.mjs`: Node.js 18+ (`node`) and HTTPS network access to `https://showheyohtaki.github.io/motion-prompt/api/v1` or `https://raw.githubusercontent.com/showheyohtaki/motion-prompt/main/api/v1` (responses are cached locally in `~/.cache/motion-prompt/v1`).
- Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`. No script, local callback server, or network request is executed during installation.
"""
    not_file = dest_dir / "NOTICE.md"
    not_file.write_text(not_content.strip() + "\n", encoding="utf-8")
    not_file.chmod(0o644)
    not_sha = sha256_file(not_file)
    file_records.append({
        "skill_id": skill_id,
        "source_path": f"{source_dir_rel}/NOTICE.md (generated by VAS)",
        "path": f"skills/{skill_id}/NOTICE.md",
        "source_sha256": not_sha,
        "sha256": not_sha,
        "executable": False,
    })

    # 4. Copy all files from upstream skills/motion-prompt/
    src_skill_dir = UPSTREAM_DIR / "skills/motion-prompt"
    for src_path in sorted(src_skill_dir.rglob("*")):
        if src_path.is_dir() or src_path.is_symlink():
            continue
        rel = src_path.relative_to(src_skill_dir)
        dst_path = dest_dir / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        src_mode = os.stat(src_path).st_mode
        is_exec = bool(src_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        src_sha = sha256_file(src_path)

        if rel.name == "SKILL.md":
            text = src_path.read_text(encoding="utf-8")
            lines = text.splitlines()
            idx = 1
            while idx < len(lines) and lines[idx].strip() != "---":
                idx += 1
            body = "\n".join(lines[idx + 1:]).lstrip()

            tags_str = json.dumps(tags)
            desc_escaped = json.dumps(description)
            new_frontmatter = f"""---
name: {skill_id}
description: {desc_escaped}
category: {final_cat}
tags: {tags_str}
risk: safe
author: "{AUTHOR}"
author_url: "{AUTHOR_URL}"
source: "https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV}/{source_dir_rel}"
source_repo: "{UPSTREAM_REPO}"
source_revision: "{UPSTREAM_REV}"
source_path: "{source_skill_md}"
license: "MIT"
license_source: "https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE"
metadata:
  version: "1.0.0"
  short-description: "192 named visual effects (#001-#192) with Canvas 2D reference code and motion specs"
---

"""
            vas_notes = f"""

---

## VAS installation notes

- Canonical ID: `{skill_id}`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at commit `{UPSTREAM_REV}` (`{source_skill_md}`).
- Author: {AUTHOR} (`{AUTHOR_URL}`).
- License: MIT (Copyright (c) 2026 Shohei Ohtaki); see `LICENSE`, `THIRD-PARTY-NOTICES.md`, and `NOTICE.md`.
- Runtime prerequisites: Node.js 18+ (`node`) to run `scripts/motion-prompt.mjs` (`pick`, `search`, `list`, `get`, `prompt`, `kit`, `info`).
- Interactive VAS gallery & guide: `/blog/thu-vien-motion-prompt-192-hieu-ung-canvas-2d/` (renders all 192 live Canvas 2D moves directly in the browser).
- Install via CLI: `./vas install {skill_id} --target <agent> --mode link` (or `--mode copy`).
"""
            full_content = new_frontmatter + body.rstrip() + vas_notes + "\n"
            dst_path.write_text(full_content, encoding="utf-8")
            dst_path.chmod(0o644)
            is_exec = False
        else:
            shutil.copy2(src_path, dst_path)
            if is_exec:
                dst_path.chmod(0o755)
            else:
                dst_path.chmod(0o644)

        file_records.append({
            "skill_id": skill_id,
            "source_path": f"{source_dir_rel}/{rel}",
            "path": f"skills/{skill_id}/{rel}",
            "source_sha256": src_sha,
            "sha256": sha256_file(dst_path),
            "executable": is_exec,
        })

    file_records.sort(key=lambda r: r["path"])

    skill_entry = {
        "id": skill_id,
        "canonical_id": skill_id,
        "name": skill_id,
        "path": f"skills/{skill_id}",
        "description": description,
        "category": final_cat,
        "tags": tags,
        "risk": "safe",
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "source": f"https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV}/{source_dir_rel}",
        "source_repo": UPSTREAM_REPO,
        "source_revision": UPSTREAM_REV,
        "source_path": source_skill_md,
        "license": "MIT",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
    }

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
            "catalog_count_before": 4074,
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
            "collision_rationale": "Exact and shingle similarity comparison against all 4,074 catalog skills identified zero existing duplicates (0.0000 max 7-word shingle Jaccard similarity). `motion-prompt` is a genuinely new skill providing 192 numbered visual and motion effects (#001-#192) across 8 packs with Canvas 2D reference code, timing/easing specifications, and a zero-dependency Node.js CLI.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, references/porting.md, and scripts/motion-prompt.mjs under Open Agent Skills format.",
            "Include upstream MIT LICENSE and THIRD-PARTY-NOTICES.md alongside VAS NOTICE.md clarifying standalone operation, Node.js 18+ runtime requirements, and local API caching.",
            "Append reversible VAS installation, attribution, prerequisites, and interactive gallery notes to SKILL.md.",
            "Map `motion-prompt` to the existing `design` category to preserve the 119-category taxonomy and surface it under UI/UX & Design.",
            "No script, local callback server, or network request is executed during installation.",
        ],
        "skills": [skill_entry],
        "files": file_records,
    }

    manifest_path = REPO_ROOT / "data" / "motion-prompt-import.json"
    manifest_path.write_text(json.dumps(import_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path} ({len(file_records)} files)")

    # Update data/source-credits.json
    credits_path = REPO_ROOT / "data" / "source-credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8"))
    credits["sections"]["motionprompt"] = [
        f"- **[showheyohtaki/motion-prompt](https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV})**: Library of 192 named visual and motion effects (`#001`–`#192`) with runnable Canvas 2D reference implementations by {AUTHOR} at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Covers 8 packs (24 elements each): Motion graphics moves (`motion`, `motion2`), Camera moves & transitions (`camera`, `camera2`), UI component names (`ui`), Landing page & web effects (`lp`, `lp2`), and Photo looks, lighting & styles (`photo`).",
        "- Includes `scripts/motion-prompt.mjs` (zero-dependency Node.js 18+ CLI supporting `pick`, `search`, `list`, `get`, `prompt`, `kit`, and `info`) and `references/porting.md` for porting Canvas 2D time functions `cells[i](k, w, h, u)` to HTML/Canvas, Remotion, CSS/WAAPI, GSAP/Motion, ffmpeg/Manim, After Effects/Premiere, and video/image generation prompts.",
        "- Standalone payload includes `SKILL.md`, `LICENSE`, `THIRD-PARTY-NOTICES.md`, `NOTICE.md`, `references/porting.md`, and `scripts/motion-prompt.mjs`.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No script, callback server, or network request is executed during installation.",
    ]
    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {credits_path}")

    # Update data/catalog.json
    cat_path = REPO_ROOT / "data" / "catalog.json"
    cat_data = json.loads(cat_path.read_text(encoding="utf-8"))
    existing_skills = [s for s in cat_data["skills"] if s["id"] != skill_id]
    existing_skills.append(skill_entry)
    existing_skills.sort(key=lambda x: x["id"])
    cat_data["skills"] = existing_skills
    cat_data["total"] = len(existing_skills)
    cat_path.write_text(json.dumps(cat_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {cat_path} with total {len(existing_skills)} skills.")


if __name__ == "__main__":
    main()
