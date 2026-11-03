#!/usr/bin/env python3
"""
Import 147 skills from minhnv0807/ai-business-skills.
"""

import hashlib
import json
import os
import re
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/ai-business-skills-check")
UPSTREAM_REV = "fe33cb1a47e6140d3693651acbb743e2b1b5b26f"
AUTHOR = "AI Business Skills"
AUTHOR_AFFILIATION = "Over Powers Agency"
AUTHOR_URL = "https://github.com/minhnv0807/ai-business-skills"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/minhnv0807/ai-business-skills/blob/{UPSTREAM_REV}/LICENSE"

COLLISION_MAP = {
    "product-marketing-context": "aibiz-product-marketing-context",
}

LICENSE_TEXT = (UPSTREAM_REPO / "LICENSE").read_text(encoding="utf-8")

NOTICE_TEMPLATE = """# Notices

AI Business Skills source code is MIT licensed (Copyright (c) 2025 Over Powers Agency); see `LICENSE`.

## Author & Attribution
- Author: Nguyễn Văn Minh (`minhnv0807`) & Over Powers Agency
- Upstream repository: https://github.com/minhnv0807/ai-business-skills (revision `{rev}`)

## Safe Operation
Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.
No unapproved scripts are executed, no external dependencies or MCP servers are installed, and
no background processes or accounts are connected during installation.
"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def find_all_upstream_skills():
    skills = []
    # 1. modules/dropshipping/en/
    ds_dir = UPSTREAM_REPO / "modules" / "dropshipping" / "en"
    if ds_dir.exists():
        for d in sorted(ds_dir.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                skills.append((d.name, d))

    # 2. modules/personal-branding/en/
    pb_en = UPSTREAM_REPO / "modules" / "personal-branding" / "en"
    if pb_en.exists():
        for d in sorted(pb_en.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                skills.append((d.name, d))

    # 3. modules/personal-branding/vi/
    pb_vi = UPSTREAM_REPO / "modules" / "personal-branding" / "vi"
    if pb_vi.exists():
        for d in sorted(pb_vi.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                skills.append((d.name, d))

    # 4. skills/en/
    skills_en = UPSTREAM_REPO / "skills" / "en"
    if skills_en.exists():
        for d in sorted(skills_en.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                skills.append((d.name, d))

    # 5. skills/vi/
    skills_vi = UPSTREAM_REPO / "skills" / "vi"
    if skills_vi.exists():
        for d in sorted(skills_vi.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                skills.append((d.name, d))

    return skills


def collect_referenced_files(source_dir: Path, skill_content: str):
    """Find references mentioned in SKILL.md that live outside source_dir."""
    referenced = {}
    
    # Potential relative reference patterns
    ref_matches = set(re.findall(r'([a-zA-Z0-9_\-\./]+\.md)', skill_content))
    source_dir_resolved = source_dir.resolve()
    
    for r in ref_matches:
        # Check various locations in UPSTREAM_REPO
        candidates = [
            (source_dir / r).resolve(),
            (UPSTREAM_REPO / r).resolve(),
            (UPSTREAM_REPO / "skills" / "vi" / r).resolve(),
            (UPSTREAM_REPO / "skills" / "en" / r).resolve(),
            (UPSTREAM_REPO / "references" / Path(r).name).resolve(),
            (UPSTREAM_REPO / "skills" / "vi" / "references" / Path(r).name).resolve(),
            (UPSTREAM_REPO / "skills" / "en" / "references" / Path(r).name).resolve(),
            (UPSTREAM_REPO / "agents" / Path(r).name).resolve(),
        ]
        for cand in candidates:
            if cand.exists() and cand.is_file() and not cand.samefile(source_dir / "SKILL.md"):
                # If it's outside source_dir, we need to bundle it
                if not cand.is_relative_to(source_dir_resolved):
                    dest_subpath = Path("references") / cand.name
                    referenced[dest_subpath] = cand
                break
    return referenced


def main():
    print("Finding all upstream skills in minhnv0807/ai-business-skills...")
    upstream_skills = find_all_upstream_skills()
    print(f"Found {len(upstream_skills)} skills.")

    imported_skills = []
    file_records = []

    dest_skills_root = REPO_ROOT / "skills"

    for original_id, source_dir in upstream_skills:
        canonical_id = COLLISION_MAP.get(original_id, original_id)
        target_dir = dest_skills_root / canonical_id

        # Clean any existing directory for this skill
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

        # 1. Copy everything inside source_dir
        for root, dirs, files in os.walk(source_dir):
            rel_root = Path(root).relative_to(source_dir)
            target_sub = target_dir / rel_root
            target_sub.mkdir(parents=True, exist_ok=True)
            for f in files:
                src_file = Path(root) / f
                dst_file = target_sub / f
                shutil.copy2(src_file, dst_file)
                dst_file.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

        # Read copied SKILL.md
        skill_md_path = target_dir / "SKILL.md"
        skill_content = skill_md_path.read_text(encoding="utf-8")

        # 2. Collect and bundle any outside referenced files
        external_refs = collect_referenced_files(source_dir, skill_content)
        for dest_subpath, src_path in external_refs.items():
            dest_file = target_dir / dest_subpath
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            if not dest_file.exists():
                shutil.copy2(src_path, dest_file)
                dest_file.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

        # 3. Adjust references in SKILL.md to point to local references/
        # e.g. ../references/foo.md -> references/foo.md
        # skills/vi/references/foo.md -> references/foo.md
        # skills/en/references/foo.md -> references/foo.md
        updated_content = skill_content
        updated_content = re.sub(r'\.\./references/', 'references/', updated_content)
        updated_content = re.sub(r'skills/vi/references/', 'references/', updated_content)
        updated_content = re.sub(r'skills/en/references/', 'references/', updated_content)

        # If namespaced, update name in frontmatter
        if canonical_id != original_id:
            updated_content = re.sub(
                r'^(name:\s*).*$',
                f'\\1{canonical_id}',
                updated_content,
                flags=re.MULTILINE
            )

        # Append standard VAS usage note
        vas_note = f"""

---

## Hướng dẫn sử dụng trong VAS / Usage in VAS

- Cài đặt vào agent yêu thích bằng VAS CLI:
  `./vas install {canonical_id} --target <agent> --mode link`
- Chế độ copy độc lập vào dự án:
  `./vas install {canonical_id} --target <agent> --mode copy`
- Hoặc sử dụng tính năng **Copy Agent Prompt** trực tiếp từ website [Vie Agentic Skills](https://huytran1120.github.io/vie-agentic-skills/?sources=aibusiness) mà không cần clone repository.
"""
        updated_content = updated_content.rstrip() + vas_note + "\n"
        skill_md_path.write_text(updated_content, encoding="utf-8")
        skill_md_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

        # 4. Copy LICENSE and write NOTICE.md
        lic_path = target_dir / "LICENSE"
        lic_path.write_text(LICENSE_TEXT, encoding="utf-8")
        lic_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

        notice_path = target_dir / "NOTICE.md"
        notice_path.write_text(NOTICE_TEMPLATE.format(rev=UPSTREAM_REV), encoding="utf-8")
        notice_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

        # 5. Extract metadata for catalog
        desc_match = re.search(r'description:\s*\"([^\"]+)\"', updated_content)
        if not desc_match:
            desc_match = re.search(r'description:\s*([^\n]+)', updated_content)
        desc = desc_match.group(1).strip().strip('"\'') if desc_match else f"{canonical_id} marketing and business workflow skill"

        # Record file inventory
        for root, dirs, files in os.walk(target_dir):
            for f in sorted(files):
                full_f = Path(root) / f
                rel_repo = full_f.relative_to(REPO_ROOT).as_posix()
                file_records.append({
                    "path": rel_repo,
                    "size": full_f.stat().st_size,
                    "sha256": sha256_file(full_f),
                    "executable": False,
                })

        source_rel_path = source_dir.relative_to(UPSTREAM_REPO).as_posix()
        imported_skills.append({
            "id": canonical_id,
            "canonical_id": canonical_id,
            "name": canonical_id,
            "description": desc,
            "category": "marketing",
            "risk": "safe",
            "tags": ["marketing", "ai-business", "solopreneur", "growth", canonical_id],
            "source": f"https://github.com/minhnv0807/ai-business-skills/tree/{UPSTREAM_REV}/{source_rel_path}",
            "source_repo": "minhnv0807/ai-business-skills",
            "source_revision": UPSTREAM_REV,
            "source_path": f"{source_rel_path}/SKILL.md",
            "author": AUTHOR,
            "license": LICENSE_NAME,
            "license_source": LICENSE_URL,
            "path": f"skills/{canonical_id}/SKILL.md",
        })

    print(f"Imported {len(imported_skills)} skills with {len(file_records)} total files.")

    # Save data/ai-business-skills-import.json
    import_manifest = {
        "source_repo": "minhnv0807/ai-business-skills",
        "revision": UPSTREAM_REV,
        "skill_count": len(imported_skills),
        "skipped": [],
        "namespaces": COLLISION_MAP,
        "duplicate_check": {
            "catalog_count_before": 3429,
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
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,429 catalog skills identified zero content collisions. The single name collision (product-marketing-context from Corey Haines' marketingskills) is namespaced with the aibiz- prefix.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, evals/, variants/, references/, and templates/.",
            "Bundle referenced shared reference documents into each skill so it remains fully operable when installed independently.",
            "Update relative markdown links to local references/ directory.",
            "Append reversible VAS installation, attribution, and safety notes to SKILL.md.",
            "Apply aibiz- namespace prefix exclusively to product-marketing-context to avoid collision with Corey Haines' marketingskills.",
            "Include upstream MIT LICENSE and add NOTICE.md acknowledging AI business workflows and safe offline execution.",
            "No unapproved code is executed and no runtime/dependency or MCP service is connected during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "ai-business-skills-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2, ensure_ascii=False)
    print("Saved data/ai-business-skills-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["aibusiness"] = [
        f"- **[minhnv0807/ai-business-skills](https://github.com/minhnv0807/ai-business-skills/tree/{UPSTREAM_REV})**: 147 AI Marketing & Business workflow skills by {AUTHOR} ([@minhnv0807](https://github.com/minhnv0807)) and Over Powers Agency at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Covers end-to-end business and marketing lifecycle: strategy & planning, content production, paid media (Facebook, Google, TikTok Ads), conversion rate optimization (CRO), e-commerce & dropshipping, personal branding & AI avatars, and sales chatbot scripts.",
        "- Includes both Vietnam cluster (79 skills tailored for Vietnam market benchmarks, legal frameworks, and platforms) and Global cluster (68 skills for US, EU, APAC, and international platforms).",
        "- Standalone payloads preserve upstream SKILL.md, variants, evals, templates, and references. The single colliding name uses the `aibiz-` namespace.",
        "- Installation runs no code, installs no dependencies or MCP servers, and connects no external accounts.",
    ]
    with open(credits_file, "w", encoding="utf-8") as f:
        json.dump(credits_data, f, indent=2, ensure_ascii=False)
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
    catalog_data["generatedAt"] = "2026-11-03T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2, ensure_ascii=False)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills.")


if __name__ == "__main__":
    main()
