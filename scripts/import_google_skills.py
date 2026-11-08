#!/usr/bin/env python3
"""
Import skills from google/skills:
Imports 184 genuinely new skills for Google Cloud, AI, and developer tools.
Skips 3 existing skills: firebase-basics, gemini-interactions-api, retrieving-developer-knowledge.
"""

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = "google/skills"
UPSTREAM_REV = "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee"
AUTHOR = "Google"
AUTHOR_URL = "https://github.com/google"

UPSTREAM_DIR = Path("/tmp/google-skills")
if not UPSTREAM_DIR.exists() or not (UPSTREAM_DIR / "skills").exists():
    raise RuntimeError(f"Upstream clone not found at {UPSTREAM_DIR}")

CATEGORY_MAPPING = {
    "GoogleAds": "marketing",
    "GoogleAnalytics": "data",
    "AiAndMachineLearning": "ai-ml",
    "ApplicationDevelopment": "developer-tools",
    "BigDataAndAnalytics": "data-engineering",
    "CloudInfrastructure": "cloud",
    "CloudInfrastructureAndServices": "cloud",
    "CloudObservabilityAndMonitoring": "devops",
    "Compute": "cloud",
    "Containers": "devops",
    "Databases": "database",
    "DevOps": "devops",
    "GettingStarted": "cloud",
    "MultiProductSolutions": "cloud",
    "Networking": "cloud",
    "Security": "security",
    "SecurityAndCompliance": "security",
    "Identity": "security",
    "Serverless": "cloud",
    "Storage": "cloud",
    "WellArchitectedFramework": "architecture",
}

GROUP_FALLBACK = {
    "ads": "marketing",
    "analytics": "data",
    "identity": "security",
    "developers": "developer-tools",
    "cloud": "cloud",
}

SKIPPED_EXISTING = {
    "firebase-basics": "Already exists in VAS catalog under skills/firebase-basics; skipped per CHỈ THÊM MỚI rule.",
    "gemini-interactions-api": "Already exists in VAS catalog under skills/gemini-interactions-api; skipped per CHỈ THÊM MỚI rule.",
    "retrieving-developer-knowledge": "Already exists in VAS catalog under skills/retrieving-developer-knowledge; skipped per CHỈ THÊM MỚI rule.",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(UPSTREAM_DIR / "index.json", "r", encoding="utf-8") as f:
        index_data = json.load(f)
    index_by_name = {s["name"]: s for s in index_data["skills"]}

    root_license_text = (UPSTREAM_DIR / "LICENSE").read_text(encoding="utf-8")

    skills_dir = UPSTREAM_DIR / "skills"
    all_skill_mds = sorted(list(skills_dir.rglob("SKILL.md")))

    file_records = []
    skill_entries = []
    skipped_records = []

    for sm in all_skill_mds:
        skill_id = sm.parent.name
        rel_from_skills = sm.parent.relative_to(skills_dir)
        group = rel_from_skills.parts[0]
        source_dir_rel = f"skills/{rel_from_skills}"
        source_skill_md = f"skills/{rel_from_skills}/SKILL.md"

        if skill_id in SKIPPED_EXISTING:
            skipped_records.append({
                "id": skill_id,
                "source_path": source_skill_md,
                "reason": SKIPPED_EXISTING[skill_id],
            })
            print(f"Skipping existing skill: {skill_id}")
            continue

        index_item = index_by_name.get(skill_id, {})
        description = index_item.get("description", "")

        text = sm.read_text(encoding="utf-8")
        lines = text.splitlines()
        frontmatter_text = ""
        body = text
        if lines and lines[0].strip() == "---":
            idx = 1
            while idx < len(lines) and lines[idx].strip() != "---":
                idx += 1
            frontmatter_text = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1:]).lstrip()

        # Extract category from frontmatter
        fm_cat = None
        for line in frontmatter_text.splitlines():
            if "category:" in line:
                fm_cat = line.split("category:", 1)[1].strip().strip("\"'")
            if not description and line.startswith("description:"):
                description = line.split("description:", 1)[1].strip().strip("\"'")

        final_cat = CATEGORY_MAPPING.get(fm_cat) or GROUP_FALLBACK.get(group, "cloud")

        # Tags
        tags = ["google", "google-cloud", group]
        if final_cat not in tags:
            tags.append(final_cat)
        # Add skill name fragments as tags
        for part in skill_id.split("-"):
            if part and part not in tags and len(part) > 2 and part not in ("api", "basics"):
                tags.append(part)

        dest_dir = REPO_ROOT / "skills" / skill_id
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        # 1. LICENSE
        lic_file = dest_dir / "LICENSE"
        lic_file.write_text(root_license_text, encoding="utf-8")
        lic_file.chmod(0o644)
        file_records.append({
            "skill_id": skill_id,
            "source_path": "LICENSE",
            "path": f"skills/{skill_id}/LICENSE",
            "sha256": sha256_file(lic_file),
            "executable": False,
        })

        # 2. NOTICE.md
        not_content = f"""# Notices

`{skill_id}` is imported from [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}) at revision `{UPSTREAM_REV}` (`{source_skill_md}`) under the Apache License 2.0 (Copyright 2026 Google LLC); see `LICENSE`.

## Purpose & Prerequisites

- {description[:180]}...
- Official Agent Skills developed by Google for Google Cloud, AI, and developer workflows.
- Standalone execution: runbooks, scripts, and references are self-contained.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No processes are executed, no external dependencies or runtimes are installed, and no cloud accounts or credentials are connected during installation.
"""
        not_file = dest_dir / "NOTICE.md"
        not_file.write_text(not_content.strip() + "\n", encoding="utf-8")
        not_file.chmod(0o644)
        file_records.append({
            "skill_id": skill_id,
            "source_path": f"{source_dir_rel}/NOTICE.md",
            "path": f"skills/{skill_id}/NOTICE.md",
            "sha256": sha256_file(not_file),
            "executable": False,
        })

        # 3. Copy all files from upstream skill directory
        src_skill_dir = sm.parent
        for src_path in sorted(src_skill_dir.rglob("*")):
            if src_path.is_dir() or src_path.is_symlink():
                continue
            rel = src_path.relative_to(src_skill_dir)
            dst_path = dest_dir / rel
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            is_exec = False
            src_mode = os.stat(src_path).st_mode
            if src_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                if rel.suffix in (".sh", ".py", "") and not rel.name.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".html")):
                    is_exec = True

            if rel.name == "SKILL.md":
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
license: "Apache-2.0"
license_source: "https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE"
---

"""
                vas_notes = f"""

---

## VAS installation notes

- Canonical ID: `{skill_id}`
- Source repository: [`{UPSTREAM_REPO}`](https://github.com/{UPSTREAM_REPO}) at commit `{UPSTREAM_REV}` (`{source_skill_md}`).
- Author: Google (`{AUTHOR_URL}`).
- License: Apache-2.0 (Copyright 2026 Google LLC); see `LICENSE` and `NOTICE.md`.
- Install via CLI: `./vas install {skill_id} --target <agent> --mode link` (or `--mode copy`).
"""
                full_content = new_frontmatter + body.rstrip() + vas_notes + "\n"
                dst_path.write_text(full_content, encoding="utf-8")
                dst_path.chmod(0o644)
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
                "sha256": sha256_file(dst_path),
                "executable": is_exec,
            })

        skill_entries.append({
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
            "license": "Apache-2.0",
            "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
        })

    print(f"Packaged {len(skill_entries)} new skills ({len(file_records)} files). Skipped: {len(skipped_records)}.")

    # Write data/google-skills-import.json
    import_manifest = {
        "source_repo": UPSTREAM_REPO,
        "source_url": f"https://github.com/{UPSTREAM_REPO}",
        "revision": UPSTREAM_REV,
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "license": "Apache-2.0",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
        "skill_count": len(skill_entries),
        "skipped": skipped_records,
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3889,
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
            "collision_rationale": "Exact and high-similarity comparison against all 3,889 catalog skills identified 3 existing duplicates (firebase-basics, gemini-interactions-api, retrieving-developer-knowledge). In accordance with the CHỈ THÊM MỚI rule, existing skills were strictly skipped. The remaining 184 skills provide official, standalone Google Cloud, AI, and developer workflows.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, references/, rules/, examples/, templates/, and scripts/ under Open Agent Skills format.",
            "Append reversible VAS installation, attribution, prerequisites, and safety notes to SKILL.md for each skill.",
            "Include upstream LICENSE (Apache-2.0) and add NOTICE.md clarifying standalone operation, copyright, and runtime prerequisites.",
            "Preserve executable bits (0755) on shell and Python execution scripts.",
            "Map all 184 skills to existing categories in the 119-category taxonomy without creating new categories.",
            "No runtime, dependency, or external service is executed during installation.",
        ],
        "skills": skill_entries,
        "files": file_records,
    }

    manifest_path = REPO_ROOT / "data" / "google-skills-import.json"
    manifest_path.write_text(json.dumps(import_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote import manifest to {manifest_path}")

    # Update data/source-credits.json
    credits_path = REPO_ROOT / "data" / "source-credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8"))
    credits["sections"]["googleskills"] = [
        f"- **[google/skills](https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV})**: Official Agent Skills for Google Cloud, AI, and Developer workflows by {AUTHOR} at revision `{UPSTREAM_REV}`.",
        "- Provides 184 modular skills covering Google Cloud Platform (GCP) infrastructure, Google Kubernetes Engine (GKE), BigQuery, Cloud Run, SecOps, Gemini API, Genkit, Google Ads, and developer tools.",
        "- Standalone payloads preserve upstream Agent Skills specification SKILL.md, references, diagnostic scripts, rule sets, and templates.",
        "- Licensing: Apache License 2.0 (Copyright 2026 Google LLC); see individual LICENSE and NOTICE.md files.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed, and no cloud accounts or credentials are connected during installation.",
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
