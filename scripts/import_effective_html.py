#!/usr/bin/env python3
"""
Import Effective HTML skills from plannotator/effective-html.
"""

import hashlib
import json
import os
from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/effective-html-temp")
UPSTREAM_REV = "5ce160a3e76dc1c0f9301f8a1903704ec607636a"
AUTHOR = "Plannotator"
AUTHOR_URL = "https://github.com/plannotator/effective-html"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/plannotator/effective-html/blob/{UPSTREAM_REV}/LICENSE"

LICENSE_TEXT = (UPSTREAM_REPO / "LICENSE").read_text(encoding="utf-8")

NOTICE_TEMPLATE = """# Notices

Effective HTML skills are MIT licensed (Copyright (c) 2026 plannotator); see bundled `LICENSE`.

## Effective HTML Artifacts & Creative Direction

This skill provides focused agent workflows for self-contained, pragmatic visual HTML artifacts (wireframes, prototypes, mockups, plans, diagrams, one-pagers, and design direction) adhering to the Open Agent Skills specification.

## Prerequisites & External Services

- The skill operates completely offline and self-contained without mandatory runtime or API dependencies.
- Render and inspect generated HTML files in any modern web browser or local previewer.
- Optional integration with Plannotator (`https://github.com/backnotprop/plannotator`) for local visual annotation and feedback.

## Safe Operation

Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.
No unapproved scripts are executed, no external dependencies or MCP servers are installed, and
no background processes or accounts are connected during installation.
"""

SKILL_DEFINITIONS = [
    {
        "source_slug": "big-pics-little-words",
        "canonical_id": "big-pics-little-words",
        "category": "design",
        "tags": ["design", "html", "visual-explanation", "communication", "one-pager", "effective-html"],
        "disable_model_invocation": True,
        "description": "Explain the current subject in HTML with large visuals and minimal text while preserving key details. Use when the user asks to explain a concept visually with big pictures and little words in self-contained HTML.",
        "role": "Visual explanation and concise visual summary workflow in self-contained HTML for AI coding agents."
    },
    {
        "source_slug": "design-artifact",
        "canonical_id": "design-artifact",
        "category": "design",
        "tags": ["design", "html", "creative-direction", "typography", "palette", "effective-html"],
        "disable_model_invocation": False,
        "description": "Design principles and creative direction for building HTML artifacts — pages, reports, plans, landing pages, demos, decks, and small tools. Use when creating or restyling any visual HTML deliverable and deciding its palette, type pairing, layout, theming, or overall register, or when the output must not look generically AI-generated.",
        "role": "Creative direction, typography pairing, palette selection, and register sizing workflow for visual HTML deliverables."
    },
    {
        "source_slug": "html",
        "canonical_id": "html",
        "category": "design",
        "tags": ["html", "design", "frontend", "web", "artifacts", "router", "effective-html"],
        "disable_model_invocation": False,
        "description": "Create or redesign self-contained single-file HTML artifacts with a visual direction shaped by the user's brief, project, and subject. Use when HTML is the deliverable for a report, explainer, landing page, presentation, tool, mixed artifact, or broad request. Routes clear wireframe, prototype, mockup, plan, or diagram requests to the matching direct-invocation specialist.",
        "role": "Primary router and deliverable creator for self-contained single-file HTML artifacts and presentations."
    },
    {
        "source_slug": "html-diagram",
        "canonical_id": "html-diagram",
        "category": "design",
        "tags": ["diagram", "html", "architecture", "sequence", "topology", "state-machine", "design", "effective-html"],
        "disable_model_invocation": False,
        "description": "Direct-invocation specialist for self-contained HTML diagrams whose layout, notation, and interaction clarify relationships, sequence, topology, state, hierarchy, or quantitative structure. Use when the user explicitly invokes html-diagram or the broad html skill routes a diagram request here.",
        "role": "Visual diagrams and interactive system topology design in self-contained HTML."
    },
    {
        "source_slug": "html-plan",
        "canonical_id": "html-plan",
        "category": "design",
        "tags": ["planning", "html", "roadmap", "rollout", "implementation", "design", "effective-html"],
        "disable_model_invocation": False,
        "description": "Direct-invocation specialist for clear, self-contained HTML plans that preserve source material while improving hierarchy, sequence, ownership, dependencies, and reviewability. Use when the user explicitly invokes html-plan or the broad html skill routes a plan request here.",
        "role": "Actionable rollout, roadmap, and implementation planning workflow in self-contained HTML."
    },
    {
        "source_slug": "html-prototype",
        "canonical_id": "html-prototype",
        "category": "design",
        "tags": ["prototype", "mockup", "html", "interactive", "ui-ux", "design", "effective-html"],
        "disable_model_invocation": False,
        "description": "Direct-invocation specialist for polished, responsive, self-contained HTML mockups and interactive prototypes grounded in the user's conversation, product context, and design language. Use when the user explicitly invokes html-prototype or the broad html skill routes a mockup or prototype request here.",
        "role": "Interactive prototyping and high-fidelity product mockup workflow in self-contained HTML."
    },
    {
        "source_slug": "html-wireframe",
        "canonical_id": "html-wireframe",
        "category": "design",
        "tags": ["wireframe", "html", "low-fidelity", "layout", "information-architecture", "design", "effective-html"],
        "disable_model_invocation": False,
        "description": "Direct-invocation specialist for low-fidelity, self-contained HTML wireframes that test information hierarchy, content, navigation, task flow, and responsive structure before visual design. Use when the user explicitly invokes html-wireframe or the broad html skill routes a wireframe request here.",
        "role": "Low-fidelity wireframing and information hierarchy validation in self-contained HTML."
    },
    {
        "source_slug": "one-pager",
        "canonical_id": "one-pager",
        "category": "design",
        "tags": ["one-pager", "html", "design", "summary", "communication", "visual-explanation", "effective-html"],
        "disable_model_invocation": True,
        "description": "Make a one-pager: one HTML page that shares an idea with teammates early, or recaps work for them, with big pictures and little words. Use when the user asks for a one-pager or executive visual summary in HTML.",
        "role": "Executive one-page visual brief and milestone recap workflow in self-contained HTML."
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
            if v in (">-", ">", "|", "|-"):
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
        description = item["description"]
        role = item["role"]
        disable_model = item["disable_model_invocation"]

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
        if not description:
            description = fm.get("description", "")

        # Format customized SKILL.md
        body = raw_skill_content
        if body.startswith("---"):
            parts = body.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].lstrip("\n")

        disable_line = "disable-model-invocation: true\n" if disable_model else ""
        vas_frontmatter = (
            f"---\n"
            f"name: {canonical_id}\n"
            f"description: {description}\n"
            f"{disable_line}"
            f"category: {category}\n"
            f"tags:\n"
            + "".join(f"  - {t}\n" for t in tags)
            + f"license: {LICENSE_NAME}\n"
            f"metadata:\n"
            f"  author: {AUTHOR}\n"
            f"  version: 1.0.0\n"
            f"---\n\n"
        )

        installation_notes = f"""

## VAS installation notes

- Canonical ID: `{canonical_id}`
- Source repository: [`plannotator/effective-html`](https://github.com/plannotator/effective-html) (revision `{UPSTREAM_REV}`, path `{source_path}`)
- Author: {AUTHOR} ([plannotator.ai](https://docs.plannotator.ai/))
- License: {LICENSE_NAME} (see bundled `LICENSE` and `NOTICE.md`)
- Role: {role}
- Prerequisites: Modern web browser or local HTML viewer; optional Plannotator integration.
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
            "risk": "safe",
            "source": f"https://github.com/plannotator/effective-html/tree/{UPSTREAM_REV}/{source_path}",
            "source_repo": "plannotator/effective-html",
            "source_revision": UPSTREAM_REV,
            "source_path": source_path,
            "author": AUTHOR,
            "license": LICENSE_NAME,
            "license_source": LICENSE_URL,
        })

        # 4. Copy subdirectories (agents/, references/)
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

    # Write data/effective-html-import.json
    import_manifest = {
        "source_repo": "plannotator/effective-html",
        "revision": UPSTREAM_REV,
        "skill_count": len(imported_skills),
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3876,
            "upstream_is_fork": False,
            "methods": [
                "canonical-id/name",
                "source-repo/path",
                "raw-sha256",
                "normalized-body",
                "renamed-body",
                "body-containment",
                "7-word-shingles"
            ],
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,876 catalog skills identified zero existing duplicates (max similarity 0.0004). All 8 skills are completely unique, focused visual HTML artifact creation workflows."
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, references/ and agents/ under Open Agent Skills format.",
            "Append reversible VAS installation, attribution, prerequisites, role, and safety notes to SKILL.md.",
            "Include upstream MIT LICENSE and add NOTICE.md clarifying standalone operation and optional Plannotator integration.",
            "Map upstream skills to existing design category to preserve exactly 119 catalog categories.",
            "Retain relative cross-references between sibling skills (e.g. ../design-artifact/SKILL.md) for direct standalone and composed resolution.",
            "No runtime/dependency or MCP service is executed during installation."
        ],
        "files": file_records,
        "skills": imported_skills,
    }

    (REPO_ROOT / "data/effective-html-import.json").write_text(
        json.dumps(import_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print("Wrote data/effective-html-import.json")

    # Update data/catalog.json
    catalog_path = REPO_ROOT / "data/catalog.json"
    catalog_data = json.loads(catalog_path.read_text(encoding="utf-8"))
    existing_catalog_ids = {s["id"] for s in catalog_data["skills"]}

    added_count = 0
    for s in imported_skills:
        if s["id"] not in existing_catalog_ids:
            catalog_data["skills"].append(s)
            added_count += 1
            existing_catalog_ids.add(s["id"])

    catalog_data["skills"].sort(key=lambda s: s["id"])
    catalog_path.write_text(
        json.dumps(catalog_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"Updated data/catalog.json: added {added_count} skills (total {len(catalog_data['skills'])})")

    # Update data/source-credits.json
    credits_path = REPO_ROOT / "data/source-credits.json"
    credits_data = json.loads(credits_path.read_text(encoding="utf-8"))
    credits_data["sections"]["effectivehtml"] = [
        f"- **[plannotator/effective-html](https://github.com/plannotator/effective-html/tree/{UPSTREAM_REV})**: Pragmatic visual HTML artifacts collection by Plannotator at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Provides focused agent workflows for self-contained, single-file HTML deliverables: wireframes, interactive prototypes, mockups, plans, diagrams, one-pagers, visual explanations, and creative design direction.",
        "- Preserves upstream Agent Skills specification SKILL.md with complete references (creative direction, charts & data, diagrams, documents & presentations, interfaces) and agent configurations.",
        "- Supports both standalone installation per skill and rich inter-skill composition (e.g., `design-artifact` with `html-prototype` or `html-diagram`).",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed, and no external accounts are connected."
    ]
    credits_path.write_text(
        json.dumps(credits_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print("Updated data/source-credits.json with effectivehtml section")


if __name__ == "__main__":
    main()
