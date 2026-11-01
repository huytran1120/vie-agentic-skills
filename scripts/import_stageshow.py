#!/usr/bin/env python3
"""
Import the Stageshow skill from benjitaylor/skills.
"""

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_ROOT = Path("/tmp/benjitaylor-skills/stageshow")
UPSTREAM_REV = "802057409787133703c56001080169e347305572"
AUTHOR = "Benji Taylor"
AUTHOR_URL = "https://github.com/benjitaylor"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/benjitaylor/skills/blob/{UPSTREAM_REV}/stageshow/LICENSE"

VAS_NOTES = """

## VAS installation notes

- Canonical ID: `stageshow`
- Source repository: [`benjitaylor/skills`](https://github.com/benjitaylor/skills) (revision `802057409787133703c56001080169e347305572`, path `stageshow`)
- Author: Benji Taylor ([@benjitaylor](https://github.com/benjitaylor))
- License: MIT License (see bundled `LICENSE`)
- Third-party assets & notices: See bundled `NOTICE.md`
- Standalone payload: Includes complete portable React `kit/`, gold `examples/`, flawed/corrected `teaching/` pairs, `references/`, local SVG icon and brand assets, verification `scripts/`, and Vite `playground/`.
- Prerequisites: Node.js 20.19+ and React 18+ in your application. Optional dev dependencies (Vite, Playwright, PostCSS) for local preview and filming.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    dest_dir = REPO_ROOT / "skills" / "stageshow"
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    file_records = []
    for src_path in sorted(UPSTREAM_ROOT.rglob("*")):
        if src_path.is_dir() or src_path.is_symlink():
            continue
        rel = src_path.relative_to(UPSTREAM_ROOT)
        dst_path = dest_dir / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        src_sha = sha256_file(src_path)

        if rel.as_posix() == "SKILL.md":
            content = src_path.read_text(encoding="utf-8")
            if "## VAS installation notes" not in content:
                content = content.rstrip() + VAS_NOTES
            dst_path.write_text(content, encoding="utf-8")
        else:
            shutil.copy2(src_path, dst_path)

        dst_sha = sha256_file(dst_path)

        # Ensure standard permissions (non-executable)
        dst_path.chmod(0o644)

        file_records.append({
            "source_path": rel.as_posix(),
            "path": f"skills/stageshow/{rel.as_posix()}",
            "source_sha256": src_sha,
            "sha256": dst_sha,
            "executable": False,
        })

    print(f"Copied {len(file_records)} files to skills/stageshow.")

    # Write data/stageshow-import.json
    import_manifest = {
        "source_repo": "benjitaylor/skills",
        "revision": UPSTREAM_REV,
        "skill_count": 1,
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3353,
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
            "collision_rationale": "No collision found across all 3,353 catalog skills. stageshow is a unique, genuine new addition for mock UI, cursor animations, and product walkthroughs.",
        },
        "adaptations": [
            "Preserve upstream payload structure: kit, examples, teaching pairs, references, assets, verification scripts, and playground.",
            "Append reversible VAS installation, attribution, prerequisites and safety notes to SKILL.md.",
            "Preserve original MIT LICENSE, NOTICE.md, and local SVG brand assets.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "stageshow-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/stageshow-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["stageshow"] = [
        f"- **[benjitaylor/skills](https://github.com/benjitaylor/skills/tree/{UPSTREAM_REV}/stageshow)**: Stageshow \u2014 mock UI, product walkthroughs, animated cursor demos, and React kit by Benji Taylor ([@benjitaylor](https://github.com/benjitaylor)) at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Standalone payload includes `kit/`, gold `examples/`, `teaching/` pairs, `references/`, local SVG brand/icon assets, verification scripts, and local Vite playground. Third-party brand artwork and example marks are documented in `NOTICE.md`.",
        "- Installation runs no code, installs no dependencies or MCP servers, and connects no external accounts. Node.js 20.19+ and optional dev dependencies (Vite, Playwright, PostCSS) are separate user prerequisites.",
    ]
    with open(credits_file, "w", encoding="utf-8") as f:
        json.dump(credits_data, f, indent=2)
    print("Updated data/source-credits.json")

    # Update data/catalog.json
    catalog_file = REPO_ROOT / "data" / "catalog.json"
    with open(catalog_file, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    filtered_skills = [
        s for s in catalog_data.get("skills", [])
        if s.get("canonical_id") != "stageshow" and s.get("id") != "stageshow"
    ]

    skill_entry = {
        "id": "stageshow",
        "canonical_id": "stageshow",
        "name": "stageshow",
        "description": "Build faux product UI that looks like a real product, as a still illustration or an animated demo with a cursor. Browser and app windows, dashboards, phones, notifications, terminals, bento grids and cursor walkthroughs, framed, masked and cropped the way a marketing page, feature card or docs hero needs them. Use whenever someone wants a fake or mocked UI, a product demo or walkthrough animation, a hero or feature-card illustration of an app, a product shot in the style of a polished marketing site, or an animated cursor doing things in an interface, even if they never say \"faux UI\". React and plain CSS.",
        "category": "frontend",
        "risk": "safe",
        "tags": [
            "frontend",
            "ui",
            "react",
            "motion",
            "product-design",
            "illustrations",
            "demo",
            "stageshow",
        ],
        "source": f"https://github.com/benjitaylor/skills/tree/{UPSTREAM_REV}/stageshow",
        "source_repo": "benjitaylor/skills",
        "source_revision": UPSTREAM_REV,
        "source_path": "stageshow/SKILL.md",
        "author": AUTHOR,
        "license": LICENSE_NAME,
        "license_source": LICENSE_URL,
        "path": "skills/stageshow/SKILL.md",
    }
    filtered_skills.append(skill_entry)

    catalog_data["skills"] = filtered_skills
    catalog_data["total"] = len(filtered_skills)
    catalog_data["generatedAt"] = "2026-11-01T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills (added stageshow).")


if __name__ == "__main__":
    main()
