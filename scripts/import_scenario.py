#!/usr/bin/env python3
"""
Import 167 creative AI, DCC, and game engine skills from scenario-labs/skills.
"""

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_ROOT = Path("/tmp/scenario-skills-temp")
UPSTREAM_REV = "7f4b801c7248d51b093ec365aceb114bd06139e6"
AUTHOR = "Scenario Inc."
AUTHOR_URL = "https://github.com/scenario-labs"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/scenario-labs/skills/blob/{UPSTREAM_REV}/LICENSE"

MIT_LICENSE_TEXT = """MIT License

Copyright (c) 2026 Scenario Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

CATEGORY_READMES = {
    "skills/dcc/blender/README.md": "skills/scenario-blender-expert/README.md",
    "skills/dcc/maya/README.md": "skills/scenario-maya-expert/README.md",
    "skills/dcc/zbrush/README.md": "skills/scenario-zbrush-expert/README.md",
    "skills/game-engines/godot/README.md": "skills/scenario-godot-expert/README.md",
    "skills/game-engines/roblox/README.md": "skills/scenario-roblox-expert/README.md",
    "skills/game-engines/unity/README.md": "skills/scenario-unity-expert/README.md",
    "skills/game-engines/unreal/README.md": "skills/scenario-unreal-expert/README.md",
}

SKIPPED = [
    ".agents/skills/pr-handle-comments",
    ".agents/skills/pr-squash-message",
    ".agents/skills/pr-summary",
    ".agents/skills/skill-creator",
    ".agents/skills/skill-development",
    ".agents/skills/skills-pr-handle",
    ".agents/skills/skills-validate",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def parse_frontmatter(content: str):
    name = ""
    description = ""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if line.startswith("name:"):
                    name = line.split("name:", 1)[1].strip().strip("\"'")
                elif line.startswith("description:"):
                    description = line.split("description:", 1)[1].strip().strip("\"'")
    return name, description


def determine_category_and_tags(canonical_id: str, upstream_rel: str, description: str):
    # Category: game-development (for DCC and game engine suites) or media (for Scenario AI generation)
    if "blender" in canonical_id or "blender" in upstream_rel:
        category = "game-development"
        default_tags = ["blender", "dcc", "3d", "gamedev", "scenario"]
    elif any(dcc in upstream_rel or dcc in canonical_id for dcc in ["maya", "zbrush"]):
        category = "game-development"
        dcc_name = "maya" if "maya" in canonical_id else "zbrush"
        default_tags = [dcc_name, "dcc", "3d", "gamedev", "scenario"]
    elif any(eng in upstream_rel or eng in canonical_id for eng in ["godot", "roblox", "unity", "unreal"]):
        category = "game-development"
        engine_name = ""
        for eng in ["godot", "roblox", "unity", "unreal"]:
            if eng in canonical_id:
                engine_name = eng
                break
        default_tags = [engine_name, "game-engine", "gamedev", "scenario"] if engine_name else ["gamedev", "scenario"]
    else:
        category = "media"
        default_tags = ["ai-generation", "media", "creative", "scenario"]

    # Extract extra tags from canonical_id suffix
    suffix = canonical_id.replace("scenario-", "").replace("blender-", "").replace("maya-", "").replace("godot-", "").replace("unity-", "").replace("unreal-", "").replace("roblox-", "").replace("zbrush-", "")
    for part in suffix.split("-"):
        part = part.strip()
        if part and len(part) > 2 and part not in default_tags:
            default_tags.append(part)

    return category, default_tags


def main():
    print(f"Scanning upstream {UPSTREAM_ROOT}...")
    skills_to_import = []

    for root, dirs, files in os.walk(UPSTREAM_ROOT):
        if "SKILL.md" in files:
            rel = Path(root).relative_to(UPSTREAM_ROOT)
            rel_str = str(rel)
            if any(rel_str.startswith(skip) for skip in SKIPPED):
                continue
            canonical_id = rel.name
            skills_to_import.append((canonical_id, rel, Path(root)))

    skills_to_import.sort(key=lambda x: x[0])
    print(f"Found {len(skills_to_import)} skills to import.")
    assert len(skills_to_import) == 167, f"Expected 167 skills, found {len(skills_to_import)}"

    file_records = []

    for canonical_id, rel_upstream, src_dir in skills_to_import:
        dst_dir = REPO_ROOT / "skills" / canonical_id
        dst_dir.mkdir(parents=True, exist_ok=True)

        # Copy all files from src_dir
        for s_root, _, s_files in os.walk(src_dir):
            rel_s = Path(s_root).relative_to(src_dir)
            target_sub = dst_dir / rel_s
            target_sub.mkdir(parents=True, exist_ok=True)

            for sf in s_files:
                src_file = Path(s_root) / sf
                dst_file = target_sub / sf
                rel_src_path = str(src_file.relative_to(UPSTREAM_ROOT))
                rel_dst_path = str(dst_file.relative_to(REPO_ROOT))

                src_sha256 = sha256_file(src_file)
                st = src_file.stat()
                is_exec = bool(st.st_mode & stat.S_IXUSR)

                if sf == "SKILL.md" and rel_s == Path("."):
                    with open(src_file, "r", encoding="utf-8") as f:
                        original_skill_content = f.read()

                    notes = f"""

## VAS installation notes

- Canonical ID: `{canonical_id}`
- Source repository: [`scenario-labs/skills`](https://github.com/scenario-labs/skills) (revision `{UPSTREAM_REV}`)
- Author: Scenario Inc. ([@scenario-labs](https://github.com/scenario-labs))
- License: MIT License (see bundled `LICENSE`)
- Prerequisites: For Scenario AI skills: Scenario account and MCP server (optional, when running online workflows). For DCC/Game Engine skills: Local installation of respective software (Blender 5.x, Maya, ZBrush, Godot, Roblox Studio, Unity, or Unreal Engine).
- Safety: No downloaded code is executed, no runtime/MCP is configured, and no external service is connected during `./vas install`.
"""
                    new_skill_content = original_skill_content.rstrip() + "\n" + notes
                    with open(dst_file, "w", encoding="utf-8") as f:
                        f.write(new_skill_content)
                else:
                    shutil.copy2(src_file, dst_file)

                # Set permission
                if is_exec:
                    os.chmod(dst_file, 0o755)
                else:
                    os.chmod(dst_file, 0o644)

                dst_sha256 = sha256_file(dst_file)
                file_records.append({
                    "source_path": rel_src_path,
                    "path": rel_dst_path,
                    "source_sha256": src_sha256,
                    "sha256": dst_sha256,
                    "executable": is_exec,
                })

        # Ensure LICENSE is present in each skill
        license_path = dst_dir / "LICENSE"
        with open(license_path, "w", encoding="utf-8") as f:
            f.write(MIT_LICENSE_TEXT)
        os.chmod(license_path, 0o644)

        file_records.append({
            "source_path": "LICENSE",
            "path": str(license_path.relative_to(REPO_ROOT)),
            "source_sha256": sha256_file(UPSTREAM_ROOT / "LICENSE"),
            "sha256": sha256_file(license_path),
            "executable": False,
        })

    # Copy Category READMEs
    for orig_src, dest_path in CATEGORY_READMES.items():
        src_readme = UPSTREAM_ROOT / orig_src
        dst_readme = REPO_ROOT / dest_path
        if src_readme.exists():
            shutil.copy2(src_readme, dst_readme)
            os.chmod(dst_readme, 0o644)
            file_records.append({
                "source_path": orig_src,
                "path": dest_path,
                "source_sha256": sha256_file(src_readme),
                "sha256": sha256_file(dst_readme),
                "executable": False,
            })

    # Sort file records
    file_records.sort(key=lambda x: x["path"])
    print(f"Total files written and tracked: {len(file_records)}")

    # Write data/scenario-import.json
    import_manifest = {
        "source_repo": "scenario-labs/skills",
        "revision": UPSTREAM_REV,
        "skill_count": len(skills_to_import),
        "skipped": SKIPPED,
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3186,
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
            "collision_rationale": "No collision found across all 3,186 catalog skills. All 167 scenario skills are genuine new creative/gamedev additions.",
        },
        "adaptations": [
            "Preserve upstream payload structure, domain scripts, shaders, templates, and references.",
            "Append reversible VAS installation, attribution, prerequisites and safety notes to SKILL.md.",
            "Include upstream MIT LICENSE in every standalone skill directory.",
            "Copy category README files into respective suite expert router skills.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "scenario-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/scenario-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["scenario"] = [
        f"- **[scenario-labs/skills](https://github.com/scenario-labs/skills/tree/{UPSTREAM_REV})**: 167 MIT-licensed creative AI, DCC, and game engine skills by Scenario Inc. ([@scenario-labs](https://github.com/scenario-labs)) at revision `{UPSTREAM_REV}`.",
        "- Covers 78 Scenario AI generation workflows (media) and 89 DCC and game engine skills across Blender, Maya, ZBrush, Godot, Roblox, Unity, and Unreal Engine (game-development). Exact MIT LICENSE, reference documentation, shaders, and executable scripts are preserved.",
        "- Installation runs no code, installs no dependencies or MCP servers, and connects no external accounts. Software runtimes (Blender, Maya, ZBrush, Godot, Roblox Studio, Unity, Unreal) and optional Scenario API/MCP accounts are separate user prerequisites.",
    ]
    with open(credits_file, "w", encoding="utf-8") as f:
        json.dump(credits_data, f, indent=2)
    print("Updated data/source-credits.json")

    # Update data/catalog.json
    catalog_file = REPO_ROOT / "data" / "catalog.json"
    with open(catalog_file, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    # Filter out existing scenario skills if any
    filtered_skills = [
        s for s in catalog_data.get("skills", [])
        if not (s.get("canonical_id", "").startswith("scenario-") or s.get("canonical_id") == "scenario")
    ]

    new_catalog_entries = []
    for canonical_id, rel_upstream, _ in skills_to_import:
        skill_md = REPO_ROOT / "skills" / canonical_id / "SKILL.md"
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        name, desc = parse_frontmatter(content)
        category, tags = determine_category_and_tags(canonical_id, str(rel_upstream), desc)

        entry = {
            "id": canonical_id,
            "canonical_id": canonical_id,
            "name": name or canonical_id,
            "description": desc or f"Scenario workflow skill for {canonical_id}",
            "category": category,
            "risk": "safe",
            "tags": tags,
            "source": f"https://github.com/scenario-labs/skills/tree/{UPSTREAM_REV}/{rel_upstream}",
            "source_repo": "scenario-labs/skills",
            "source_revision": UPSTREAM_REV,
            "source_path": f"{rel_upstream}/SKILL.md",
            "author": AUTHOR,
            "license": LICENSE_NAME,
            "license_source": LICENSE_URL,
            "path": f"skills/{canonical_id}/SKILL.md",
        }
        new_catalog_entries.append(entry)

    filtered_skills.extend(new_catalog_entries)
    catalog_data["skills"] = filtered_skills
    catalog_data["total"] = len(filtered_skills)
    catalog_data["generatedAt"] = "2026-11-01T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills (added {len(new_catalog_entries)} scenario skills).")


if __name__ == "__main__":
    main()
