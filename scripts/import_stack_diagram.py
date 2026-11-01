#!/usr/bin/env python3
"""
Import the stack-diagram skill from caru-ini/stack-diagram.
"""

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/stack-diagram")
UPSTREAM_SKILL = UPSTREAM_REPO / "skills" / "stack-diagram"
UPSTREAM_REV = "75dbd3e3c6fe28844322e6064d3a947b870a6c61"
AUTHOR = "caru-ini"
AUTHOR_URL = "https://github.com/caru-ini"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/caru-ini/stack-diagram/blob/{UPSTREAM_REV}/LICENSE"

VAS_NOTES = """

## VAS installation notes

- Canonical ID: `stack-diagram`
- Source repository: [`caru-ini/stack-diagram`](https://github.com/caru-ini/stack-diagram) (revision `75dbd3e3c6fe28844322e6064d3a947b870a6c61`, path `skills/stack-diagram`)
- Author: caru-ini ([@caru-ini](https://github.com/caru-ini))
- License: MIT License (see bundled `LICENSE`)
- Third-party assets & notices: See bundled `NOTICE.md` and font licenses in `assets/fonts/`
- Standalone payload: Includes complete `assets/` (template HTML, generic SVGs, self-contained Geist and JetBrains Mono fonts), reference guides (`geometry.md`, `tsx.md`), and build/render/fetch scripts (`build.py`, `fetch_icons.py`, `render_png.py`).
- Prerequisites: Python 3.9+ (standard library only for `build.py` and `fetch_icons.py`). Optional Playwright with Chromium for headless PNG export (`render_png.py`).
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""

NOTICE_CONTENT = """# Notices

`stack-diagram` source code is MIT licensed (Copyright (c) 2026 caru-ini); see `LICENSE`.

## Bundled fonts

The fonts in `assets/fonts/` (`Geist.woff2` and `JetBrainsMono.woff2`) are not covered by the MIT license;
they are licensed under the SIL Open Font License 1.1.
See `assets/fonts/OFL-Geist.txt` and `assets/fonts/OFL-JetBrainsMono.txt`.

## Third-party brand logos and trademarks

Brand names, official cloud logos, service marks, and technologies mentioned or fetched during diagram generation
are trademarks of their respective owners. Their use in architecture diagrams is illustrative and does not imply
affiliation or endorsement.
Logos are not bundled with the skill payload. They are downloaded on demand at build time unmodified from:
- [svgl](https://svgl.app) (MIT)
- [devicon](https://devicon.dev) (MIT)
- [gilbarbara/logos](https://github.com/gilbarbara/logos) (CC0 1.0)
- [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)
- Official brand websites or repositories
"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    dest_dir = REPO_ROOT / "skills" / "stack-diagram"
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    file_records = []

    # 1. Copy all files from UPSTREAM_SKILL
    for src_path in sorted(UPSTREAM_SKILL.rglob("*")):
        if src_path.is_dir():
            continue
        rel = src_path.relative_to(UPSTREAM_SKILL)
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
        dst_path.chmod(0o644)

        file_records.append({
            "source_path": rel.as_posix(),
            "path": f"skills/stack-diagram/{rel.as_posix()}",
            "source_sha256": src_sha,
            "sha256": dst_sha,
            "executable": False,
        })

    # 2. Add NOTICE.md
    notice_path = dest_dir / "NOTICE.md"
    notice_path.write_text(NOTICE_CONTENT.strip() + "\n", encoding="utf-8")
    notice_path.chmod(0o644)
    file_records.append({
        "source_path": "NOTICE.md",
        "path": "skills/stack-diagram/NOTICE.md",
        "source_sha256": sha256_file(notice_path),
        "sha256": sha256_file(notice_path),
        "executable": False,
    })

    # 3. Add README.md from upstream root
    readme_upstream = UPSTREAM_REPO / "README.md"
    if readme_upstream.exists():
        readme_dst = dest_dir / "README.md"
        shutil.copy2(readme_upstream, readme_dst)
        readme_dst.chmod(0o644)
        file_records.append({
            "source_path": "README.md",
            "path": "skills/stack-diagram/README.md",
            "source_sha256": sha256_file(readme_upstream),
            "sha256": sha256_file(readme_dst),
            "executable": False,
        })

    file_records.sort(key=lambda r: r["path"])
    print(f"Copied {len(file_records)} files to skills/stack-diagram.")

    # Write data/stack-diagram-import.json
    import_manifest = {
        "source_repo": "caru-ini/stack-diagram",
        "revision": UPSTREAM_REV,
        "skill_count": 1,
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3354,
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
            "collision_rationale": "No collision found across all 3,354 catalog skills. stack-diagram is a unique, genuine new addition for cloud-architecture-style system diagrams, infra topologies, and tech stack overviews.",
        },
        "adaptations": [
            "Preserve upstream payload structure: assets/ (template HTML, generic SVGs, OFL fonts), references/ (geometry, TSX), and scripts/ (build, fetch_icons, render_png).",
            "Append reversible VAS installation, attribution, prerequisites and safety notes to SKILL.md.",
            "Include upstream MIT LICENSE, add comprehensive NOTICE.md, and include upstream README.md.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "stack-diagram-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/stack-diagram-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["stackdiagram"] = [
        f"- **[caru-ini/stack-diagram](https://github.com/caru-ini/stack-diagram/tree/{UPSTREAM_REV})**: Stack Diagram — cloud-architecture-style diagrams for tech stacks, systems, and infra with official brand logos by caru-ini ([@caru-ini](https://github.com/caru-ini)) at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Standalone payload includes `assets/` (HTML template, generic SVGs, OFL 1.1 fonts), `references/` (geometry, TSX), and scripts (`build.py`, `fetch_icons.py`, `render_png.py`). Third-party marks and font licenses are documented in `NOTICE.md`.",
        "- Installation runs no code, installs no dependencies or MCP servers, and connects no external accounts. Python 3.9+ and optional Playwright are separate user prerequisites.",
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
        if s.get("canonical_id") != "stack-diagram" and s.get("id") != "stack-diagram"
    ]

    skill_entry = {
        "id": "stack-diagram",
        "canonical_id": "stack-diagram",
        "name": "stack-diagram",
        "description": "Create cloud-architecture-style diagrams of tech stacks, system architectures, infra layouts, and service topologies — with real brand logos, grouped containers, and clean orthogonal arrows — delivered as self-contained HTML, a PNG image, a React/TSX component, or a live artifact. Use this skill whenever the user asks for an architecture / system / stack / infra diagram, a tech-stack overview, a service topology, a cloud-vendor-style diagram, or wants tech logos arranged into a picture of how their services connect — in any language, even if they don't name an output format, and even if the tools involved aren't cloud services.",
        "category": "architecture",
        "risk": "safe",
        "tags": [
            "architecture",
            "diagram",
            "infra",
            "cloud",
            "system-design",
            "stack-diagram",
            "svg",
            "html",
        ],
        "source": f"https://github.com/caru-ini/stack-diagram/tree/{UPSTREAM_REV}/skills/stack-diagram",
        "source_repo": "caru-ini/stack-diagram",
        "source_revision": UPSTREAM_REV,
        "source_path": "skills/stack-diagram/SKILL.md",
        "author": AUTHOR,
        "license": LICENSE_NAME,
        "license_source": LICENSE_URL,
        "path": "skills/stack-diagram/SKILL.md",
    }
    filtered_skills.append(skill_entry)

    catalog_data["skills"] = filtered_skills
    catalog_data["total"] = len(filtered_skills)
    catalog_data["generatedAt"] = "2026-11-01T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills (added stack-diagram).")


if __name__ == "__main__":
    main()
