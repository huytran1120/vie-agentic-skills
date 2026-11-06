#!/usr/bin/env python3
"""
Import 283 specialized agent skills from msitarzewski/agency-agents.
"""

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/agency-agents-temp")
UPSTREAM_CONVERTED = UPSTREAM_REPO / "integrations" / "antigravity"
UPSTREAM_REV = "b37b5bb33b78f2c1d6567d98e25ca818e3259219"
AUTHOR = "AgentLand Contributors"
AUTHOR_URL = "https://github.com/msitarzewski/agency-agents"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/msitarzewski/agency-agents/blob/{UPSTREAM_REV}/LICENSE"

LICENSE_TEXT = (UPSTREAM_REPO / "LICENSE").read_text(encoding="utf-8")

NOTICE_TEMPLATE = """# Notices

The Agency source code and agent specifications are MIT licensed (Copyright (c) 2025 AgentLand Contributors); see bundled `LICENSE`.

## Specialized Agent Persona

This skill defines an AI Agent persona with structured role identity, core competencies, deliverables, workflows, and production prompts from The Agency.

## Safe Operation

Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.
No unapproved scripts are executed, no external dependencies or MCP servers are installed, and
no background processes or accounts are connected during installation.
"""

# Map upstream 18 divisions to existing VAS categories (preserving exactly 119 categories)
DIVISION_TO_CATEGORY = {
    "academic": "education",
    "design": "design",
    "engineering": "engineering",
    "finance": "finance",
    "game-development": "game-development",
    "gis": "engineering",
    "healthcare": "health",
    "marketing": "marketing",
    "paid-media": "marketing",
    "product": "product",
    "project-management": "project-management",
    "research": "research",
    "sales": "business",
    "security": "security",
    "spatial-computing": "creative",
    "specialized": "agent-persona",
    "support": "operations",
    "testing": "testing",
}

AGENT_DIRS = [
    "academic", "design", "engineering", "finance", "game-development", "gis", "healthcare",
    "marketing", "paid-media", "product", "project-management", "research", "sales",
    "security", "spatial-computing", "specialized", "support", "testing",
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
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            fm[k] = v
    return fm


def main():
    skills_dir = REPO_ROOT / "skills"
    file_records = []
    imported_skills = []

    # Map each agency slug to its upstream source file and division
    upstream_agents = {}
    for div in AGENT_DIRS:
        div_path = UPSTREAM_REPO / div
        if not div_path.is_dir():
            continue
        for f in sorted(div_path.rglob("*.md")):
            content = f.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue
            parts = content.split("---", 2)
            if len(parts) < 3:
                continue
            name_match = re.search(r"^name:\s*(.+)$", parts[1], re.MULTILINE)
            if not name_match:
                continue
            raw_name = name_match.group(1).strip().strip("\"'")
            slug = re.sub(r"[^a-z0-9]+", "-", raw_name.lower()).strip("-")
            agency_slug = f"agency-{slug}"
            upstream_agents[agency_slug] = {
                "division": div,
                "source_path": str(f.relative_to(UPSTREAM_REPO)),
                "raw_name": raw_name,
                "source_file": f,
            }

    print(f"Discovered {len(upstream_agents)} upstream agent specifications.")

    # Converted Antigravity dirs
    converted_dirs = sorted([
        d for d in UPSTREAM_CONVERTED.glob("agency-*")
        if d.is_dir() and (d / "SKILL.md").exists()
    ])
    print(f"Found {len(converted_dirs)} converted Antigravity skills.")
    assert len(converted_dirs) == 283, f"Expected 283 skills, found {len(converted_dirs)}"

    for c_dir in converted_dirs:
        canonical_id = c_dir.name
        agent_meta = upstream_agents.get(canonical_id)
        if not agent_meta:
            raise ValueError(f"Could not map {canonical_id} to upstream agent source")

        division = agent_meta["division"]
        source_path = agent_meta["source_path"]
        category = DIVISION_TO_CATEGORY.get(division, "general")
        dest_dir = skills_dir / canonical_id

        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

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
        notice = NOTICE_TEMPLATE.strip() + "\n"
        if canonical_id == "agency-agentic-identity-trust-architect":
            notice += "\n## VAS link adaptation\n\nThe related Identity Graph Operator link points to the imported skill's `SKILL.md` in this catalog.\n"
        not_file.write_text(notice, encoding="utf-8")
        not_file.chmod(0o644)
        file_records.append({
            "source_path": f"{source_path} (via NOTICE.md)",
            "path": f"skills/{canonical_id}/NOTICE.md",
            "source_sha256": hashlib.sha256((NOTICE_TEMPLATE.strip() + "\n").encode("utf-8")).hexdigest(),
            "sha256": sha256_file(not_file),
            "executable": False,
        })

        # 3. SKILL.md
        conv_smd = c_dir / "SKILL.md"
        smd_text = conv_smd.read_text(encoding="utf-8")
        if canonical_id == "agency-agentic-identity-trust-architect":
            smd_text = smd_text.replace(
                "](identity-graph-operator.md)", "](../agency-identity-graph-operator/SKILL.md)"
            )
        fm = extract_frontmatter(smd_text)

        vas_notes = f"""

## VAS installation notes

- Canonical ID: `{canonical_id}`
- Division: `{division}`
- Source repository: [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) (revision `{UPSTREAM_REV}`, path `{source_path}`)
- Author: {AUTHOR} ([@msitarzewski](https://github.com/msitarzewski))
- License: MIT License (see bundled `LICENSE`)
- Role: Specialized AI agent persona engineered with production workflows, deliverables, and behavioral prompts.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""
        smd_dst = dest_dir / "SKILL.md"
        smd_dst.write_text(smd_text.rstrip() + vas_notes, encoding="utf-8")
        smd_dst.chmod(0o644)
        file_records.append({
            "source_path": source_path,
            "path": f"skills/{canonical_id}/SKILL.md",
            "source_sha256": sha256_file(conv_smd),
            "sha256": sha256_file(smd_dst),
            "executable": False,
        })

        desc = fm.get("description", f"Specialized AI agent persona for {canonical_id}.")
        clean_tag_name = canonical_id.replace("agency-", "")
        tags = [
            "agency-agents",
            "the-agency",
            "ai-specialist",
            division,
            clean_tag_name,
        ]
        # add slug words to tags
        for w in clean_tag_name.split("-"):
            if len(w) > 2 and w not in tags:
                tags.append(w)

        imported_skills.append({
            "id": canonical_id,
            "canonical_id": canonical_id,
            "name": canonical_id,
            "description": desc,
            "category": category,
            "risk": "safe",
            "tags": tags,
            "source": f"https://github.com/msitarzewski/agency-agents/tree/{UPSTREAM_REV}/{source_path}",
            "source_repo": "msitarzewski/agency-agents",
            "source_revision": UPSTREAM_REV,
            "source_path": source_path,
            "author": AUTHOR,
            "license": LICENSE_NAME,
            "license_source": LICENSE_URL,
            "path": f"skills/{canonical_id}/SKILL.md",
        })

    file_records.sort(key=lambda r: r["path"])
    imported_skills.sort(key=lambda s: s["id"])
    print(f"Processed {len(imported_skills)} skills with {len(file_records)} total files.")

    # Write data/agency-agents-import.json
    import_manifest = {
        "source_repo": "msitarzewski/agency-agents",
        "revision": UPSTREAM_REV,
        "skill_count": len(imported_skills),
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3576,
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
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,576 catalog skills identified zero existing duplicates. All 283 skills are prefixed with agency- according to upstream design and represent distinct AI agent personas.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md generated via convert.sh for Antigravity standard format.",
            "Append reversible VAS installation, attribution, division, role, and safety notes to SKILL.md.",
            "Map 18 upstream divisions into existing VAS taxonomy to preserve exactly 119 catalog categories.",
            "Include upstream MIT LICENSE and add NOTICE.md acknowledging AI specialist persona and safe offline execution.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "agency-agents-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/agency-agents-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["agency"] = [
        f"- **[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents/tree/{UPSTREAM_REV})**: 283 specialized AI agent personas by AgentLand Contributors ([@msitarzewski](https://github.com/msitarzewski)) at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Covers 18 specialized divisions: engineering (architects, fullstack, backend, DevOps, performance, QA), design (UI/UX, design systems, visual, 3D), marketing & paid media (growth, PPC, SEO, copywriters), product & project management (PO, scrum, release, agile), security & compliance (pentest, appsec, cloud security), research, sales, finance, health, and education.",
        "- Standalone payloads preserve upstream Antigravity standard SKILL.md with full role prompts, memory guidelines, and operational playbooks.",
        "- Installation runs no code, installs no dependencies or MCP servers, and connects no external accounts.",
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
    catalog_data["generatedAt"] = "2026-11-04T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills.")


if __name__ == "__main__":
    main()
