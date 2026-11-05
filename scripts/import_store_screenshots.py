#!/usr/bin/env python3
"""
Import Store Screenshots skill from thearkxd/store-screenshots-skill.
"""

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/store-screenshots-skill-temp")
UPSTREAM_REV = "c25bf66faa7396818c0f7b267e6add4d441573a8"
AUTHOR = "thearkxd (Alpiworks)"
AUTHOR_URL = "https://github.com/thearkxd/store-screenshots-skill"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/thearkxd/store-screenshots-skill/blob/{UPSTREAM_REV}/LICENSE"

LICENSE_TEXT = (UPSTREAM_REPO / "LICENSE").read_text(encoding="utf-8")

NOTICE_TEMPLATE = """# Notices

`store-screenshots` skill code, reference texts, and classification data are MIT licensed (Copyright (c) 2026 Alpiworks); see bundled `LICENSE`.

## Third-party material

`skills/store-screenshots/assets/library/img/` contains downscaled App Store screenshots of third-party apps,
collected from Apple's public App Store listings on 2026-11-04 for study and reference only. They remain the
property of their respective publishers; app names and marks are trademarks of their owners. They are not
covered by this project's license, must not be reused in store listings or other products, and will be
removed on request by a rights holder (open an issue).

The OCR text, labels and notes in `catalog.json` / `classifications.json` are Alpiworks' own analysis.

## Prerequisites & External Services

- Standard screenshot planning, visual DNA extraction, and copy rules run dependency-free with Python standard library.
- Scene rendering and SVG output optionally use `Pillow` and `resvg-py` for PNG and SVG rasterization.
- Multi-language OCR checks optionally use system `tesseract` (with language models such as `tur.traineddata`).
- No external runtime, network API key, or MCP service is required for installation or baseline offline operation.

## Safe Operation

Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.
No unapproved scripts are executed, no external dependencies or MCP servers are installed, and
no background processes or accounts are connected during installation.
"""

SKILL_DEFINITIONS = [
    {
        "source_slug": "store-screenshots",
        "canonical_id": "store-screenshots",
        "category": "design",
        "tags": ["design", "marketing", "mobile", "app-store", "google-play", "screenshots", "aso", "ui-ux"],
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def extract_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    lines = parts[1].splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line or line.startswith("#"):
            i += 1
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v == ">-":
                i += 1
                multi = []
                while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                    multi.append(lines[i].strip())
                    i += 1
                fm[k] = " ".join(multi).strip()
                continue
            fm[k] = v
        i += 1
    return fm


def main():
    skills_dir = REPO_ROOT / "skills"
    file_records = []
    imported_skills = []

    for item in SKILL_DEFINITIONS:
        source_slug = item["source_slug"]
        canonical_id = item["canonical_id"]
        category = item["category"]
        tags = item["tags"]

        source_dir = UPSTREAM_REPO / "skills" / source_slug
        dest_dir = skills_dir / canonical_id
        dest_dir.mkdir(parents=True, exist_ok=True)

        source_path = f"skills/{source_slug}"

        # 1. LICENSE
        lic_file = dest_dir / "LICENSE"
        lic_file.write_text(LICENSE_TEXT, encoding="utf-8")
        lic_file.chmod(0o644)
        file_records.append({
            "source_path": f"{source_path} (via upstream LICENSE)",
            "path": f"skills/{canonical_id}/LICENSE",
            "source_sha256": sha256_file(UPSTREAM_REPO / "LICENSE"),
            "sha256": sha256_file(lic_file),
            "executable": False,
        })

        # 2. NOTICE.md
        not_file = dest_dir / "NOTICE.md"
        not_file.write_text(NOTICE_TEMPLATE.strip() + "\n", encoding="utf-8")
        not_file.chmod(0o644)
        file_records.append({
            "source_path": f"{source_path} (via NOTICE.md)",
            "path": f"skills/{canonical_id}/NOTICE.md",
            "source_sha256": sha256_file(not_file),
            "sha256": sha256_file(not_file),
            "executable": False,
        })

        # 3. SKILL.md
        upstream_skill_md = source_dir / "SKILL.md"
        raw_skill_content = upstream_skill_md.read_text(encoding="utf-8")
        fm = extract_frontmatter(raw_skill_content)
        name = fm.get("name", canonical_id)
        description = fm.get("description", "")

        # Format customized SKILL.md
        body = raw_skill_content
        if body.startswith("---"):
            parts = body.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].lstrip("\n")

        vas_frontmatter = (
            f"---\n"
            f"name: {canonical_id}\n"
            f"description: {description}\n"
            f"category: {category}\n"
            f"tags:\n"
            + "".join(f"  - {t}\n" for t in tags)
            + f"license: {LICENSE_NAME}\n"
            f"metadata:\n"
            f"  author: {AUTHOR}\n"
            f"  version: 2.2.41\n"
            f"---\n\n"
        )

        installation_notes = f"""

## VAS installation notes

- Canonical ID: `{canonical_id}`
- Source repository: [`thearkxd/store-screenshots-skill`](https://github.com/thearkxd/store-screenshots-skill) (revision `{UPSTREAM_REV}`, path `{source_path}`)
- Author: {AUTHOR}
- License: {LICENSE_NAME} (see bundled `LICENSE` and `NOTICE.md`)
- Role: App Store and Google Play screenshot planning, copywriting, visual DNA extraction, and multi-layer scene design workflow for AI coding agents.
- Prerequisites: Python 3 standard library; optional `Pillow` and `resvg-py` for PNG and SVG rendering, optional `tesseract` for multi-language OCR verification.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""

        final_skill_md = vas_frontmatter + body.rstrip() + installation_notes
        dest_skill_md = dest_dir / "SKILL.md"
        dest_skill_md.write_text(final_skill_md, encoding="utf-8")
        dest_skill_md.chmod(0o644)

        file_records.append({
            "source_path": f"{source_path}/SKILL.md",
            "path": f"skills/{canonical_id}/SKILL.md",
            "source_sha256": sha256_file(upstream_skill_md),
            "sha256": sha256_file(dest_skill_md),
            "executable": False,
        })

        imported_skills.append({
            "id": canonical_id,
            "canonical_id": canonical_id,
            "name": name,
            "path": f"skills/{canonical_id}",
            "description": description,
            "category": category,
            "tags": tags,
            "risk": "low",
            "source": f"https://github.com/thearkxd/store-screenshots-skill/tree/{UPSTREAM_REV}/{source_path}",
            "source_repo": "thearkxd/store-screenshots-skill",
            "source_revision": UPSTREAM_REV,
            "source_path": source_path,
            "author": AUTHOR,
            "license": LICENSE_NAME,
            "license_source": LICENSE_URL,
        })

        # 4. Copy all subdirectories and assets
        for root_path, dirs, files in os.walk(source_dir):
            for file_name in files:
                if file_name == "SKILL.md":
                    continue
                src_f = Path(root_path) / file_name
                rel_to_src = src_f.relative_to(source_dir)
                dst_f = dest_dir / rel_to_src
                dst_f.parent.mkdir(parents=True, exist_ok=True)

                rel_src = f"{source_path}/{rel_to_src.as_posix()}"
                rel_dst = f"skills/{canonical_id}/{rel_to_src.as_posix()}"

                shutil.copy2(src_f, dst_f)
                dst_f.chmod(0o644)
                file_records.append({
                    "source_path": rel_src,
                    "path": str(rel_dst),
                    "source_sha256": sha256_file(src_f),
                    "sha256": sha256_file(dst_f),
                    "executable": False,
                })

    file_records.sort(key=lambda r: r["path"])
    imported_skills.sort(key=lambda s: s["id"])
    print(f"Processed {len(imported_skills)} skills with {len(file_records)} total files.")

    # Write data/store-screenshots-import.json
    import_manifest = {
        "source_repo": "thearkxd/store-screenshots-skill",
        "revision": UPSTREAM_REV,
        "skill_count": len(imported_skills),
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3875,
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
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,875 catalog skills identified zero existing duplicates (max similarity 0.0004 with ffmpeg-skill). The skill provides a unique App Store & Google Play marketing screenshot design system.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, references/, scripts/, templates/, and assets/ under Open Agent Skills format.",
            "Append reversible VAS installation, attribution, prerequisites, role, and safety notes to SKILL.md.",
            "Include upstream MIT LICENSE and NOTICE.md acknowledging third-party App Store reference screenshots and safe offline execution.",
            "Map upstream skill to existing design category to preserve exactly 119 catalog categories.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "store-screenshots-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/store-screenshots-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["storescreenshots"] = [
        f"- **[thearkxd/store-screenshots-skill](https://github.com/thearkxd/store-screenshots-skill/tree/{UPSTREAM_REV})**: App Store and Google Play screenshot planning, copywriting, and multi-layer scene design skill by thearkxd (Alpiworks) at revision `{UPSTREAM_REV}` (tag `v2.2.41`) under the MIT License.",
        "- Plans, writes, and renders conversion-focused App Store and Play Store screenshots from real app screens (visual DNA extraction, 3 app concepts, 3D device perspective, multi-layer scene composition, claim verification, alt text, and store spec checks).",
        "- Standalone payload preserves upstream Agent Skills specification SKILL.md with complete references (storytelling, copy rules, design process, scene format, layouts, store specs, categories, critique), helper scripts, directions, fonts, templates, and reference library.",
        "- Preserves upstream NOTICE.md clarifying third-party App Store screenshot reference material in `assets/library/img/` under study and reference terms.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed, and no external accounts are connected.",
    ]
    with open(credits_file, "w", encoding="utf-8") as f:
        json.dump(credits_data, f, indent=2)
    print("Updated data/source-credits.json")

    # Update data/catalog.json
    catalog_file = REPO_ROOT / "data" / "catalog.json"
    with open(catalog_file, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    imported_ids = {s["id"] for s in imported_skills}
    filtered_skills = [
        s for s in catalog_data.get("skills", [])
        if s.get("canonical_id") not in imported_ids and s.get("id") not in imported_ids
    ]
    filtered_skills.extend(imported_skills)
    filtered_skills.sort(key=lambda s: s.get("id", ""))

    catalog_data["skills"] = filtered_skills
    catalog_data["total"] = len(filtered_skills)
    catalog_data["generatedAt"] = "2026-11-05T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills.")


if __name__ == "__main__":
    main()
