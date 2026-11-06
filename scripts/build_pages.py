#!/usr/bin/env python3
"""Stage the Vercel website with content-versioned CSS and script URLs."""

from hashlib import sha256
from html import escape
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "huytran1120/vie-agentic-skills"
EXCLUDED = {"__pycache__", ".DS_Store"}
PAGES_LIMIT_BYTES = 1_000_000_000


def web_analytics_snippet(root):
    """Use Vercel's client routes without adding tracking to local previews."""
    if os.environ.get("VERCEL") != "1":
        return ""
    config = json.loads(os.environ.get("VERCEL_OBSERVABILITY_CLIENT_CONFIG") or "{}")
    analytics = config.get("analytics", {}) if isinstance(config, dict) else None
    if not isinstance(analytics, dict):
        raise ValueError("Invalid Vercel Web Analytics client configuration")
    attributes = {"src": analytics.get("scriptSrc") or "/_vercel/insights/script.js"}
    for key, attribute in (("viewEndpoint", "data-view-endpoint"),
                           ("eventEndpoint", "data-event-endpoint"),
                           ("sessionEndpoint", "data-session-endpoint")):
        if analytics.get(key):
            attributes[attribute] = analytics[key]
    for key, value in attributes.items():
        if (not isinstance(value, str) or value.startswith("//")
                or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in value)
                or any(char in value for char in '\\"\'<>')):
            raise ValueError(f"Invalid Vercel Web Analytics route: {key}")
        url = urlsplit(value)
        if url.scheme:
            if url.scheme not in ("http", "https") or not url.netloc or url.username or url.password:
                raise ValueError(f"Invalid Vercel Web Analytics URL: {key}")
        else:
            # Match the official SDK's makeAbsolute(): Vercel may provide paths
            # without a leading slash, as well as fully qualified intake URLs.
            attributes[key] = value if value.startswith("/") else "/" + value
    version = sha256((root / "docs/analytics.js").read_bytes()).hexdigest()[:12]
    routes = " ".join(f'{key}="{escape(value, quote=True)}"' for key, value in attributes.items())
    return (f'<script id="vas-analytics-bootstrap" defer src="/analytics.js?v={version}"></script>\n'
            f'<script id="vas-web-analytics" defer {routes}></script>')


def inject_web_analytics(source, snippet):
    if not snippet:
        return source
    if 'id="vas-web-analytics"' in source or 'id="vas-analytics-bootstrap"' in source:
        raise ValueError("Web Analytics must be injected once by the Vercel build")
    if len(re.findall(r"</head\s*>", source, flags=re.I)) != 1:
        raise ValueError("Web Analytics requires one closing head element")
    return re.sub(r"</head\s*>", lambda match: snippet + "\n" + match.group(0), source, count=1, flags=re.I)


def load_size_budget(root, target="vercel"):
    if target not in ("vercel", "pages"):
        raise ValueError(f"Unknown publication target: {target}")
    filename = f"{target}-budget.json"
    budget = json.loads((root / filename).read_text())
    if (not isinstance(budget, dict)
            or set(budget) != {"warning_bytes", "max_bytes"}
            or any(type(budget[key]) is not int for key in budget)
            or not 0 < budget["warning_bytes"] < budget["max_bytes"]):
        raise ValueError(f"Invalid {filename}: require integer bytes with "
                         "0 < warning_bytes < max_bytes")
    # The retained legacy configuration is never used by the Vercel build.
    if target == "pages" and budget["max_bytes"] >= PAGES_LIMIT_BYTES:
        raise ValueError("Invalid pages-budget.json: require max_bytes < 1,000,000,000")
    return budget


def enforce_size_budget(output, budget, report=False):
    total, directories = 0, {}
    for path in output.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Vercel artifact must not contain symlinks: {path}")
        if not path.is_file():
            continue
        size = path.stat().st_size
        total += size
        parts = path.relative_to(output).parts
        if parts[0] == "skills" and len(parts) > 2:
            directory = "/".join(parts[:2])
        else:
            directory = parts[0] if len(parts) > 1 else "(root files)"
        directories[directory] = directories.get(directory, 0) + size
    largest = sorted(directories.items(), key=lambda item: (-item[1], item[0]))[:5]
    details = (f"Vercel size: {total:,} bytes ({total / 1_000_000:.1f} MB; "
               f"{total / 2**20:.1f} MiB)\n"
               f"Warning: {budget['warning_bytes']:,} bytes; "
               f"limit: {budget['max_bytes']:,} bytes\n"
               "Largest directories:\n" + "\n".join(
                   f"  {name}: {size:,} bytes ({size / 1_000_000:.1f} MB)"
                   for name, size in largest))
    if total > budget["max_bytes"]:
        raise ValueError(f"Vercel size budget exceeded by {total - budget['max_bytes']:,} bytes.\n"
                         f"{details}\nReduce the publication payload before deploying.")
    if report or total >= budget["warning_bytes"]:
        print(details)
    if total >= budget["warning_bytes"]:
        prefix = "::warning::" if os.environ.get("GITHUB_ACTIONS") == "true" else "WARNING: "
        print(f"{prefix}Vercel is approaching its size budget: "
              f"{total:,} / {budget['max_bytes']:,} bytes.")
    return total


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


def build(root=ROOT, revision=None, report=False):
    budget = load_size_budget(root)
    analytics = web_analytics_snippet(root)
    output = root / "_site"
    sources = (root / "docs", root / "skills")
    for source in sources:
        if source.is_symlink():
            raise ValueError(f"Website sources must not contain symlinks: {source}")
        for path in source.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Website sources must not contain symlinks: {path}")
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
    (output / "index.html").write_text(inject_web_analytics(html, analytics))
    # Static guides share catalog assets; version them just like the homepage.
    for page in (output / "blog").rglob("*.html"):
        def version_guide_asset(match):
            value = match.group(2)
            if re.match(r"^[a-zA-Z][\w+.-]*:|^//", value):
                return match.group(0)
            asset = (page.parent / value).resolve()
            if not asset.is_relative_to(output.resolve()) or not asset.is_file():
                raise ValueError(f"Missing or invalid guide asset: {page}: {value}")
            version = sha256(asset.read_bytes()).hexdigest()[:12]
            return f'{match.group(1)}="{value}?v={version}"'
        source = re.sub(r'(<span data-catalog-count="(vi|en)">)[^<]*(</span>)',
                        lambda match: match.group(1) +
                        (f"{len(manifests):,}".replace(",", ".") if match.group(2) == "vi"
                         else f"{len(manifests):,}") + match.group(3), page.read_text())
        source = re.sub(r'(href|src)="([^"?#]+\.(?:css|js))"', version_guide_asset, source)
        page.write_text(inject_web_analytics(source, analytics))

    for skill_id, manifest in manifests.items():
        destination = output / "install-manifests" / f"{skill_id}.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    (output / ".nojekyll").touch()
    enforce_size_budget(output, budget, report=report)
    return output


if __name__ == "__main__":
    try:
        print(f"Vercel artifact: {build(report=True)}")
    except ValueError as error:
        raise SystemExit(str(error))
