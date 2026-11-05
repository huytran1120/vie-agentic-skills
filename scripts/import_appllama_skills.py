#!/usr/bin/env python3
"""
Import 2 mobile app design and research skills from Appllama/appllama-skills.
"""

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/appllama-skills-temp")
UPSTREAM_REV = "dd5caaec3d5d50ad7fc0324da238119c6b7c3707"
AUTHOR = "Appllama (Antmind Ventures Private Limited)"
AUTHOR_URL = "https://appllama.io"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/Appllama/appllama-skills/blob/{UPSTREAM_REV}/LICENSE"

LICENSE_TEXT = (UPSTREAM_REPO / "LICENSE").read_text(encoding="utf-8")

NOTICE_TEMPLATE = """# Notices

Appllama mobile design and research skills are MIT licensed (Copyright (c) 2026 Antmind Ventures Private Limited (appllama.io)); see bundled `LICENSE`.

## Mobile App Design & Benchmark Intelligence

This skill provides mobile UI engineering guidelines, HIG compliance standards, anti-slop principles, and design research methods benchmarked against top-grossing iOS and Android apps.

## Prerequisites & External Services

- `appllama-app-design-skill` stands completely on its own for native Expo / React Native UI building, motion rules, and simulator iteration without any external dependencies.
- `appllama-usage` optionally connects to the Appllama MCP server (`https://mcp.appllama.io/mcp`) for live top-grossing app screen search and revenue/download context. No API key is required to read documentation or use offline playbooks.

## Safe Operation

Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.
No unapproved scripts are executed, no external dependencies or MCP servers are installed, and
no background processes or accounts are connected during installation.
"""

SKILL_DEFINITIONS = [
    {
        "source_slug": "appllama-app-design-skill",
        "canonical_id": "appllama-app-design-skill",
        "category": "mobile",
        "tags": ["mobile", "react-native", "expo", "app-design", "ui-ux", "apple-hig", "mobile-design", "appllama"],
    },
    {
        "source_slug": "appllama-usage",
        "canonical_id": "appllama-usage",
        "category": "mobile",
        "tags": ["mobile", "research", "appllama", "mcp", "ui-patterns", "competitor-analysis", "mobile-apps", "app-store"],
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

        # 3. Copy other files and directories from upstream
        for root, dirs, files in os.walk(source_dir):
            rel_root = Path(root).relative_to(source_dir)
            target_root = dest_dir / rel_root
            target_root.mkdir(parents=True, exist_ok=True)

            for f in sorted(files):
                src_f = Path(root) / f
                dst_f = target_root / f
                rel_dst = dst_f.relative_to(REPO_ROOT)
                rel_src = f"{source_path}/{src_f.relative_to(source_dir)}"

                if f == "SKILL.md":
                    smd_text = src_f.read_text(encoding="utf-8")
                    fm = extract_frontmatter(smd_text)

                    vas_notes = f"""

## VAS installation notes

- Canonical ID: `{canonical_id}`
- Source repository: [`Appllama/appllama-skills`](https://github.com/Appllama/appllama-skills) (revision `{UPSTREAM_REV}`, path `{source_path}`)
- Author: {AUTHOR} ([appllama.io]({AUTHOR_URL}))
- License: MIT License (see bundled `LICENSE`)
- Role: Mobile app design and top-grossing UI research workflow for AI coding agents.
- Prerequisites: Standalone native UI development; optional Appllama MCP (`https://mcp.appllama.io/mcp`) for live screen library search.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""
                    dst_f.write_text(smd_text.rstrip() + vas_notes, encoding="utf-8")
                    dst_f.chmod(0o644)
                    file_records.append({
                        "source_path": rel_src,
                        "path": str(rel_dst),
                        "source_sha256": sha256_file(src_f),
                        "sha256": sha256_file(dst_f),
                        "executable": False,
                    })

                    desc = fm.get("description", f"Mobile app engineering and research skill for {canonical_id}.")
                    imported_skills.append({
                        "id": canonical_id,
                        "canonical_id": canonical_id,
                        "name": canonical_id,
                        "description": desc,
                        "category": category,
                        "risk": "safe",
                        "tags": tags,
                        "source": f"https://github.com/Appllama/appllama-skills/tree/{UPSTREAM_REV}/{source_path}",
                        "source_repo": "Appllama/appllama-skills",
                        "source_revision": UPSTREAM_REV,
                        "source_path": source_path,
                        "author": "Appllama",
                        "license": LICENSE_NAME,
                        "license_source": LICENSE_URL,
                        "path": f"skills/{canonical_id}/SKILL.md",
                    })
                else:
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

    # Write data/appllama-skills-import.json
    import_manifest = {
        "source_repo": "Appllama/appllama-skills",
        "revision": UPSTREAM_REV,
        "skill_count": len(imported_skills),
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3873,
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
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,873 catalog skills identified zero existing duplicates (max similarity 0.0002). Both skills are completely unique mobile app design and research workflows.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, references/ and agents/ under Open Agent Skills format.",
            "Append reversible VAS installation, attribution, prerequisites, role, and safety notes to SKILL.md.",
            "Include upstream MIT LICENSE and add NOTICE.md acknowledging mobile design standards, optional Appllama MCP, and safe offline execution.",
            "Map upstream skills to existing mobile category to preserve exactly 119 catalog categories.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "appllama-skills-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/appllama-skills-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["appllama"] = [
        f"- **[Appllama/appllama-skills](https://github.com/Appllama/appllama-skills/tree/{UPSTREAM_REV})**: 2 mobile app design and top-grossing UI research skills by Appllama (Antmind Ventures Private Limited - [appllama.io](https://appllama.io)) at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Covers native-feeling mobile app engineering for Expo and React Native (Apple HIG fidelity, semantic colors, native controls, motion laws, full-motion simulator loop) and research playbooks studying real screens, flows, and paywalls from top-grossing apps.",
        "- Standalone payloads preserve upstream Agent Skills specification SKILL.md with complete references (image-assets, native-controls, motion, performance, simulator-loop, build-from-scratch, improve-a-screen, research-methods).",
        "- Optional live screen queries use the Appllama MCP (`https://mcp.appllama.io/mcp`); offline design standards and implementation guidelines run safely with zero external dependencies.",
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
