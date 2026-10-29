#!/usr/bin/env python3
"""Stage a complete static site with content-versioned CSS and script URLs."""

from hashlib import sha256
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]


def build(root=ROOT):
    output = root / "_site"
    sources = (root / "docs", root / "skills")
    for source in sources:
        for path in source.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Pages sources must not contain symlinks: {path}")
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
        ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"),
    )
    for name in documents:
        shutil.copy2(root / name, output / name)
    (output / "index.html").write_text(html)
    (output / ".nojekyll").touch()
    return output


if __name__ == "__main__":
    print(f"GitHub Pages artifact: {build()}")
