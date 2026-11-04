#!/usr/bin/env python3
"""
Import 13 social media research skills from ScrapeCreators/social-media-research-skills.
"""

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/social-media-research-skills-temp")
UPSTREAM_REV = "64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2"
AUTHOR = "ScrapeCreators"
AUTHOR_URL = "https://github.com/ScrapeCreators/social-media-research-skills"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/ScrapeCreators/social-media-research-skills/blob/{UPSTREAM_REV}/LICENSE"

LICENSE_TEXT = (UPSTREAM_REPO / "LICENSE").read_text(encoding="utf-8")

NOTICE_TEMPLATE = """# Notices

ScrapeCreators social media research skills and specifications are MIT licensed (Copyright (c) 2026 ScrapeCreators); see bundled `LICENSE`.

## Social Media Research & Intelligence

This skill provides standardized prompt engineering, research playbooks, and analytical workflows for extracting insights, hooks, transcripts, audience signals, and competitor intelligence from public social media platforms.

## Prerequisites & External Services

- Public social data analysis workflows can query public endpoints or the optional ScrapeCreators REST API (`SCRAPECREATORS_API_KEY`).
- No API keys are required for offline playbook inspection, prompt templating, or static reasoning.
- Users provide their own API key via environment variables if making live API calls.

## Safe Operation

Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.
No unapproved scripts are executed, no external dependencies or MCP servers are installed, and
no background processes or accounts are connected during installation.
"""

SKILL_DEFINITIONS = [
    {
        "source_slug": "ad-library-teardown",
        "canonical_id": "ad-library-teardown",
        "category": "marketing",
        "tags": ["social-media", "marketing", "ad-library", "facebook-ads", "meta-ads", "google-ads", "advertising", "scrapecreators"],
    },
    {
        "source_slug": "audience-research",
        "canonical_id": "scrapecreators-audience-research",
        "category": "marketing",
        "tags": ["social-media", "marketing", "audience-research", "demographics", "tiktok", "influencer", "scrapecreators"],
    },
    {
        "source_slug": "comment-mining",
        "canonical_id": "comment-mining",
        "category": "research",
        "tags": ["social-media", "research", "comment-mining", "voice-of-customer", "sentiment", "customer-feedback", "scrapecreators"],
    },
    {
        "source_slug": "competitor-social-research",
        "canonical_id": "competitor-social-research",
        "category": "research",
        "tags": ["social-media", "research", "competitor-analysis", "social-strategy", "content-gaps", "scrapecreators"],
    },
    {
        "source_slug": "content-repurposing",
        "canonical_id": "content-repurposing",
        "category": "content",
        "tags": ["social-media", "content", "content-repurposing", "transcripts", "linkedin", "x-threads", "short-form", "scrapecreators"],
    },
    {
        "source_slug": "creator-profile-teardown",
        "canonical_id": "creator-profile-teardown",
        "category": "marketing",
        "tags": ["social-media", "marketing", "creator-profile", "influencer-analysis", "content-pillars", "scrapecreators"],
    },
    {
        "source_slug": "influencer-prospecting",
        "canonical_id": "influencer-prospecting",
        "category": "marketing",
        "tags": ["social-media", "marketing", "influencer-prospecting", "partnerships", "ugc", "creator-outreach", "scrapecreators"],
    },
    {
        "source_slug": "outlier-post-finder",
        "canonical_id": "outlier-post-finder",
        "category": "marketing",
        "tags": ["social-media", "marketing", "outlier-posts", "viral-content", "hooks", "swipe-file", "scrapecreators"],
    },
    {
        "source_slug": "product-demand-research",
        "canonical_id": "product-demand-research",
        "category": "research",
        "tags": ["social-media", "research", "product-demand", "validation", "pain-points", "reddit", "scrapecreators"],
    },
    {
        "source_slug": "scrapecreators-api",
        "canonical_id": "scrapecreators-api",
        "category": "api-integration",
        "tags": ["social-media", "api-integration", "scrapecreators-api", "rest-api", "data-extraction", "scrapecreators"],
    },
    {
        "source_slug": "social-listening-brief",
        "canonical_id": "social-listening-brief",
        "category": "marketing",
        "tags": ["social-media", "marketing", "social-listening", "brand-monitoring", "sentiment", "executive-brief", "scrapecreators"],
    },
    {
        "source_slug": "transcript-intelligence",
        "canonical_id": "transcript-intelligence",
        "category": "media-processing",
        "tags": ["social-media", "media-processing", "transcript-intelligence", "video-transcripts", "youtube", "tiktok", "scrapecreators"],
    },
    {
        "source_slug": "trend-discovery",
        "canonical_id": "trend-discovery",
        "category": "research",
        "tags": ["social-media", "research", "trend-discovery", "trending-topics", "hashtags", "viral-trends", "scrapecreators"],
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
        upstream_smd = source_dir / "SKILL.md"
        smd_text = upstream_smd.read_text(encoding="utf-8")

        # Update name frontmatter if namespaced
        if canonical_id != source_slug:
            smd_text = re.sub(
                r"^name:\s*" + re.escape(source_slug) + r"\b",
                f"name: {canonical_id}",
                smd_text,
                flags=re.MULTILINE
            )

        fm = extract_frontmatter(smd_text)

        vas_notes = f"""

## VAS installation notes

- Canonical ID: `{canonical_id}`
- Source repository: [`ScrapeCreators/social-media-research-skills`](https://github.com/ScrapeCreators/social-media-research-skills) (revision `{UPSTREAM_REV}`, path `{source_path}`)
- Author: {AUTHOR} ([@ScrapeCreators](https://github.com/ScrapeCreators))
- License: MIT License (see bundled `LICENSE`)
- Role: Social media research and intelligence workflow for AI coding agents.
- Prerequisites: Requires `SCRAPECREATORS_API_KEY` for live API scraping operations; offline analysis and prompt templating function without credentials.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""
        smd_dst = dest_dir / "SKILL.md"
        smd_dst.write_text(smd_text.rstrip() + vas_notes, encoding="utf-8")
        smd_dst.chmod(0o644)
        file_records.append({
            "source_path": f"{source_path}/SKILL.md",
            "path": f"skills/{canonical_id}/SKILL.md",
            "source_sha256": sha256_file(upstream_smd),
            "sha256": sha256_file(smd_dst),
            "executable": False,
        })

        desc = fm.get("description", f"Social media intelligence and research skill for {canonical_id}.")

        imported_skills.append({
            "id": canonical_id,
            "canonical_id": canonical_id,
            "name": canonical_id,
            "description": desc,
            "category": category,
            "risk": "safe",
            "tags": tags,
            "source": f"https://github.com/ScrapeCreators/social-media-research-skills/tree/{UPSTREAM_REV}/{source_path}",
            "source_repo": "ScrapeCreators/social-media-research-skills",
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

    # Write data/scrapecreators-import.json
    import_manifest = {
        "source_repo": "ScrapeCreators/social-media-research-skills",
        "revision": UPSTREAM_REV,
        "skill_count": len(imported_skills),
        "skipped": [],
        "namespaces": {
            "audience-research": "scrapecreators-audience-research"
        },
        "duplicate_check": {
            "catalog_count_before": 3859,
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
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,859 catalog skills identified zero content duplicates. The upstream audience-research collided in name with an existing ad targeting skill (minhnv0807/ai-business-skills), so it was namespaced to scrapecreators-audience-research per Golden Rule 4. All other 12 skills have unique IDs and distinct content.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md under Open Agent Skills format.",
            "Append reversible VAS installation, attribution, prerequisites, role, and safety notes to SKILL.md.",
            "Namespace audience-research to scrapecreators-audience-research to avoid colliding with existing ad targeting skill.",
            "Map upstream skills into existing VAS taxonomy (marketing, research, content, api-integration, media-processing) to preserve exactly 119 catalog categories.",
            "Include upstream MIT LICENSE and add NOTICE.md acknowledging social intelligence workflows, optional API keys, and safe offline execution.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "scrapecreators-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/scrapecreators-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["scrapecreators"] = [
        f"- **[ScrapeCreators/social-media-research-skills](https://github.com/ScrapeCreators/social-media-research-skills/tree/{UPSTREAM_REV})**: 13 social media research and intelligence skills by ScrapeCreators ([@ScrapeCreators](https://github.com/ScrapeCreators)) at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Covers 13 specialized social intelligence workflows: ad library teardown (Meta, Google, LinkedIn), creator demographics & audience research, comment mining, competitor research, content repurposing, creator profile teardowns, influencer prospecting, outlier post finding, product demand validation, ScrapeCreators REST API integration, social listening briefs, video transcript intelligence, and trend discovery.",
        "- Standalone payloads preserve upstream Agent Skills specification SKILL.md with full prompts, parameter extraction, and structured research playbooks.",
        "- Optional live API features require user-provided SCRAPECREATORS_API_KEY; offline prompt generation and analysis run safely with zero external dependencies.",
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
    catalog_data["generatedAt"] = "2026-11-04T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills.")


if __name__ == "__main__":
    main()
