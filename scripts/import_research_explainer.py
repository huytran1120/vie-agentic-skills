#!/usr/bin/env python3
"""
Import skills from sepi2p/research-explainer-skill:
1. manim-composer
2. manimce-best-practices
3. manimgl-best-practices
4. research-explainer
"""

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = "sepi2p/research-explainer-skill"
UPSTREAM_REV = "374ecd10fdf60bd08269ff7f51464f754a504ce7"
AUTHOR = "sepi2p"
AUTHOR_URL = "https://github.com/sepi2p"

UPSTREAM_DIR = Path("/tmp/research-explainer-skill")

if not UPSTREAM_DIR.exists() or not (UPSTREAM_DIR / "skills/research-explainer/SKILL.md").exists():
    raise RuntimeError(f"Upstream clone not found at {UPSTREAM_DIR}")

SKILLS_CONFIG = {
    "manim-composer": {
        "name": "manim-composer",
        "description": "Trigger when: (1) User wants to create an educational/explainer video, (2) User has a vague concept they want visualized, (3) User mentions '3b1b style' or 'explain like 3Blue1Brown', (4) User wants to plan a Manim video or animation sequence, (5) User asks to 'compose' or 'plan' a math/science visualization. Transforms vague video ideas into detailed scene-by-scene plans (scenes.md).",
        "category": "media",
        "tags": ["manim", "video", "animation", "scene-planning", "3blue1brown", "storyboard", "education", "explainer"],
        "risk": "safe",
        "author": "Adithya S Kolavi (adithya-s-k)",
        "author_url": "https://github.com/adithya-s-k",
        "license": "MIT",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/skills/manim-composer/LICENSE.txt",
        "notice": f"""# Notices

`manim-composer` is imported from [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}) at revision `{UPSTREAM_REV}` (origin: `github.com/adithya-s-k/manim_skill @ cef0450`) under the MIT License (Copyright (c) 2026 Adithya S Kolavi); see `LICENSE` and `LICENSE.txt`.

## Purpose & Prerequisites

- Plans educational math and science animations before writing code. Produces a detailed `scenes.md` specification with narrative arcs, visual motifs, camera moves, and pacing.
- Works hand-in-hand with `manimce-best-practices` or `manimgl-best-practices` for code implementation.
- No special system runtime is needed for scene composition and planning.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static markdown references, templates, and writes `.vas-manifest.json`.
No processes are executed and no external services are contacted during installation.
""",
        "vas_notes": f"""

---

## VAS installation notes

- Canonical ID: `manim-composer`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at commit `{UPSTREAM_REV}` (`skills/manim-composer/SKILL.md`).
- Author: Adithya S Kolavi (`github.com/adithya-s-k/manim_skill @ cef0450`), packaged by sepi2p.
- License: MIT (Copyright (c) 2026 Adithya S Kolavi); see `LICENSE` and `NOTICE.md`.
- Bundled references: `references/narrative-patterns.md`, `references/scene-examples.md`, `references/visual-techniques.md`, and `templates/scenes-template.md`.
- Install via CLI: `./vas install manim-composer --target <agent> --mode link` (or `--mode copy`).
""",
    },
    "manimce-best-practices": {
        "name": "manimce-best-practices",
        "description": "Trigger when: (1) User mentions 'manim' or 'Manim Community' or 'ManimCE', (2) Code contains 'from manim import *', (3) User runs 'manim' CLI commands, (4) Working with Scene, MathTex, Create(), or ManimCE-specific classes. Best practices for Manim Community Edition - the community-maintained Python animation engine.",
        "category": "media",
        "tags": ["manim", "manimce", "python", "math-animation", "3blue1brown", "video", "best-practices", "animation"],
        "risk": "safe",
        "author": "Adithya S Kolavi (adithya-s-k)",
        "author_url": "https://github.com/adithya-s-k",
        "license": "MIT",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/skills/manimce-best-practices/LICENSE.txt",
        "notice": f"""# Notices

`manimce-best-practices` is imported from [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}) at revision `{UPSTREAM_REV}` (origin: `github.com/adithya-s-k/manim_skill @ cef0450`) under the MIT License (Copyright (c) 2026 Adithya S Kolavi); see `LICENSE` and `LICENSE.txt`.

## Purpose & Prerequisites

- Comprehensive rule library for writing high-quality Python animation code with Manim Community Edition (ManimCE).
- Covers Scenes, Mobjects, VGroup, animations (Transform, ReplacementTransform, Create, Write), LaTeX/MathTex typography, 3D scenes (ThreeDScene), camera control, and CLI rendering.
- Rendering animations locally requires Python 3.9+, Manim Community (`uv tool install manim` or `pip install manim`), FFmpeg, and LaTeX (optional for MathTex).

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static markdown rules, examples, and templates, and writes `.vas-manifest.json`.
No processes are executed and no external services are contacted during installation.
""",
        "vas_notes": f"""

---

## VAS installation notes

- Canonical ID: `manimce-best-practices`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at commit `{UPSTREAM_REV}` (`skills/manimce-best-practices/SKILL.md`).
- Author: Adithya S Kolavi (`github.com/adithya-s-k/manim_skill @ cef0450`), packaged by sepi2p.
- License: MIT (Copyright (c) 2026 Adithya S Kolavi); see `LICENSE` and `NOTICE.md`.
- Bundled references: 25 rule files in `rules/`, code examples in `examples/`, and scene templates in `templates/`.
- Install via CLI: `./vas install manimce-best-practices --target <agent> --mode link` (or `--mode copy`).
""",
    },
    "manimgl-best-practices": {
        "name": "manimgl-best-practices",
        "description": "Trigger when: (1) User mentions 'manimgl' or 'ManimGL' or '3b1b manim', (2) Code contains 'from manimlib import *', (3) User runs 'manimgl' CLI commands, (4) Working with InteractiveScene, self.frame, self.embed(), ShowCreation(), or ManimGL-specific patterns. Best practices for ManimGL (Grant Sanderson's 3Blue1Brown version).",
        "category": "media",
        "tags": ["manim", "manimgl", "3blue1brown", "opengl", "interactive-animation", "python", "math-animation", "video"],
        "risk": "safe",
        "author": "Adithya S Kolavi / Grant Sanderson (3Blue1Brown)",
        "author_url": "https://github.com/3b1b/videos",
        "license": "CC-BY-NC-SA-4.0",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/skills/manimgl-best-practices/LICENSE.txt",
        "notice": f"""# Notices

`manimgl-best-practices` is imported from [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}) at revision `{UPSTREAM_REV}` (origin: `github.com/adithya-s-k/manim_skill @ cef0450`, adapted from `github.com/3b1b/videos`).
Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
Copyright (c) 2025 3Blue1Brown (Grant Sanderson); Copyright (c) 2026 Adithya S Kolavi; see `LICENSE` and `LICENSE.txt`.

## Purpose & Prerequisites

- Interactive animation rules for ManimGL (the OpenGL-accelerated engine used by 3Blue1Brown).
- Covers InteractiveScene, self.frame camera control, interactive development (-se flag), shaders, and checkpoint_paste() workflow.
- Rendering locally requires Python, PyOpenGL, FFmpeg, and ManimGL (`manimgl`).

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static markdown rules, examples, and templates, and writes `.vas-manifest.json`.
No processes are executed and no external services are contacted during installation.
""",
        "vas_notes": f"""

---

## VAS installation notes

- Canonical ID: `manimgl-best-practices`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at commit `{UPSTREAM_REV}` (`skills/manimgl-best-practices/SKILL.md`).
- Authors: Grant Sanderson (3Blue1Brown) and Adithya S Kolavi (`github.com/adithya-s-k/manim_skill @ cef0450`), packaged by sepi2p.
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0); see `LICENSE` and `NOTICE.md`.
- Bundled references: 20 rule files in `rules/`, 76 example scenes in `examples/`, references in `references/`, and templates in `templates/`.
- Install via CLI: `./vas install manimgl-best-practices --target <agent> --mode link` (or `--mode copy`).
""",
    },
    "research-explainer": {
        "name": "research-explainer",
        "description": "Make a scientifically accurate, 3Blue1Brown-style explainer video (and optionally a matching slide deck) about research: a paper, a collection of papers, or the user's own experiments, project or study. Built with Manim Community Edition, Playwright diorama, or HyperFrames vertical shorts. Features real data traceability, motion rules, critique loop, and multi-format templates.",
        "category": "media",
        "tags": ["research-explainer", "manim", "3blue1brown", "video", "science", "paper-to-video", "animation", "slides", "data-visualization"],
        "risk": "safe",
        "author": "sepi2p",
        "author_url": "https://github.com/sepi2p",
        "license": "MIT",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
        "notice": f"""# Notices

`research-explainer` is imported from [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}) at revision `{UPSTREAM_REV}` under the MIT License (Copyright (c) 2026 sepi2p); see `LICENSE`.

## Bundled Third-Party Components

- Inter Font: SIL Open Font License 1.1 (`github.com/rsms/inter`).
- Vazirmatn Font: SIL Open Font License 1.1 (`github.com/rastikerdar/vazirmatn`).
- JetBrains Mono Font: SIL Open Font License 1.1 (`github.com/JetBrains/JetBrainsMono`).
- Caveat Font: SIL Open Font License 1.1 (`github.com/googlefonts/caveat`).
- Sound Effects: CC0 1.0 by Kenney (`kenney.nl`).
- Rough.js 4.6.6: MIT (`github.com/rough-stuff/rough`, patched with seeded PRNG for deterministic rendering).
- Watercolor Paintings: Generated for this skill by the author, released under the repository MIT license.

## Runtime & Tool Prerequisites

- Making full explainer videos with Manim Community Edition requires Python 3.10+, `manim`, FFmpeg, and cairo/pango.
- Optional rendering tools: Playwright for HTML paper dioramas, Piper TTS for free offline narration, or an OpenAI API key for paid voiceover.
- HyperFrames CLI for vertical shorts (optional).

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No scripts, renders, or node processes are executed, no external dependencies or runtimes are installed, and no API services are connected during installation.
""",
        "vas_notes": f"""

---

## VAS installation notes

- Canonical ID: `research-explainer`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at commit `{UPSTREAM_REV}` (`skills/research-explainer/SKILL.md`).
- Author: sepi2p (`https://github.com/sepi2p`).
- License: MIT (Copyright (c) 2026 sepi2p; third-party fonts: SIL OFL 1.1; SFX: CC0 1.0; Rough.js: MIT); see `LICENSE` and `NOTICE.md`.
- Bundled companions: Works with `manim-composer` (scene planning) and `manimce-best-practices` (ManimCE animation rules).
- Bundled contents: `agents/`, `assets/`, `examples/` (`averaging-noise` and `how-a-network-sees`), `promo/`, `references/`, `scripts/` (including `rx.py`), and `templates/` (diorama, short, watercolor-story).
- Install via CLI: `./vas install research-explainer --target <agent> --mode link` (or `--mode copy`).
""",
    },
}

EXECUTABLE_SCRIPTS = {
    "research-explainer": [
        "scripts/rx.py",
        "templates/short/setup.sh",
        "templates/short/work/mix.sh",
        "templates/short/work/stills.sh",
        "templates/diorama/video/render_par.sh",
        "templates/diorama/video/stills.sh",
        "templates/diorama/video/stills_scene.sh",
        "templates/diorama/work/render_part.sh",
        "templates/watercolor-story/setup.sh",
        "templates/watercolor-story/work/mix.sh",
        "templates/watercolor-story/work/empty_room.sh",
        "templates/watercolor-story/work/stills.sh",
    ]
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    file_records = []
    skill_entries = []

    root_license_text = (UPSTREAM_DIR / "LICENSE").read_text(encoding="utf-8")

    for skill_id, cfg in SKILLS_CONFIG.items():
        src_skill_dir = UPSTREAM_DIR / "skills" / skill_id
        dest_dir = REPO_ROOT / "skills" / skill_id
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        # 1. License file
        lic_file = dest_dir / "LICENSE"
        if (src_skill_dir / "LICENSE.txt").exists():
            lic_content = (src_skill_dir / "LICENSE.txt").read_text(encoding="utf-8")
        else:
            lic_content = root_license_text
        lic_file.write_text(lic_content, encoding="utf-8")
        lic_file.chmod(0o644)
        file_records.append({
            "skill_id": skill_id,
            "source_path": f"skills/{skill_id}/LICENSE.txt" if (src_skill_dir / "LICENSE.txt").exists() else "LICENSE",
            "path": f"skills/{skill_id}/LICENSE",
            "sha256": sha256_file(lic_file),
            "executable": False,
        })

        # 2. NOTICE.md
        not_file = dest_dir / "NOTICE.md"
        not_file.write_text(cfg["notice"].strip() + "\n", encoding="utf-8")
        not_file.chmod(0o644)
        file_records.append({
            "skill_id": skill_id,
            "source_path": f"skills/{skill_id}/NOTICE.md",
            "path": f"skills/{skill_id}/NOTICE.md",
            "sha256": sha256_file(not_file),
            "executable": False,
        })

        # 3. Copy all files from upstream skill directory
        for src_path in sorted(src_skill_dir.rglob("*")):
            if src_path.is_dir() or src_path.is_symlink():
                continue
            rel = src_path.relative_to(src_skill_dir)
            dst_path = dest_dir / rel
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if rel.name == "SKILL.md":
                text = src_path.read_text(encoding="utf-8")
                # Format frontmatter
                # Remove existing frontmatter
                lines = text.splitlines()
                if lines and lines[0].strip() == "---":
                    idx = 1
                    while idx < len(lines) and lines[idx].strip() != "---":
                        idx += 1
                    body = "\n".join(lines[idx + 1:]).lstrip()
                else:
                    body = text

                tags_str = json.dumps(cfg["tags"])
                desc_escaped = json.dumps(cfg["description"])
                new_frontmatter = f"""---
name: {cfg["name"]}
description: {desc_escaped}
category: {cfg["category"]}
tags: {tags_str}
risk: {cfg["risk"]}
author: "{cfg["author"]}"
license: "{cfg["license"]}"
source_repo: "{UPSTREAM_REPO}"
source_revision: "{UPSTREAM_REV}"
source_path: "skills/{skill_id}/SKILL.md"
---

"""
                full_content = new_frontmatter + body.rstrip() + cfg["vas_notes"] + "\n"
                dst_path.write_text(full_content, encoding="utf-8")
                dst_path.chmod(0o644)
            else:
                shutil.copy2(src_path, dst_path)

            rel_str = str(rel)
            is_exec = rel_str in EXECUTABLE_SCRIPTS.get(skill_id, [])
            if is_exec:
                dst_path.chmod(0o755)
            else:
                dst_path.chmod(0o644)

            file_records.append({
                "skill_id": skill_id,
                "source_path": f"skills/{skill_id}/{rel}",
                "path": f"skills/{skill_id}/{rel}",
                "sha256": sha256_file(dst_path),
                "executable": is_exec,
            })

        # 4. If research-explainer, also copy examples/ into skills/research-explainer/examples/
        if skill_id == "research-explainer":
            src_examples_dir = UPSTREAM_DIR / "examples"
            dst_examples_dir = dest_dir / "examples"
            for src_path in sorted(src_examples_dir.rglob("*")):
                if src_path.is_dir() or src_path.is_symlink():
                    continue
                rel = src_path.relative_to(src_examples_dir)
                dst_path = dst_examples_dir / rel
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                dst_path.chmod(0o644)
                file_records.append({
                    "skill_id": skill_id,
                    "source_path": f"examples/{rel}",
                    "path": f"skills/{skill_id}/examples/{rel}",
                    "sha256": sha256_file(dst_path),
                    "executable": False,
                })

        skill_entries.append({
            "id": skill_id,
            "canonical_id": skill_id,
            "name": cfg["name"],
            "path": f"skills/{skill_id}",
            "description": cfg["description"],
            "category": cfg["category"],
            "tags": cfg["tags"],
            "risk": cfg["risk"],
            "author": cfg["author"],
            "author_url": cfg["author_url"],
            "source": f"https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV}/skills/{skill_id}",
            "source_repo": UPSTREAM_REPO,
            "source_revision": UPSTREAM_REV,
            "source_path": f"skills/{skill_id}/SKILL.md",
            "license": cfg["license"],
            "license_source": cfg["license_source"],
        })
        print(f"Packaged {skill_id}: {len([f for f in file_records if f['skill_id'] == skill_id])} files")

    # Write data/research-explainer-import.json
    import_manifest = {
        "source_repo": UPSTREAM_REPO,
        "source_url": f"https://github.com/{UPSTREAM_REPO}",
        "revision": UPSTREAM_REV,
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "license": "MIT / CC-BY-NC-SA-4.0",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/THIRD_PARTY.md",
        "skill_count": len(skill_entries),
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3885,
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
            "collision_rationale": "Exact and high-similarity comparison against all 3,885 catalog skills identified zero existing duplicates. All 4 skills (manim-composer, manimce-best-practices, manimgl-best-practices, and research-explainer) provide an entirely new research-to-explainer video and mathematical animation pipeline.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, references/, rules/, examples/, templates/, and scripts/ under Open Agent Skills format.",
            "Bundle complete worked examples (averaging-noise, how-a-network-sees) directly inside skills/research-explainer/examples/ for standalone execution.",
            "Append reversible VAS installation, attribution, prerequisites, and safety notes to SKILL.md for each skill.",
            "Include upstream LICENSE and add NOTICE.md clarifying standalone operation, third-party component licenses, and runtime prerequisites.",
            "Preserve executable bits (0755) on shell and Python execution scripts.",
            "Map all 4 skills to the existing media category (119 existing categories preserved).",
            "No runtime, dependency, or external service is executed during installation.",
        ],
        "skills": skill_entries,
        "files": file_records,
    }

    manifest_path = REPO_ROOT / "data" / "research-explainer-import.json"
    manifest_path.write_text(json.dumps(import_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote import manifest to {manifest_path}")

    # Update data/source-credits.json
    credits_path = REPO_ROOT / "data" / "source-credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8"))
    credits["sections"]["researchexplainer"] = [
        f"- **[sepi2p/research-explainer-skill](https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV})**: Research-to-video explainer pipeline and Manim animation collection by {AUTHOR} (with companion Manim skills by Adithya S Kolavi and Grant Sanderson) at revision `{UPSTREAM_REV}`.",
        "- Provides 4 modular skills for creating scientifically accurate, 3Blue1Brown-style explainer videos and animations: `research-explainer` (paper-to-video orchestrator, paper diorama, and vertical shorts), `manim-composer` (scene planning and storyboard specifications), `manimce-best-practices` (Manim Community Edition animation rules), and `manimgl-best-practices` (ManimGL interactive OpenGL rules).",
        "- Standalone payloads preserve upstream Agent Skills specification SKILL.md, 45+ rule files, 80+ example scenes, templates, audio synthesis scripts, and full worked examples (`averaging-noise` and `how-a-network-sees`).",
        "- Licensing: Root is MIT; `manimgl-best-practices` is licensed under CC BY-NC-SA 4.0; bundled fonts under SIL Open Font License 1.1; sound effects under CC0 1.0; see individual LICENSE and NOTICE.md files.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed, and no external accounts are connected.",
    ]
    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {credits_path}")

    # Update data/catalog.json
    cat_path = REPO_ROOT / "data" / "catalog.json"
    cat_data = json.loads(cat_path.read_text(encoding="utf-8"))
    imported_ids = {s["id"] for s in skill_entries}
    existing_skills = [s for s in cat_data["skills"] if s["id"] not in imported_ids]
    existing_skills.extend(skill_entries)
    existing_skills.sort(key=lambda x: x["id"])
    cat_data["skills"] = existing_skills
    cat_data["total"] = len(existing_skills)
    cat_path.write_text(json.dumps(cat_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {cat_path} with total {len(existing_skills)} skills.")


if __name__ == "__main__":
    main()
