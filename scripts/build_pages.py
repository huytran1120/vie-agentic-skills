#!/usr/bin/env python3
"""Stage a complete static site with content-versioned CSS and script URLs."""

from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "huytran1120/vie-agentic-skills"
EXCLUDED = {"__pycache__", ".DS_Store"}


def relative_path(value):
    if (not isinstance(value, str) or not value
            or "\\" in value or any(ord(char) < 32 or ord(char) == 127 for char in value)
            or any(part in ("", ".", "..") for part in value.split("/"))
            or PurePosixPath(value).is_absolute() or re.match(r"^[A-Za-z]:", value)):
        raise ValueError(f"Invalid installation path: {value!r}")
    return PurePosixPath(value)


def snapshot(root, revision):
    if revision is not None:
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("An installation snapshot requires a full commit SHA")
        return revision, True
    revision = subprocess.check_output(
        ["git", "rev-parse", "--verify", "HEAD"], cwd=root, text=True,
    ).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Cannot identify the catalog publication commit")
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "-z", revision, "--", "skills", "skills_index.json"],
        cwd=root,
    )
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "-z", "--", "skills"],
        cwd=root,
    )
    unpublished = any(
        not EXCLUDED.intersection(PurePosixPath(path.decode()).parts)
        for path in (changed + untracked).split(b"\0") if path
    )
    return revision, not unpublished


def installation_manifests(root, revision=None):
    revision, available = snapshot(root, revision)
    index = json.loads((root / "skills_index.json").read_text())
    if not isinstance(index, list) or not index:
        raise ValueError("Installation manifests require a nonempty canonical catalog")
    manifests, source_paths = {}, set()
    for skill in index:
        if not isinstance(skill, dict) or not {"id", "path"} <= skill.keys():
            raise ValueError("Invalid canonical installation entry")
        skill_id = str(relative_path(skill["id"]))
        source = relative_path(skill["path"])
        if source.parts[0] != "skills" or len(source.parts) < 2:
            raise ValueError(f"Skill source must be inside skills/: {source}")
        directory = root.joinpath(*source.parts)
        if not (directory / "SKILL.md").is_file():
            raise ValueError(f"Missing skill runbook: {source}")
        if skill_id in manifests or str(source) in source_paths:
            raise ValueError(f"Duplicate installation identity or source: {skill_id}")
        source_paths.add(str(source))
        files = []
        for path in sorted(directory.rglob("*")):
            relative = path.relative_to(directory)
            if EXCLUDED.intersection(relative.parts):
                continue
            relative_path(relative.as_posix())
            if path.is_symlink():
                raise ValueError(f"Installation sources must not contain symlinks: {path}")
            if path.is_dir():
                continue
            if not path.is_file():
                raise ValueError(f"Unsupported installation file: {path}")
            record = {
                "path": relative.as_posix(), "bytes": path.stat().st_size,
                "sha256": sha256(path.read_bytes()).hexdigest(),
                "executable": bool(path.stat().st_mode & 0o111),
            }
            if available:
                record["url"] = (
                    f"https://raw.githubusercontent.com/{REPOSITORY}/{revision}/"
                    + quote(path.relative_to(root).as_posix(), safe="/")
                )
            files.append(record)
        entry = {
            "mode": "copy", "target_name": directory.name,
            "category": skill.get("category", "general"),
            "source": f"https://github.com/{REPOSITORY}/tree/{revision}/{quote(str(source), safe='/')}",
            "catalog_revision": revision,
        }
        manifest = {
            "schema_version": 1, "available": available,
            "skill_id": skill_id, "source_path": str(source),
            "target_name": directory.name, "repository": REPOSITORY, "revision": revision,
            "provenance": {key: skill[key] for key in
                           ("category", "license", "author", "source", "source_repo") if key in skill},
            "files": files,
            "receipt": {"filename": ".vas-manifest.json", "key": skill_id,
                        "installed_at_unit": "unix_seconds", "entry": entry},
        }
        if not available:
            manifest["unavailable_reason"] = "unpublished_local_changes"
        manifests[skill_id] = manifest
    destinations = {f"{skill_id}.json".casefold() for skill_id in manifests}
    if len(destinations) != len(manifests) or any(
        str(parent) in destinations
        for destination in destinations for parent in PurePosixPath(destination).parents
    ):
        raise ValueError("Conflicting installation manifest paths")
    return manifests


def build(root=ROOT, revision=None):
    output = root / "_site"
    sources = (root / "docs", root / "skills")
    for source in sources:
        if source.is_symlink():
            raise ValueError(f"Pages sources must not contain symlinks: {source}")
        for path in source.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Pages sources must not contain symlinks: {path}")
    manifests = installation_manifests(root, revision)
    html = (root / "docs/index.html").read_text()
    if html.count('data-skill-base=".."') != 1:
        raise ValueError("Missing or ambiguous local skill-root marker")
    html = html.replace('data-skill-base=".."', 'data-skill-base="."')
    documents = ("README.md", "README_EN.md", "CATALOG.md", "LICENSE")
    for name in documents:
        html = html.replace(f'href="../{name}"', f'href="./{name}"')
    for asset in sorted((root / "docs").iterdir()):
        if asset.suffix not in (".css", ".js") or not asset.is_file():
            continue
        attribute = "href" if asset.suffix == ".css" else "src"
        version = sha256(asset.read_bytes()).hexdigest()[:12]
        for prefix in ("", "./"):
            html = html.replace(
                f'{attribute}="{prefix}{asset.name}"',
                f'{attribute}="{prefix}{asset.name}?v={version}"',
            )
    if output.is_symlink():
        raise ValueError(f"Refusing to replace a symlink: {output}")
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(root / "docs", output)
    shutil.copytree(
        root / "skills", output / "skills",
        ignore=shutil.ignore_patterns(*EXCLUDED),
    )
    for name in documents:
        shutil.copy2(root / name, output / name)
    (output / "index.html").write_text(html)
    for skill_id, manifest in manifests.items():
        destination = output / "install-manifests" / f"{skill_id}.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    (output / ".nojekyll").touch()
    return output


if __name__ == "__main__":
    print(f"GitHub Pages artifact: {build()}")
