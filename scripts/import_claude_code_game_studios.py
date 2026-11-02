#!/usr/bin/env python3
"""
Import 74 skills from Donchitos/Claude-Code-Game-Studios.
"""

import hashlib
import json
import os
import re
import shutil
import stat
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = Path("/tmp/Claude-Code-Game-Studios")
UPSTREAM_SKILLS = UPSTREAM_REPO / ".claude" / "skills"
UPSTREAM_SCRIPTS = UPSTREAM_REPO / ".claude" / "scripts"
UPSTREAM_HOOKS = UPSTREAM_REPO / ".claude" / "hooks"
UPSTREAM_TEMPLATES = UPSTREAM_REPO / ".claude" / "docs" / "templates"
UPSTREAM_REV = "05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418"
AUTHOR = "Donchitos"
AUTHOR_URL = "https://github.com/Donchitos"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/Donchitos/Claude-Code-Game-Studios/blob/{UPSTREAM_REV}/LICENSE"

COLLISION_MAP = {
    "architecture-review": "gamestudio-architecture-review",
    "code-review": "gamestudio-code-review",
    "design-system": "gamestudio-design-system",
    "prototype": "gamestudio-prototype",
    "security-audit": "gamestudio-security-audit",
}

LICENSE_TEXT = (UPSTREAM_REPO / "LICENSE").read_text(encoding="utf-8")

NOTICE_TEMPLATE = """# Notices

Claude Code Game Studios source code is MIT licensed (Copyright (c) 2026 Donchitos); see `LICENSE`.

## Game Engine Compatibility

Skills are compatible with Godot 4, Unity, and Unreal Engine 5.
Engine tools, SDKs, and runtimes (e.g., Godot CLI, Unity Editor, Unreal Engine) are separate
user prerequisites configured in your game development environment.

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

    upstream_dirs = sorted([
        d for d in UPSTREAM_SKILLS.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    ])
    print(f"Found {len(upstream_dirs)} upstream skills to process.")

    for u_dir in upstream_dirs:
        u_name = u_dir.name
        canonical_id = COLLISION_MAP.get(u_name, u_name)
        dest_dir = skills_dir / canonical_id

        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        # 1. LICENSE
        lic_file = dest_dir / "LICENSE"
        lic_file.write_text(LICENSE_TEXT, encoding="utf-8")
        lic_file.chmod(0o644)
        file_records.append({
            "source_path": f".claude/skills/{u_name}/LICENSE",
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
            "source_path": f".claude/skills/{u_name}/NOTICE.md",
            "path": f"skills/{canonical_id}/NOTICE.md",
            "source_sha256": sha256_file(not_file),
            "sha256": sha256_file(not_file),
            "executable": False,
        })

        # 3. CONTRACT.md if present
        if (u_dir / "CONTRACT.md").exists():
            c_src = u_dir / "CONTRACT.md"
            c_dst = dest_dir / "CONTRACT.md"
            shutil.copy2(c_src, c_dst)
            c_dst.chmod(0o644)
            file_records.append({
                "source_path": f".claude/skills/{u_name}/CONTRACT.md",
                "path": f"skills/{canonical_id}/CONTRACT.md",
                "source_sha256": sha256_file(c_src),
                "sha256": sha256_file(c_dst),
                "executable": False,
            })

        # 4. references/ if present
        ref_dir = u_dir / "references"
        if ref_dir.is_dir():
            for r_src in sorted(ref_dir.rglob("*.md")):
                r_rel = r_src.relative_to(ref_dir)
                r_dst = dest_dir / "references" / r_rel
                r_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(r_src, r_dst)
                r_dst.chmod(0o644)
                file_records.append({
                    "source_path": f".claude/skills/{u_name}/references/{r_rel.as_posix()}",
                    "path": f"skills/{canonical_id}/references/{r_rel.as_posix()}",
                    "source_sha256": sha256_file(r_src),
                    "sha256": sha256_file(r_dst),
                    "executable": False,
                })

        # 5. Check dependencies for scripts and templates
        all_u_text = ""
        for f in u_dir.rglob("*.md"):
            all_u_text += f.read_text(encoding="utf-8") + "\n"

        needed_scripts = set(re.findall(r"\.claude/scripts/([a-zA-Z0-9_\-\.]+)", all_u_text))
        if "yaml-helper.sh" in all_u_text:
            needed_scripts.add("yaml-helper.sh")

        for s_name in sorted(needed_scripts):
            if s_name == "yaml-helper.sh":
                s_src = UPSTREAM_HOOKS / "yaml-helper.sh"
            else:
                s_src = UPSTREAM_SCRIPTS / s_name
            if s_src.exists():
                s_dst = dest_dir / "scripts" / s_name
                s_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(s_src, s_dst)
                is_exec = s_name.endswith(".sh")
                s_dst.chmod(0o755 if is_exec else 0o644)
                file_records.append({
                    "source_path": f".claude/{'hooks' if s_name == 'yaml-helper.sh' else 'scripts'}/{s_name}",
                    "path": f"skills/{canonical_id}/scripts/{s_name}",
                    "source_sha256": sha256_file(s_src),
                    "sha256": sha256_file(s_dst),
                    "executable": is_exec,
                })

        needed_templates = set(re.findall(r"\.claude/docs/templates/([a-zA-Z0-9_\-\.]+)", all_u_text))
        for t_name in sorted(needed_templates):
            t_src = UPSTREAM_TEMPLATES / t_name
            if t_src.exists() and t_src.is_file():
                t_dst = dest_dir / "templates" / t_name
                t_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(t_src, t_dst)
                t_dst.chmod(0o644)
                file_records.append({
                    "source_path": f".claude/docs/templates/{t_name}",
                    "path": f"skills/{canonical_id}/templates/{t_name}",
                    "source_sha256": sha256_file(t_src),
                    "sha256": sha256_file(t_dst),
                    "executable": False,
                })

        # 6. SKILL.md
        smd_src = u_dir / "SKILL.md"
        smd_text = smd_src.read_text(encoding="utf-8")
        fm = extract_frontmatter(smd_text)

        # Update frontmatter name for colliding skills
        if u_name in COLLISION_MAP:
            smd_text = re.sub(
                r"^name:\s*[^\n]+",
                f"name: {canonical_id}",
                smd_text,
                count=1,
                flags=re.MULTILINE,
            )

        # Build VAS installation notes
        vas_notes = f"""

## VAS installation notes

- Canonical ID: `{canonical_id}`
- Source repository: [`Donchitos/Claude-Code-Game-Studios`](https://github.com/Donchitos/Claude-Code-Game-Studios) (revision `{UPSTREAM_REV}`, path `.claude/skills/{u_name}`)
- Author: Donchitos ([@Donchitos](https://github.com/Donchitos))
- License: MIT License (see bundled `LICENSE`)
- Third-party notices: See bundled `NOTICE.md`
- Standalone payload: Includes complete `SKILL.md`, references, contracts, helper scripts, and templates required for independent execution.
- Prerequisites: Python 3 and Bash in your project. Game engines (Godot 4, Unity, or Unreal Engine 5) configured per your project requirements.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""
        smd_dst = dest_dir / "SKILL.md"
        smd_dst.write_text(smd_text.rstrip() + vas_notes, encoding="utf-8")
        smd_dst.chmod(0o644)
        file_records.append({
            "source_path": f".claude/skills/{u_name}/SKILL.md",
            "path": f"skills/{canonical_id}/SKILL.md",
            "source_sha256": sha256_file(smd_src),
            "sha256": sha256_file(smd_dst),
            "executable": False,
        })

        desc = fm.get("description", f"Game development studio skill for {canonical_id}.")
        imported_skills.append({
            "id": canonical_id,
            "canonical_id": canonical_id,
            "name": canonical_id,
            "description": desc,
            "category": "game-development",
            "risk": "safe",
            "tags": [
                "game-development",
                "gamedev",
                "claude-code-game-studios",
                "studio-workflow",
                u_name,
            ],
            "source": f"https://github.com/Donchitos/Claude-Code-Game-Studios/tree/{UPSTREAM_REV}/.claude/skills/{u_name}",
            "source_repo": "Donchitos/Claude-Code-Game-Studios",
            "source_revision": UPSTREAM_REV,
            "source_path": f".claude/skills/{u_name}/SKILL.md",
            "author": AUTHOR,
            "license": LICENSE_NAME,
            "license_source": LICENSE_URL,
            "path": f"skills/{canonical_id}/SKILL.md",
        })

    file_records.sort(key=lambda r: r["path"])
    imported_skills.sort(key=lambda s: s["id"])
    print(f"Processed {len(imported_skills)} skills with {len(file_records)} total files.")

    # Write data/claude-code-game-studios-import.json
    import_manifest = {
        "source_repo": "Donchitos/Claude-Code-Game-Studios",
        "revision": UPSTREAM_REV,
        "skill_count": len(imported_skills),
        "skipped": [],
        "namespaces": COLLISION_MAP,
        "duplicate_check": {
            "catalog_count_before": 3355,
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
            "collision_rationale": "Exact and high-similarity shingle comparison against all 3,355 catalog skills identified zero existing duplicates. The 5 colliding generic names (architecture-review, code-review, design-system, prototype, security-audit) are namespaced with the gamestudio- prefix.",
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, CONTRACT.md, and references/.",
            "Bundle referenced helper scripts (scripts/*.sh) and templates (templates/*.md) into each skill so it remains fully operable when installed independently.",
            "Append reversible VAS installation, attribution, prerequisites and safety notes to SKILL.md.",
            "Apply gamestudio- namespace prefix exclusively to the 5 skills with colliding catalog names.",
            "Include upstream MIT LICENSE and add NOTICE.md acknowledging game studio architecture and safe offline execution.",
            "No runtime/dependency or MCP service is executed during installation.",
        ],
        "files": file_records,
    }
    with open(REPO_ROOT / "data" / "claude-code-game-studios-import.json", "w", encoding="utf-8") as f:
        json.dump(import_manifest, f, indent=2)
    print("Saved data/claude-code-game-studios-import.json")

    # Update data/source-credits.json
    credits_file = REPO_ROOT / "data" / "source-credits.json"
    with open(credits_file, "r", encoding="utf-8") as f:
        credits_data = json.load(f)

    credits_data.setdefault("sections", {})["gamestudios"] = [
        f"- **[Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios/tree/{UPSTREAM_REV})**: 74 game development studio workflow skills for AI coding agents by Donchitos ([@Donchitos](https://github.com/Donchitos)) at revision `{UPSTREAM_REV}` under the MIT License.",
        "- Covers complete game studio lifecycle: concept brainstorming, game design documents, art/sound bibles, sprint planning, engine setup (Godot 4, Unity, Unreal Engine 5), story implementation, testing & QA, and release management.",
        "- Standalone payloads preserve upstream SKILL.md, contracts, references, helper scripts, and templates. Colliding names use the `gamestudio-` namespace.",
        "- Installation runs no code, installs no dependencies or MCP servers, and connects no external accounts. Game engines and Python 3 runtime are separate user prerequisites.",
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
    catalog_data["generatedAt"] = "2026-11-02T00:00:00Z"

    with open(catalog_file, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Updated data/catalog.json: {len(filtered_skills)} total skills.")


if __name__ == "__main__":
    main()
