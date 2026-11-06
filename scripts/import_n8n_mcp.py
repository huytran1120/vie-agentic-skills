#!/usr/bin/env python3
"""
Import genuinely new skills from czlonkowski/n8n-mcp into Vie Agentic Skill (VAS).
14 of the 15 skills in data/skills/* already exist in the VAS catalog and are skipped.
Only `n8n-self-hosting` is genuinely new and imported at commit 1c755c5c8d99eb71faade17753a7f24138f4212c.
"""

import hashlib
import json
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO_SLUG = "czlonkowski/n8n-mcp"
UPSTREAM_REV = "1c755c5c8d99eb71faade17753a7f24138f4212c"
AUTHOR = "Romuald Czlonkowski"
AUTHOR_URL = "https://github.com/czlonkowski"
LICENSE_NAME = "MIT"
LICENSE_URL = f"https://github.com/{UPSTREAM_REPO_SLUG}/blob/{UPSTREAM_REV}/LICENSE"
IMPORT_PATHS = (
    "skills/n8n-self-hosting",
    "data/n8n-mcp-import.json",
    "data/source-credits.json",
    "data/catalog.json",
)

SKIPPED_SKILLS = [
    "n8n-agents",
    "n8n-binary-and-data",
    "n8n-code-javascript",
    "n8n-code-python",
    "n8n-code-tool",
    "n8n-error-handling",
    "n8n-expression-syntax",
    "n8n-mcp-tools-expert",
    "n8n-multi-instance",
    "n8n-node-configuration",
    "n8n-subworkflows",
    "n8n-validation-expert",
    "n8n-workflow-patterns",
    "using-n8n-mcp-skills",
]

UPSTREAM_FILES = [
    "SKILL.md",
    "README.md",
    "CREDENTIAL_OVERWRITES.md",
    "DAY2.md",
    "QUEUE_MODE.md",
    "SECURITY.md",
    "SINGLE_MODE.md",
    "assets/.env.queue.example",
    "assets/.env.single.example",
    "assets/Caddyfile",
    "assets/docker-compose.queue.yml",
    "assets/docker-compose.single.yml",
    "assets/init-data.sh",
]

TAGS = [
    "n8n",
    "self-hosting",
    "docker",
    "docker-compose",
    "postgres",
    "redis",
    "caddy",
    "queue-mode",
    "devops",
    "automation",
    "n8n-mcp",
]

NOTICE_TEXT = f"""# Notices

`n8n-self-hosting` is imported from [{UPSTREAM_REPO_SLUG}](https://github.com/{UPSTREAM_REPO_SLUG}) at revision `{UPSTREAM_REV}` under the MIT License (Copyright (c) 2024 Romuald Czlonkowski @ www.aiadvisors.pl/en); see `LICENSE`.

## Runtime & Infrastructure Prerequisites

- Deploying self-hosted n8n stacks requires Docker Engine and Docker Compose v2 on your target host, along with a domain name and DNS A/AAAA record if using automatic TLS via Caddy.
- All configuration templates (`assets/docker-compose.single.yml`, `assets/docker-compose.queue.yml`, `assets/.env.single.example`, `assets/.env.queue.example`, `assets/Caddyfile`, `assets/init-data.sh`) are shipped as static reference files inside `assets/` and never contain live secrets.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No scripts or containers are executed, no runtime or MCP server is installed, and no external services are connected during installation.
"""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def fetch_bytes(rel_path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/{UPSTREAM_REPO_SLUG}/{UPSTREAM_REV}/{rel_path}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read()


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[2].lstrip("\r\n")


def stage_import(staging_root):
    canonical_id = "n8n-self-hosting"
    category = "automation"
    dest_dir = staging_root / "skills" / canonical_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    (staging_root / "data").mkdir()

    file_records = []

    # 1. Fetch and write LICENSE
    license_bytes = fetch_bytes("LICENSE")
    if not license_bytes.strip():
        raise ValueError("Empty upstream LICENSE")
    lic_file = dest_dir / "LICENSE"
    lic_file.write_bytes(license_bytes)
    lic_file.chmod(0o644)
    file_records.append({
        "source_path": "LICENSE",
        "path": f"skills/{canonical_id}/LICENSE",
        "source_sha256": sha256_bytes(license_bytes),
        "sha256": sha256_file(lic_file),
        "executable": False,
    })

    # 2. Write NOTICE.md
    not_file = dest_dir / "NOTICE.md"
    not_file.write_text(NOTICE_TEXT.strip() + "\n", encoding="utf-8")
    not_file.chmod(0o644)
    file_records.append({
        "source_path": f"data/skills/{canonical_id}/NOTICE.md",
        "path": f"skills/{canonical_id}/NOTICE.md",
        "source_sha256": sha256_file(not_file),
        "sha256": sha256_file(not_file),
        "executable": False,
    })

    # 3. Fetch and write all upstream files in data/skills/n8n-self-hosting
    description = ""
    for rel in UPSTREAM_FILES:
        upstream_rel = f"data/skills/{canonical_id}/{rel}"
        raw_bytes = fetch_bytes(upstream_rel)
        if not raw_bytes.strip():
            raise ValueError(f"Empty upstream file: {upstream_rel}")
        source_hash = sha256_bytes(raw_bytes)
        out_path = dest_dir / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if rel == "SKILL.md":
            raw_text = raw_bytes.decode("utf-8")
            fm, body = parse_frontmatter(raw_text)
            if not fm.get("name") or not fm.get("description") or not body.strip():
                raise ValueError(f"Invalid upstream runbook: {upstream_rel}")
            description = fm["description"].replace('"', "'")
            tags_str = json.dumps(TAGS)
            new_fm = (
                f"---\n"
                f"name: {canonical_id}\n"
                f'description: "{description}"\n'
                f"category: {category}\n"
                f"tags: {tags_str}\n"
                f"risk: safe\n"
                f'author: "{AUTHOR}"\n'
                f'license: "{LICENSE_NAME}"\n'
                f'source_repo: "{UPSTREAM_REPO_SLUG}"\n'
                f'source_revision: "{UPSTREAM_REV}"\n'
                f'source_path: "{upstream_rel}"\n'
                f"---\n\n"
            )
            footer = (
                f"\n\n---\n\n"
                f"## VAS installation notes\n\n"
                f"- Canonical ID: `{canonical_id}`\n"
                f"- Source repository: [`{UPSTREAM_REPO_SLUG}`](https://github.com/{UPSTREAM_REPO_SLUG}) at commit `{UPSTREAM_REV}` (`{upstream_rel}`).\n"
                f"- License: MIT (Copyright (c) 2024 Romuald Czlonkowski @ www.aiadvisors.pl/en); see `LICENSE` and `NOTICE.md`.\n"
                f"- Bundled references and assets: `SINGLE_MODE.md`, `QUEUE_MODE.md`, `SECURITY.md`, `CREDENTIAL_OVERWRITES.md`, `DAY2.md`, `README.md`, and `assets/` (`docker-compose.single.yml`, `docker-compose.queue.yml`, `.env.single.example`, `.env.queue.example`, `Caddyfile`, `init-data.sh`).\n"
                f"- Install via CLI: `./vas install {canonical_id} --target <agent> --mode link` (or `--mode copy`).\n"
            )
            out_path.write_text(new_fm + body.rstrip() + footer, encoding="utf-8")
            out_path.chmod(0o644)
            is_exec = False
        else:
            out_path.write_bytes(raw_bytes)
            is_exec = rel.endswith(".sh")
            out_path.chmod(0o755 if is_exec else 0o644)

        file_records.append({
            "source_path": upstream_rel,
            "path": f"skills/{canonical_id}/{rel}",
            "source_sha256": source_hash,
            "sha256": sha256_file(out_path),
            "executable": is_exec,
        })

    skill_entry = {
        "id": canonical_id,
        "canonical_id": canonical_id,
        "name": canonical_id,
        "path": f"skills/{canonical_id}",
        "description": description,
        "category": category,
        "tags": TAGS,
        "risk": "safe",
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "source": f"https://github.com/{UPSTREAM_REPO_SLUG}/tree/{UPSTREAM_REV}/data/skills/{canonical_id}",
        "source_repo": UPSTREAM_REPO_SLUG,
        "source_revision": UPSTREAM_REV,
        "source_path": f"data/skills/{canonical_id}/SKILL.md",
        "license": LICENSE_NAME,
        "license_source": LICENSE_URL,
    }

    # 4. Write data/n8n-mcp-import.json
    import_manifest = {
        "source_repo": UPSTREAM_REPO_SLUG,
        "source_url": f"https://github.com/{UPSTREAM_REPO_SLUG}",
        "revision": UPSTREAM_REV,
        "author": AUTHOR,
        "author_url": AUTHOR_URL,
        "license": LICENSE_NAME,
        "license_source": LICENSE_URL,
        "skill_count": 1,
        "skipped": [
            {
                "id": sid,
                "source_path": f"data/skills/{sid}",
                "reason": "already_exists_in_catalog",
            }
            for sid in SKIPPED_SKILLS
        ],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 3872,
            "upstream_is_fork": False,
            "skipped_existing_count": len(SKIPPED_SKILLS),
            "collision_rationale": (
                "14 of the 15 upstream skills in data/skills/* already exist in the VAS catalog "
                "(n8n-agents, n8n-binary-and-data, n8n-code-javascript, n8n-code-python, n8n-code-tool, "
                "n8n-error-handling, n8n-expression-syntax, n8n-mcp-tools-expert, n8n-multi-instance, "
                "n8n-node-configuration, n8n-subworkflows, n8n-validation-expert, n8n-workflow-patterns, "
                "using-n8n-mcp-skills) and were skipped without modification. "
                "`n8n-self-hosting` has zero canonical ID or content shingle overlap with existing catalog skills."
            ),
        },
        "adaptations": [
            "Added standardized VAS YAML frontmatter fields (category, tags, risk, author, license, source_repo, source_revision, source_path) to SKILL.md.",
            "Preserved all 6 reference markdown guides (README.md, SINGLE_MODE.md, QUEUE_MODE.md, SECURITY.md, CREDENTIAL_OVERWRITES.md, DAY2.md) and all 6 production Docker/Caddy/Postgres assets in assets/.",
            "Added LICENSE and NOTICE.md to skills/n8n-self-hosting/ and appended VAS installation notes to SKILL.md.",
            "Set executable bit (0755) on assets/init-data.sh so the Postgres entrypoint script is ready when mounted.",
        ],
        "skills": [skill_entry],
        "files": file_records,
    }
    manifest_file = staging_root / "data" / "n8n-mcp-import.json"
    manifest_file.write_text(
        json.dumps(import_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # 5. Update data/source-credits.json
    credits_file = staging_root / "data" / "source-credits.json"
    credits_data = json.loads((REPO_ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
    credits_data["sections"]["n8nmcp"] = [
        f"- **n8n Self-Hosting (`n8n-self-hosting`)**: 1 production self-hosting runbook with Docker Compose templates (single-mode and Redis/Postgres queue-mode), Caddy auto-TLS, credential overwrites, security hardening, and Day-2 operations from [`{UPSTREAM_REPO_SLUG}`](https://github.com/{UPSTREAM_REPO_SLUG}) at `{UPSTREAM_REV}`, authored by [{AUTHOR}]({AUTHOR_URL}), licensed under [MIT]({LICENSE_URL}). (14 existing n8n workflow skills in the upstream repository were skipped as already present in the catalog.)"
    ]
    credits_file.write_text(
        json.dumps(credits_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # 6. Update data/catalog.json
    catalog_file = staging_root / "data" / "catalog.json"
    catalog_data = json.loads((REPO_ROOT / "data/catalog.json").read_text(encoding="utf-8"))
    existing = [
        s
        for s in catalog_data.get("skills", [])
        if s.get("source_repo") != UPSTREAM_REPO_SLUG and s.get("id") != canonical_id
    ]
    existing.append(skill_entry)
    existing.sort(key=lambda x: x["id"])
    catalog_data["skills"] = existing
    catalog_data["total"] = len(existing)
    catalog_file.write_text(
        json.dumps(catalog_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return len(file_records), len(existing)


def validate_import(staging_root):
    manifest = json.loads((staging_root / "data/n8n-mcp-import.json").read_text(encoding="utf-8"))
    expected = {f"skills/n8n-self-hosting/{name}" for name in (*UPSTREAM_FILES, "LICENSE", "NOTICE.md")}
    records = manifest["files"]
    if len(records) != len(expected) or {record["path"] for record in records} != expected:
        raise ValueError("Incomplete n8n import inventory")
    for record in records:
        path = staging_root / record["path"]
        if path.is_symlink() or not path.is_file() or sha256_file(path) != record["sha256"]:
            raise ValueError(f"Invalid staged import file: {record['path']}")


def publish_import(staging_root):
    for relative in IMPORT_PATHS:
        destination = REPO_ROOT / relative
        staged = staging_root / relative
        compatible = destination.is_dir() if staged.is_dir() else destination.is_file()
        if (destination.is_symlink() or destination.parent.is_symlink()
                or (destination.exists() and not compatible)):
            raise ValueError(f"Refusing incompatible import destination: {destination}")
    replacements = []
    try:
        for relative in IMPORT_PATHS:
            staged = staging_root / relative
            destination = REPO_ROOT / relative
            backup = staging_root / "backup" / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            replacements.append((staged, destination, backup))
            if destination.exists():
                destination.rename(backup)
            staged.rename(destination)
    except BaseException:
        for staged, destination, backup in reversed(replacements):
            if not staged.exists() and destination.exists():
                destination.rename(staged)
            if backup.exists():
                backup.rename(destination)
        raise


def main():
    staging_root = Path(tempfile.mkdtemp(prefix=".n8n-import-", dir=REPO_ROOT))
    keep_backup = False
    try:
        file_count, catalog_count = stage_import(staging_root)
        validate_import(staging_root)
        publish_import(staging_root)
    except BaseException:
        keep_backup = any((staging_root / "backup" / path).exists() for path in IMPORT_PATHS)
        if keep_backup:
            print(f"Import recovery needs attention; backups retained at {staging_root}", file=sys.stderr)
        raise
    finally:
        if not keep_backup:
            shutil.rmtree(staging_root)
    print(f"Wrote {REPO_ROOT / 'data/n8n-mcp-import.json'} with {file_count} file records.")
    print("Updated data/source-credits.json")
    print(f"Updated data/catalog.json (total: {catalog_count})")


if __name__ == "__main__":
    main()
