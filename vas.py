#!/usr/bin/env python3
"""
Vie Agentic Skill (VAS) - CLI & Antigravity Installer
Author: Huy Tran (https://github.com/huytran1120)
License: MIT

Zero-dependency tool to search, inspect, install, and manage 2,951+ agentic skills
specifically designed for Google Antigravity and AI coding agents. No npm/npx required.
"""

import sys
import os
import json
import shutil
import argparse
import re
import stat
import tempfile
from pathlib import Path

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    @classmethod
    def disable(cls):
        cls.HEADER = ''
        cls.BLUE = ''
        cls.CYAN = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.RED = ''
        cls.BOLD = ''
        cls.DIM = ''
        cls.RESET = ''

if not sys.stdout.isatty():
    Colors.disable()

# Base directories
REPO_ROOT = Path(__file__).resolve().parent
SKILLS_DIR = REPO_ROOT / "skills"
INDEX_FILE = REPO_ROOT / "skills_index.json"
MANIFEST_NAME = ".vas-manifest.json"

HOME = Path.home()

# Multi-Agent target configurations: (workspace_relative_dir, global_home_dir, human_label)
AGENT_TARGET_MAP = {
    "antigravity": (Path(".agents/skills"), HOME / ".gemini" / "antigravity" / "skills", "Google Antigravity"),
    "workspace": (Path(".agents/skills"), HOME / ".agents" / "skills", "Workspace Standard (.agents/skills)"),
    "claude": (Path(".claude/skills"), HOME / ".claude" / "skills", "Claude Code"),
    "cursor": (Path(".cursor/skills"), HOME / ".cursor" / "skills", "Cursor IDE"),
    "windsurf": (Path(".windsurf/skills"), HOME / ".codeium" / "windsurf" / "skills", "Windsurf (Codeium)"),
    "codex": (Path(".codex/skills"), HOME / ".codex" / "skills", "OpenAI Codex / OpenCode"),
    "cline": (Path(".cline/skills"), HOME / ".cline" / "skills", "Cline / Roo Code"),
    "copilot": (Path(".github/skills"), HOME / ".copilot" / "skills", "GitHub Copilot CLI"),
    "gemini": (Path(".gemini/skills"), HOME / ".gemini" / "skills", "Google Gemini CLI"),
    "global": (None, HOME / ".gemini" / "antigravity" / "skills", "Antigravity Global"),
    "global-agents": (None, HOME / ".agents" / "skills", "Global Universal (.agents/skills)"),
}

ALL_WORKSPACE_TARGETS = [
    Path(".agents/skills"),
    Path(".claude/skills"),
    Path(".cursor/skills"),
    Path(".windsurf/skills"),
    Path(".codex/skills"),
    Path(".cline/skills"),
    Path(".github/skills"),
]



def load_aliases():
    """Load alias mappings from data/aliases.json if available."""
    aliases_file = REPO_ROOT / "data" / "aliases.json"
    if aliases_file.exists():
        try:
            with open(aliases_file, "r", encoding="utf-8") as f:
                return json.load(f).get("aliases", {})
        except Exception:
            pass
    return {}


def load_category_overrides():
    """Load maintainer category overrides from data/category-overrides.json."""
    overrides_file = REPO_ROOT / "data" / "category-overrides.json"
    if overrides_file.exists():
        try:
            with open(overrides_file, "r", encoding="utf-8") as f:
                return json.load(f).get("overrides", {})
        except Exception:
            pass
    return {}


def load_source_catalog():
    """Load curated metadata from data/catalog.json if available."""
    catalog_file = REPO_ROOT / "data" / "catalog.json"
    if catalog_file.exists():
        try:
            with open(catalog_file, "r", encoding="utf-8") as f:
                return json.load(f).get("skills", [])
        except Exception:
            pass
    return []


def resolve_skill_id(query_id, skills_by_id=None, aliases=None):
    """Resolve aliases, canonical IDs, or subpaths to the canonical skill ID."""
    if aliases is None:
        aliases = load_aliases()
    clean_id = query_id.strip()

    # 1. Direct match in skills_by_id
    if skills_by_id and clean_id in skills_by_id:
        return clean_id

    # 2. Match in aliases map
    if clean_id in aliases:
        aliased = aliases[clean_id]
        if skills_by_id and aliased in skills_by_id:
            return aliased
        return aliased

    # 3. Match canonical_id or trailing subpath (e.g. 2d-games -> game-development/2d-games)
    if skills_by_id:
        for s_id, s_data in skills_by_id.items():
            if s_data.get("canonical_id") == clean_id or s_id.endswith(f"/{clean_id}"):
                return s_id

    return clean_id


def load_index():
    """Load skills index from skills_index.json with fallback to local scan."""
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Failed to read {INDEX_FILE}: {e}{Colors.RESET}", file=sys.stderr)
    return scan_skills_locally()


def scan_skills_locally():
    """Scan skills directory and build an in-memory index, resolving child skills and categories."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills

    overrides = load_category_overrides()
    source_catalog = load_source_catalog()
    catalog_by_key = {}
    for s in source_catalog:
        if s.get("id"):
            catalog_by_key[s["id"]] = s
        if s.get("canonical_id"):
            catalog_by_key[s["canonical_id"]] = s
        if s.get("path"):
            catalog_by_key[s["path"]] = s

    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir():
            continue

        candidates = []
        # Check parent directory
        if (entry / "SKILL.md").exists():
            candidates.append((entry.name, entry / "SKILL.md"))

        # Check subdirectories (child skills) regardless of whether parent has SKILL.md!
        for subentry in sorted(entry.iterdir()):
            if subentry.is_dir() and (subentry / "SKILL.md").exists():
                candidates.append((f"{entry.name}/{subentry.name}", subentry / "SKILL.md"))

        for s_id, smd_path in candidates:
            metadata = extract_skill_metadata(
                smd_path, s_id,
                catalog_by_key=catalog_by_key,
                overrides=overrides
            )
            skills.append(metadata)

    return skills


def extract_skill_metadata(skill_md_path, skill_id, catalog_by_key=None, overrides=None):
    """Extract YAML frontmatter name and description harmonized with catalog sources."""
    if overrides is None:
        overrides = load_category_overrides()
    if catalog_by_key is None:
        catalog_by_key = {}
        for s in load_source_catalog():
            if s.get("id"):
                catalog_by_key[s["id"]] = s
            if s.get("canonical_id"):
                catalog_by_key[s["canonical_id"]] = s
            if s.get("path"):
                catalog_by_key[s["path"]] = s

    base_id = skill_id.split("/")[-1]
    source_meta = catalog_by_key.get(skill_id) or catalog_by_key.get(base_id) or {}
    rel_path = str(skill_md_path.parent.relative_to(REPO_ROOT))

    name = skill_id
    description = source_meta.get("description", "")
    category = "general"
    tags = list(source_meta.get("tags", []))
    risk = source_meta.get("risk", "safe")
    canonical_id = source_meta.get("canonical_id", base_id)
    provenance_fields = (
        "source", "source_repo", "author", "license", "license_source",
        "source_revision", "source_path",
    )
    provenance = {
        key: source_meta[key]
        for key in provenance_fields
        if isinstance(source_meta.get(key), str) and source_meta[key]
    }

    fm_cat = None
    try:
        with open(skill_md_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(8192)

        match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if match:
            fm_text = match.group(1)
            lines = fm_text.splitlines()
            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    i += 1
                    continue

                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("category:"):
                    fm_cat = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("risk:"):
                    risk = line.split(":", 1)[1].strip().strip('"\'')
                elif line.partition(":")[0] in provenance_fields:
                    key, _, value = line.partition(":")
                    provenance[key] = value.strip().strip('"\'')
                elif line.startswith("description:"):
                    val = line.split(":", 1)[1].strip()
                    if val in (">-", ">", "|", "|-") or not val:
                        desc_lines = []
                        i += 1
                        while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                            if lines[i].strip():
                                desc_lines.append(lines[i].strip())
                            i += 1
                        description = " ".join(desc_lines)
                        continue
                    else:
                        description = val.strip('"\'')
                elif line.startswith("tags:"):
                    val = line.split(":", 1)[1].strip()
                    if val.startswith("[") and val.endswith("]"):
                        tags = [t.strip().strip('"\'') for t in val[1:-1].split(",") if t.strip()]
                    else:
                        tag_lines = []
                        i += 1
                        while i < len(lines) and lines[i].startswith("  "):
                            t_stripped = lines[i].strip()
                            if t_stripped.startswith("- "):
                                tag_lines.append(t_stripped[2:].strip().strip('"\''))
                            i += 1
                        tags = tag_lines
                        continue
                i += 1
    except Exception:
        pass

    # Category hierarchy:
    # 1. Maintainer override
    # 2. Curated catalog.json
    # 3. Explicit frontmatter (not default "general")
    # 4. Fallback to "general"
    final_cat = (
        overrides.get(skill_id)
        or overrides.get(base_id)
        or (source_meta.get("category") if source_meta.get("category") else None)
        or (fm_cat if fm_cat and fm_cat != "general" else None)
        or "general"
    )

    return {
        "id": skill_id,
        "canonical_id": canonical_id,
        "name": name or skill_id,
        "path": rel_path,
        "description": description or "No description available",
        "category": final_cat,
        "tags": tags,
        "risk": risk,
        **provenance,
    }


def resolve_target_dirs(target_type, custom_path=None, is_global=False):
    """Determine destination folder(s) across supported AI agents."""
    if target_type == "all" and is_global:
        raise ValueError("--target all cannot be combined with --global; select one agent.")
    if custom_path:
        dest = Path(custom_path).resolve()
        dest.mkdir(parents=True, exist_ok=True)
        return [dest]

    if target_type == "all":
        results = []
        for p in ALL_WORKSPACE_TARGETS:
            res = p.resolve()
            res.mkdir(parents=True, exist_ok=True)
            results.append(res)
        return results

    info = AGENT_TARGET_MAP.get(target_type, AGENT_TARGET_MAP["workspace"])
    ws_dir, glob_dir, _ = info

    if is_global or target_type in ("global", "global-agents"):
        dest = glob_dir
    else:
        dest = (ws_dir or glob_dir).resolve()

    dest.mkdir(parents=True, exist_ok=True)
    return [dest]


def resolve_target_dir(target_type, custom_path=None, is_global=False):
    """Determine the destination folder for skills."""
    return resolve_target_dirs(target_type, custom_path, is_global)[0]


def validate_target_name(name):
    """A receipt may address one immediate child, never a traversable path."""
    if (not isinstance(name, str) or not name or name in (".", "..", MANIFEST_NAME)
            or "/" in name or "\\" in name or ":" in name
            or any(ord(char) < 32 or ord(char) == 127 for char in name)):
        raise ValueError(f"Invalid manifest target name: {name!r}")
    return name


def manifest_target(skill_id, entry):
    return validate_target_name(entry["target_name"] if "target_name" in entry else skill_id.rsplit("/", 1)[-1])


def validate_manifest(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid VAS manifest: expected an object")
    for skill_id, entry in data.items():
        if not isinstance(skill_id, str) or not skill_id or not isinstance(entry, dict):
            raise ValueError("Invalid VAS manifest entry")
        manifest_target(skill_id, entry)
        if entry.get("mode") not in ("link", "copy"):
            raise ValueError(f"Invalid installation mode in manifest for {skill_id}")
    return data


def check_manifest_file(path):
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise ValueError(f"Refusing non-regular or symlinked VAS manifest: {path}")


def load_manifest(dest_dir):
    """Invalid receipts fail closed instead of being mistaken for an empty ledger."""
    manifest_file = dest_dir / MANIFEST_NAME
    check_manifest_file(manifest_file)
    try:
        descriptor = os.open(manifest_file, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except FileNotFoundError:
        return {}
    with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError(f"Refusing non-regular VAS manifest: {manifest_file}")
        return validate_manifest(json.load(stream))


def save_manifest(dest_dir, manifest_data):
    """Replace a complete, flushed receipt without following the destination file."""
    validate_manifest(manifest_data)
    manifest_file = dest_dir / MANIFEST_NAME
    check_manifest_file(manifest_file)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=dest_dir,
                                         prefix=".vas-receipt-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(manifest_data, stream, indent=2, ensure_ascii=False)
            stream.flush()
            os.fsync(stream.fileno())
        check_manifest_file(manifest_file)
        os.replace(temporary, manifest_file)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def target_owners(manifest, target_name):
    return [key for key, entry in manifest.items() if manifest_target(key, entry) == target_name]


def temporary_slot(dest_dir, target_name, purpose):
    """Reserve a unique sibling; never remove a guessed pre-existing temp path."""
    slot = Path(tempfile.mkdtemp(prefix=f".{purpose}_{target_name}_", dir=dest_dir))
    slot.rmdir()
    return slot


def remove_installation(path):
    # The final child may be a skill symlink. Unlink it, never traverse its source.
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


# CLI Subcommands

def cmd_search(args):
    """Search skills by keywords, source repository, or author."""
    query = args.query.lower().strip()
    skills = load_index()
    results = []

    tokens = query.split()
    for s in skills:
        score = 0
        s_id = s.get("id", "").lower()
        s_name = s.get("name", "").lower()
        s_desc = s.get("description", "").lower()
        s_cat = s.get("category", "").lower()
        s_tags = [t.lower() for t in s.get("tags", [])]
        s_source = " ".join(
            s.get(key, "") for key in ("source", "source_repo", "author")
        ).lower()

        if query == s_id:
            score += 100
        elif query in s_id:
            score += 50
        if query in s_name:
            score += 40
        if query == s_cat:
            score += 30
        elif query in s_cat:
            score += 15
        if query in s_tags:
            score += 25
        if query in s_desc:
            score += 10
        if query in s_source:
            score += 20

        # Token matching for multi-word queries
        if len(tokens) > 1:
            token_matches = 0
            for tok in tokens:
                matched_tok = False
                if tok in s_id:
                    score += 25
                    matched_tok = True
                if tok in s_name:
                    score += 15
                    matched_tok = True
                if tok in s_cat:
                    score += 10
                    matched_tok = True
                if any(tok in t for t in s_tags):
                    score += 15
                    matched_tok = True
                if tok in s_desc:
                    score += 5
                    matched_tok = True
                if tok in s_source:
                    score += 10
                    matched_tok = True
                if matched_tok:
                    token_matches += 1
            if token_matches == len(tokens):
                score += 50  # Bonus when all tokens are present

        if score > 0:
            results.append((score, s))

    results.sort(key=lambda x: x[0], reverse=True)
    matched = [s for _, s in results]

    print(f"\n{Colors.BOLD}Found {len(matched)} matching skill(s) for '{query}':{Colors.RESET}\n")

    display_count = min(len(matched), args.limit)
    for i, s in enumerate(matched[:display_count], 1):
        s_id = s.get("id", "unknown")
        s_cat = s.get("category", "general")
        s_desc = s.get("description", "").replace("\n", " ")
        if len(s_desc) > 90:
            s_desc = s_desc[:87] + "..."

        print(f"  {Colors.CYAN}{i:2d}. {Colors.BOLD}{s_id}{Colors.RESET} [{Colors.YELLOW}{s_cat}{Colors.RESET}]")
        print(f"      {Colors.DIM}{s_desc}{Colors.RESET}")

    if len(matched) > display_count:
        print(f"\n  {Colors.DIM}... and {len(matched) - display_count} more. Use --limit to show more.{Colors.RESET}")
    print()


def cmd_list(args):
    """List skills with optional category or tag filtering."""
    skills = load_index()
    filtered = skills

    if args.category:
        cat = args.category.lower()
        filtered = [s for s in filtered if s.get("category", "").lower() == cat]

    if args.tag:
        tag = args.tag.lower()
        filtered = [s for s in filtered if tag in [t.lower() for t in s.get("tags", [])]]

    print(f"\n{Colors.BOLD}Listing skills ({len(filtered)} total){Colors.RESET}")
    if args.category:
        print(f"  Category: {Colors.YELLOW}{args.category}{Colors.RESET}")
    if args.tag:
        print(f"  Tag: {Colors.YELLOW}{args.tag}{Colors.RESET}")
    print()

    limit = args.limit if args.limit > 0 else len(filtered)
    for i, s in enumerate(filtered[:limit], 1):
        s_id = s.get("id", "unknown")
        s_cat = s.get("category", "general")
        s_desc = s.get("description", "").replace("\n", " ")
        if len(s_desc) > 80:
            s_desc = s_desc[:77] + "..."
        print(f"  {Colors.CYAN}{i:3d}. {Colors.BOLD}{s_id:<32}{Colors.RESET} [{Colors.YELLOW}{s_cat:<16}{Colors.RESET}] {Colors.DIM}{s_desc}{Colors.RESET}")

    if len(filtered) > limit:
        print(f"\n  {Colors.DIM}... and {len(filtered) - limit} more. Use --limit {len(filtered)} to show all.{Colors.RESET}")
    print()


def cmd_show(args):
    """Show detailed metadata and preview SKILL.md of a skill."""
    raw_id = args.skill_id.strip()
    skills = load_index()
    skills_by_id = {s.get("id"): s for s in skills}
    aliases = load_aliases()

    resolved_id = resolve_skill_id(raw_id, skills_by_id, aliases)
    skill = skills_by_id.get(resolved_id)

    # Fallback to local directory check
    if not skill:
        for cand in [SKILLS_DIR / resolved_id, SKILLS_DIR / raw_id]:
            if cand.is_dir() and (cand / "SKILL.md").exists():
                skill = extract_skill_metadata(cand / "SKILL.md", resolved_id)
                break

    if not skill:
        print(f"{Colors.RED}Skill '{raw_id}' not found.{Colors.RESET}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{Colors.HEADER}======================================================================{Colors.RESET}")
    print(f"{Colors.BOLD}Skill:{Colors.RESET}        {Colors.GREEN}{skill.get('id')}{Colors.RESET}")
    print(f"{Colors.BOLD}Name:{Colors.RESET}         {skill.get('name', 'N/A')}")
    print(f"{Colors.BOLD}Category:{Colors.RESET}     {Colors.YELLOW}{skill.get('category', 'N/A')}{Colors.RESET}")
    print(f"{Colors.BOLD}Risk Level:{Colors.RESET}   {skill.get('risk', 'safe')}")
    print(f"{Colors.BOLD}Source:{Colors.RESET}       {skill.get('source_repo') or skill.get('source', 'personal/community')}")
    if skill.get("author"):
        print(f"{Colors.BOLD}Author:{Colors.RESET}       {skill['author']}")
    if skill.get("license"):
        print(f"{Colors.BOLD}License:{Colors.RESET}      {skill['license']}")
    print(f"{Colors.BOLD}Tags:{Colors.RESET}         {', '.join(skill.get('tags', [])) or 'None'}")
    print(f"{Colors.BOLD}Path:{Colors.RESET}         {skill.get('path', 'N/A')}")
    print(f"{Colors.BOLD}Description:{Colors.RESET}  {skill.get('description', 'N/A')}")
    print(f"{Colors.HEADER}======================================================================{Colors.RESET}\n")

    # Read SKILL.md preview
    skill_path = REPO_ROOT / skill.get("path", f"skills/{resolved_id}")
    skill_md = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
    if not skill_md.exists() and (SKILLS_DIR / resolved_id / "SKILL.md").exists():
        skill_md = SKILLS_DIR / resolved_id / "SKILL.md"

    if skill_md.exists():
        print(f"{Colors.BOLD}Preview of {skill_md.name}:{Colors.RESET}\n")
        try:
            with open(skill_md, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                preview_lines = lines[:40]
                for line in preview_lines:
                    print(f"  {line.rstrip()}")
                if len(lines) > 40:
                    print(f"\n  {Colors.DIM}... ({len(lines) - 40} lines remaining in full file) ...{Colors.RESET}")
        except Exception as e:
            print(f"  {Colors.RED}Could not read SKILL.md: {e}{Colors.RESET}")
    print()


def cmd_categories(args):
    """List all categories with skill counts."""
    skills = load_index()
    cats = {}
    for s in skills:
        c = s.get("category", "uncategorized")
        cats[c] = cats.get(c, 0) + 1

    sorted_cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    print(f"\n{Colors.BOLD}Vie Agentic Skill Categories ({len(sorted_cats)} total):{Colors.RESET}\n")
    for cat, count in sorted_cats:
        print(f"  - {Colors.YELLOW}{cat:<24}{Colors.RESET} ({count:3d} skills)")
    print(f"\n{Colors.DIM}Filter with: ./vas list --category <name>{Colors.RESET}\n")


def cmd_tags(args):
    """List popular tags with skill counts."""
    skills = load_index()
    tags = {}
    for s in skills:
        for t in s.get("tags", []):
            tags[t] = tags.get(t, 0) + 1

    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    limit = args.limit if args.limit > 0 else 50
    print(f"\n{Colors.BOLD}Top Tags in Vie Agentic Skill (showing {min(limit, len(sorted_tags))} of {len(tags)}):{Colors.RESET}\n")
    for tag, count in sorted_tags[:limit]:
        print(f"  - {Colors.CYAN}{tag:<24}{Colors.RESET} ({count:3d} skills)")
    print(f"\n{Colors.DIM}Filter with: ./vas list --tag <tag>{Colors.RESET}\n")


def cmd_install(args):
    """Install skill(s) into workspace or global configuration across AI agents."""
    dest_dirs = resolve_target_dirs(args.target, args.dest, getattr(args, 'is_global', False))
    skills = load_index()
    skills_by_id = {s.get("id"): s for s in skills}
    aliases = load_aliases()

    targets_to_install = []

    if args.all:
        target_names = ", ".join(str(d) for d in dest_dirs)
        confirm = input(f"{Colors.RED}{Colors.BOLD}WARNING:{Colors.RESET} Installing all {len(skills)} skills into {target_names}? [y/N]: ")
        if confirm.lower() != 'y':
            print("Aborted.")
            sys.exit(1)
        targets_to_install = list(skills_by_id.keys())
    elif args.category:
        cat = args.category.lower()
        matched = [s.get("id") for s in skills if s.get("category", "").lower() == cat]
        if not matched:
            print(f"{Colors.RED}No skills found in category '{args.category}'.{Colors.RESET}")
            sys.exit(1)
        print(f"Selected {len(matched)} skill(s) in category '{args.category}'.")
        targets_to_install.extend(matched)
    elif args.tag:
        tag = args.tag.lower()
        matched = [s.get("id") for s in skills if tag in [t.lower() for t in s.get("tags", [])]]
        if not matched:
            print(f"{Colors.RED}No skills found with tag '{args.tag}'.{Colors.RESET}")
            sys.exit(1)
        print(f"Selected {len(matched)} skill(s) with tag '{args.tag}'.")
        targets_to_install.extend(matched)
    elif args.skill_ids:
        targets_to_install.extend(args.skill_ids)
    else:
        print(f"{Colors.RED}Error: Provide skill ID(s), --category, --tag, or --all.{Colors.RESET}")
        sys.exit(1)

    total_installed = 0
    total_failed = 0

    for dest_dir in dest_dirs:
        dest_dir = dest_dir.resolve()
        dest_dir.mkdir(parents=True, exist_ok=True)
        manifest = load_manifest(dest_dir)
        print(f"\n{Colors.BOLD}Installing {len(targets_to_install)} skill(s) for target:{Colors.RESET}")
        print(f"  Destination: {Colors.CYAN}{dest_dir}{Colors.RESET}")
        print(f"  Mode:        {Colors.YELLOW}{args.mode}{Colors.RESET}\n")

        installed_count = 0
        for raw_id in targets_to_install:
            raw_id = raw_id.strip()
            s_id = resolve_skill_id(raw_id, skills_by_id, aliases)

            # Locate source skill directory
            source_dir = None
            if s_id in skills_by_id:
                rel_path = skills_by_id[s_id].get("path", f"skills/{s_id}")
                candidate = REPO_ROOT / rel_path
                if candidate.is_dir():
                    source_dir = candidate

            if not source_dir:
                for cand in [SKILLS_DIR / s_id, SKILLS_DIR / raw_id]:
                    if cand.is_dir() and (cand / "SKILL.md").exists():
                        source_dir = cand
                        break

            if not source_dir or not (source_dir / "SKILL.md").exists():
                print(f"  {Colors.RED}✗{Colors.RESET} Skill '{raw_id}' not found or missing SKILL.md. Skipped.")
                total_failed += 1
                continue

            target_name = validate_target_name(source_dir.name)
            target_skill_dir = dest_dir / target_name
            owners = target_owners(manifest, target_name)
            if any(owner != s_id for owner in owners):
                print(f"  {Colors.RED}✗{Colors.RESET} Conflict: '{target_name}' belongs to another skill: {', '.join(owners)}. Skipped.")
                total_failed += 1
                continue
            if s_id in manifest and manifest_target(s_id, manifest[s_id]) != target_name:
                print(f"  {Colors.RED}✗{Colors.RESET} Conflict: {s_id} is recorded at a different destination. Skipped.")
                total_failed += 1
                continue
            if (target_skill_dir.exists() or target_skill_dir.is_symlink()) and s_id not in manifest:
                print(f"  {Colors.RED}✗{Colors.RESET} Conflict: '{target_name}' is not managed by VAS. Existing contents preserved.")
                total_failed += 1
                continue

            # Staging below the source would recursively copy its own output.
            source_resolved = source_dir.resolve()
            if dest_dir.is_relative_to(source_resolved):
                print(f"  {Colors.RED}✗{Colors.RESET} Destination overlaps source directory in catalog. Skipped.")
                total_failed += 1
                continue
            if target_skill_dir.exists() and not target_skill_dir.is_symlink():
                existing = target_skill_dir.resolve()
                if existing == source_resolved or source_resolved.is_relative_to(existing):
                    print(f"  {Colors.RED}✗{Colors.RESET} Destination overlaps or matches source directory in catalog. Skipped.")
                    total_failed += 1
                    continue

            staging_dir = temporary_slot(dest_dir, target_name, "tmp")
            backup_dir = None
            replacement_ready = False
            try:
                if args.mode == "link":
                    try:
                        rel_target = os.path.relpath(source_resolved, dest_dir)
                        os.symlink(rel_target, staging_dir)
                    except ValueError:
                        os.symlink(source_resolved, staging_dir)
                    mode_label = "linked"
                else:
                    shutil.copytree(source_resolved, staging_dir)
                    mode_label = "copied"

                if target_skill_dir.exists() or target_skill_dir.is_symlink():
                    backup_dir = temporary_slot(dest_dir, target_name, "bak")
                    target_skill_dir.rename(backup_dir)

                staging_dir.rename(target_skill_dir)
                replacement_ready = True

                updated = dict(manifest)
                updated[s_id] = {
                    "installed_at": target_skill_dir.stat().st_mtime,
                    "mode": args.mode,
                    "source": str(source_resolved),
                    "target_name": target_name,
                    "category": skills_by_id.get(s_id, {}).get("category", "general")
                }
                # Keep the old payload until its replacement receipt is durable.
                save_manifest(dest_dir, updated)
            except Exception as e:
                total_failed += 1
                recovery_error = None
                try:
                    remove_installation(staging_dir)
                    if replacement_ready:
                        remove_installation(target_skill_dir)
                    if backup_dir and (backup_dir.exists() or backup_dir.is_symlink()):
                        backup_dir.rename(target_skill_dir)
                except OSError as error:
                    recovery_error = error
                # Recovery must not depend on an available/Unicode-capable terminal.
                print(f"  {Colors.RED}✗{Colors.RESET} Failed to install {s_id}: {e}")
                if recovery_error is not None:
                    print(f"  Recovery needs attention; original backup: {backup_dir}. {recovery_error}", file=sys.stderr)
                continue

            manifest = updated
            installed_count += 1
            total_installed += 1
            if backup_dir:
                try:
                    remove_installation(backup_dir)
                except OSError as cleanup_error:
                    print(f"  Warning: installation saved; old backup retained at {backup_dir}: {cleanup_error}", file=sys.stderr)
            print(f"  {Colors.GREEN}✓{Colors.RESET} {s_id} ({mode_label})")

        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Successfully installed {installed_count} skill(s) into {dest_dir}.{Colors.RESET}")

    if total_installed == 0 or total_failed > 0:
        sys.exit(1)


def cmd_uninstall(args):
    """Uninstall skill(s) from workspace or global configuration across AI agents."""
    dest_dirs = resolve_target_dirs(args.target, args.dest, getattr(args, 'is_global', False))
    to_remove = args.skill_ids
    if not to_remove:
        print(f"{Colors.RED}Specify skill ID(s) to uninstall.{Colors.RESET}")
        sys.exit(1)

    aliases = load_aliases()
    skills = load_index()
    skills_by_id = {s.get("id"): s for s in skills}

    total_removed = 0
    total_failed = 0

    for dest_dir in dest_dirs:
        dest_dir = dest_dir.resolve()
        manifest = load_manifest(dest_dir)
        print(f"\n{Colors.BOLD}Uninstalling from {dest_dir}:{Colors.RESET}\n")
        removed_count = 0
        for raw_id in to_remove:
            clean_id = raw_id.strip()
            s_id = resolve_skill_id(clean_id, skills_by_id, aliases)

            receipt_key = None
            if s_id in manifest:
                receipt_key = s_id
            elif clean_id in manifest:
                receipt_key = clean_id
            elif s_id not in skills_by_id and clean_id not in skills_by_id:
                # Legacy/removed catalog IDs may be addressed by a unique basename.
                matches = [key for key, entry in manifest.items()
                           if manifest_target(key, entry) == clean_id or key.rsplit("/", 1)[-1] == clean_id]
                if len(matches) == 1:
                    receipt_key = matches[0]

            if receipt_key is None:
                print(f"  {Colors.RED}✗{Colors.RESET} {clean_id} has no matching VAS receipt; existing contents preserved.")
                total_failed += 1
                continue

            target_name = manifest_target(receipt_key, manifest[receipt_key])
            owners = target_owners(manifest, target_name)
            if owners != [receipt_key]:
                print(f"  {Colors.RED}✗{Colors.RESET} Conflict: '{target_name}' has multiple recorded owners; nothing removed.")
                total_failed += 1
                continue
            target_skill_dir = dest_dir / target_name
            updated = {key: entry for key, entry in manifest.items() if key != receipt_key}

            if target_skill_dir.exists() or target_skill_dir.is_symlink():
                backup_dir = temporary_slot(dest_dir, target_name, "remove")
                moved = False
                try:
                    # With a validated single-component name, only the last child
                    # can be a symlink. Rename/unlink never follow that link.
                    target_skill_dir.rename(backup_dir)
                    moved = True
                    save_manifest(dest_dir, updated)
                except Exception as e:
                    if moved:
                        backup_dir.rename(target_skill_dir)
                    print(f"  {Colors.RED}✗{Colors.RESET} Error removing {clean_id}: {e}")
                    total_failed += 1
                    continue
                manifest = updated
                removed_count += 1
                total_removed += 1
                try:
                    remove_installation(backup_dir)
                except OSError as cleanup_error:
                    print(f"  Warning: removed receipt; retained payload at {backup_dir}: {cleanup_error}", file=sys.stderr)
                    total_failed += 1
                print(f"  {Colors.GREEN}✓{Colors.RESET} Removed {clean_id}")
            else:
                save_manifest(dest_dir, updated)
                manifest = updated
                print(f"  {Colors.YELLOW}-{Colors.RESET} {clean_id} is not installed in {dest_dir}")
                total_failed += 1

        print(f"\n{Colors.GREEN}Removed {removed_count} skill(s) from {dest_dir}.{Colors.RESET}\n")

    if total_removed == 0 or total_failed > 0:
        sys.exit(1)


def cmd_status(args):
    """Show currently installed skills across target AI agents."""
    dest_dirs = resolve_target_dirs(args.target, args.dest, getattr(args, 'is_global', False))

    for dest_dir in dest_dirs:
        dest_dir = dest_dir.resolve()
        manifest = load_manifest(dest_dir)
        print(f"\n{Colors.BOLD}Skills Status in:{Colors.RESET} {Colors.CYAN}{dest_dir}{Colors.RESET}\n")

        skills_on_disk = []
        if dest_dir.exists():
            for item in sorted(dest_dir.iterdir()):
                if item.name.startswith("."):
                    continue
                if item.is_dir() or item.is_symlink():
                    if (item / "SKILL.md").exists() or item.name in manifest:
                        is_link = item.is_symlink()
                        skills_on_disk.append((item.name, is_link))

        if not skills_on_disk:
            print(f"  {Colors.YELLOW}No skills currently installed.{Colors.RESET}")
            print(f"  Install some with: ./vas install <skill_id> --target {args.target}")
        else:
            print(f"  Total installed: {Colors.GREEN}{len(skills_on_disk)}{Colors.RESET}\n")
            for name, is_link in skills_on_disk:
                tag = f"{Colors.BLUE}[symlink]{Colors.RESET}" if is_link else f"{Colors.YELLOW}[copied]{Colors.RESET}"
                cat = manifest.get(name, {}).get("category", "")
                if not cat:
                    for k, v in manifest.items():
                        if v.get("target_name") == name or Path(k).name == name:
                            cat = v.get("category", "")
                            break
                cat_label = f"[{cat}]" if cat else ""
                print(f"  - {Colors.BOLD}{name:<32}{Colors.RESET} {tag} {Colors.DIM}{cat_label}{Colors.RESET}")
        print()


def cmd_init(args):
    """Initialize the current working directory as an Antigravity workspace with .agents/skills."""
    target_dir = Path(".agents/skills").resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    meta_skill_dir = target_dir / "vie-agentic-skill"

    # Avoid writing through symlinks into catalog repository
    if meta_skill_dir.is_symlink():
        meta_skill_dir.unlink()
    meta_skill_dir.mkdir(parents=True, exist_ok=True)

    meta_skill_md = meta_skill_dir / "SKILL.md"
    if meta_skill_md.is_symlink():
        meta_skill_md.unlink()

    # Space-safe quoting for REPO_ROOT / vas.py
    vas_path = REPO_ROOT / "vas.py"
    vas_cmd = f'"{vas_path}"'

    content = f"""---
name: vie-agentic-skill
description: >-
  Use this skill to search, inspect, and install curated agentic skills from the
  Vie Agentic Skill (VAS) catalog into this Antigravity project.
---

# Vie Agentic Skill (VAS)

This workspace is enabled with Vie Agentic Skill catalog.

## Commands

Search skills:
`python3 {vas_cmd} search <keyword>`

Install a skill to this workspace:
`python3 {vas_cmd} install <skill_id> --target workspace`

List categories:
`python3 {vas_cmd} categories`
"""
    with open(meta_skill_md, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Antigravity workspace initialized!{Colors.RESET}")
    print(f"  Created: {Colors.CYAN}{target_dir}{Colors.RESET}")
    print(f"  Installed meta-skill: {Colors.BOLD}vie-agentic-skill{Colors.RESET}\n")


def cmd_sync(args):
    """Rebuild skills_index.json and docs/skills.min.json from the skills directory."""
    print(f"\n{Colors.BOLD}Scanning skills directory to rebuild index...{Colors.RESET}")
    scanned = scan_skills_locally()
    print(f"Scanned {len(scanned)} skills.")

    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(scanned, f, indent=2, ensure_ascii=False)
        print(f"{Colors.GREEN}✓ Successfully saved {INDEX_FILE}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error writing index: {e}{Colors.RESET}")
        sys.exit(1)

    min_file = REPO_ROOT / "docs" / "skills.min.json"
    if min_file.parent.exists():
        try:
            with open(min_file, "w", encoding="utf-8") as f:
                json.dump(scanned, f, separators=(",", ":"), ensure_ascii=False)
            print(f"{Colors.GREEN}✓ Successfully saved {min_file}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Could not save minified index: {e}{Colors.RESET}")

    # Update CATALOG.md
    catalog_md = REPO_ROOT / "CATALOG.md"
    try:
        categories = {}
        for s in scanned:
            cat = s.get("category", "general")
            categories.setdefault(cat, []).append(s)

        lines = [
            "# Vie Agentic Skill (VAS) - Catalog",
            "",
            f"Tổng hợp **{len(scanned):,}** kỹ năng Agentic tiêu chuẩn hóa, chia theo **{len(categories)}** danh mục chuyên biệt.",
            "",
            "| Danh mục | Số lượng | Lệnh cài đặt nhanh |",
            "| :--- | :---: | :--- |",
        ]
        for cat in sorted(categories.keys()):
            cnt = len(categories[cat])
            lines.append(f"| **{cat}** | {cnt} skills | `./vas install --category {cat} --target codex` |")

        lines.extend([
            "",
            "---",
            "",
            "## Chi Tiết Các Kỹ Năng",
            "",
        ])
        for cat in sorted(categories.keys()):
            lines.append(f"### {cat.upper()} ({len(categories[cat])} skills)")
            lines.append("")
            lines.append("| Skill ID | Rủi ro | Mô tả tóm tắt |")
            lines.append("| :--- | :---: | :--- |")
            for s in sorted(categories[cat], key=lambda x: x.get("id", "")):
                s_id = s.get("id")
                risk = s.get("risk", "safe")
                desc = s.get("description", "").replace("\n", " ")
                if len(desc) > 80:
                    desc = desc[:77] + "..."
                lines.append(f"| `{s_id}` | `{risk}` | {desc} |")
            lines.append("")

        with open(catalog_md, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{Colors.GREEN}✓ Successfully generated {catalog_md}{Colors.RESET}\n")
    except Exception as e:
        print(f"{Colors.YELLOW}Warning: Could not update CATALOG.md: {e}{Colors.RESET}\n")
    except Exception as e:
        print(f"{Colors.RED}✗ Error writing index: {e}{Colors.RESET}\n")


def cmd_antigravity_guide(args):
    """Print architectural guide on using VAS with all supported AI agents."""
    print(f"""
{Colors.HEADER}{Colors.BOLD}======================================================================
  Vie Agentic Skill (VAS) - Universal Multi-Agent Guide
======================================================================{Colors.RESET}

{Colors.BOLD}1. Universal Agent Skills Architecture:{Colors.RESET}
   VAS adheres to the Open Agent Skills specification (agentskills.io).
   All playbooks (SKILL.md) are vendor-neutral and natively executable by:
   - Google Antigravity (.agents/skills)
   - Claude Code (.claude/skills)
   - Cursor (.cursor/skills)
   - Windsurf by Codeium (.windsurf/skills)
   - OpenAI Codex / OpenCode (.codex/skills or .agents/skills)
   - Cline / Roo Code (.cline/skills)
   - GitHub Copilot CLI (.github/skills)

{Colors.BOLD}2. Progressive Disclosure Across Agents:{Colors.RESET}
   Agents only load the concise frontmatter summary at startup.
   The full detailed playbook and scripts are loaded into memory ONLY
   when you ask a relevant question, saving up to 99% of prompt tokens!

{Colors.BOLD}3. Common Workflows (Zero NPX):{Colors.RESET}
   - Search for a skill:
     {Colors.CYAN}./vas search security{Colors.RESET}
   - View details:
     {Colors.CYAN}./vas show ui-ux-pro-max{Colors.RESET}
   - Install for Google Antigravity (or universal standard):
     {Colors.CYAN}./vas install ui-ux-pro-max --target antigravity --mode link{Colors.RESET}
   - Install for OpenAI Codex:
     {Colors.CYAN}./vas install ui-ux-pro-max --target codex --mode link{Colors.RESET}
   - Install for Claude Code:
     {Colors.CYAN}./vas install ui-ux-pro-max --target claude --mode link{Colors.RESET}
   - Install for Cursor:
     {Colors.CYAN}./vas install ui-ux-pro-max --target cursor --mode link{Colors.RESET}
   - Install for Windsurf:
     {Colors.CYAN}./vas install ui-ux-pro-max --target windsurf --mode link{Colors.RESET}
   - Install for Cline / Roo Code:
     {Colors.CYAN}./vas install ui-ux-pro-max --target cline --mode link{Colors.RESET}
   - Install for GitHub Copilot CLI:
     {Colors.CYAN}./vas install ui-ux-pro-max --target copilot --mode link{Colors.RESET}
   - Install for ALL AI agents at once:
     {Colors.CYAN}./vas install ui-ux-pro-max --target all{Colors.RESET}
   - Check installed skills:
     {Colors.CYAN}./vas status --target codex{Colors.RESET}

{Colors.HEADER}======================================================================{Colors.RESET}
""")


def main():
    TARGET_CHOICES = [
        "workspace", "antigravity", "claude", "cursor",
        "windsurf", "codex", "cline", "copilot", "gemini",
        "global", "global-agents", "all"
    ]

    parser = argparse.ArgumentParser(
        prog="vas",
        description="Vie Agentic Skill (VAS) - Universal AI Agent Skills Manager (Zero NPX)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # search
    p_search = subparsers.add_parser("search", help="Search skills by keyword")
    p_search.add_argument("query", help="Keyword to search for")
    p_search.add_argument("--limit", type=int, default=20, help="Max results to display (default: 20)")
    p_search.set_defaults(func=cmd_search)

    # list
    p_list = subparsers.add_parser("list", help="List skills with optional filters")
    p_list.add_argument("--category", "-c", help="Filter by category")
    p_list.add_argument("--tag", "-t", help="Filter by tag")
    p_list.add_argument("--limit", "-l", type=int, default=50, help="Max skills to show (default: 50)")
    p_list.set_defaults(func=cmd_list)

    # show / info
    p_show = subparsers.add_parser("show", aliases=["info"], help="Display skill details and preview")
    p_show.add_argument("skill_id", help="Exact skill ID")
    p_show.set_defaults(func=cmd_show)

    # categories
    p_cats = subparsers.add_parser("categories", help="List all skill categories")
    p_cats.set_defaults(func=cmd_categories)

    # tags
    p_tags = subparsers.add_parser("tags", help="List popular skill tags")
    p_tags.add_argument("--limit", type=int, default=50, help="Max tags to display")
    p_tags.set_defaults(func=cmd_tags)

    # install
    p_install = subparsers.add_parser("install", help="Install skills for AI agents (Antigravity, Claude, Cursor, Codex, Windsurf, Cline, Copilot)")
    p_install.add_argument("skill_ids", nargs="*", help="Skill ID(s) to install")
    p_install.add_argument("--target", choices=TARGET_CHOICES, default="workspace",
                           help="Target AI agent: workspace, antigravity, claude, cursor, windsurf, codex, cline, copilot, all (default: workspace -> .agents/skills)")
    p_install.add_argument("--mode", choices=["copy", "link"], default="link",
                           help="Installation mode: link (symlink, zero disk space, auto updates) or copy (default: link)")
    p_install.add_argument("--global", dest="is_global", action="store_true",
                           help="Install globally in user's home directory for the selected target")
    p_install.add_argument("--dest", help="Custom destination directory")
    p_install.add_argument("--category", "-c", help="Install all skills in this category")
    p_install.add_argument("--tag", "-t", help="Install all skills with this tag")
    p_install.add_argument("--all", action="store_true", help="Install ALL catalog skills")
    p_install.set_defaults(func=cmd_install)

    # uninstall / remove
    p_uninst = subparsers.add_parser("uninstall", aliases=["remove"], help="Uninstall skills from target agent")
    p_uninst.add_argument("skill_ids", nargs="+", help="Skill ID(s) to uninstall")
    p_uninst.add_argument("--target", choices=TARGET_CHOICES, default="workspace")
    p_uninst.add_argument("--global", dest="is_global", action="store_true",
                          help="Uninstall from user's global config directory for the selected target")
    p_uninst.add_argument("--dest", help="Custom destination directory")
    p_uninst.set_defaults(func=cmd_uninstall)

    # status
    p_status = subparsers.add_parser("status", help="Show installed skills for target agent")
    p_status.add_argument("--target", choices=TARGET_CHOICES, default="workspace")
    p_status.add_argument("--global", dest="is_global", action="store_true",
                          help="Inspect user's global directory for the selected target")
    p_status.add_argument("--dest", help="Custom destination directory")
    p_status.set_defaults(func=cmd_status)

    # init
    p_init = subparsers.add_parser("init", help="Initialize workspace for AI agents")
    p_init.set_defaults(func=cmd_init)

    # sync
    p_sync = subparsers.add_parser("sync", help="Rebuild skills_index.json")
    p_sync.set_defaults(func=cmd_sync)

    # guide
    p_guide = subparsers.add_parser("guide", help="Multi-agent integration guide")
    p_guide.set_defaults(func=cmd_antigravity_guide)

    args = parser.parse_args()
    if hasattr(args, "func"):
        try:
            args.func(args)
        except (ValueError, OSError) as error:
            parser.exit(1, f"Error: {error}\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
