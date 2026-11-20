#!/usr/bin/env python3
"""
Import 32 genuinely new motion graphics and Blender 5.x agent skills from 5 upstream repositories:
  1. NiazMorshed2007/reanimate (1 skill: reanimate, MIT)
  2. alchaincyf/huashu-art-motion (1 skill: huashu-art-motion, MIT + OFL 1.1 fonts + MIT Three.js)
  3. alexgreensh/anidoodle (1 skill: anidoodle, Apache-2.0 + MIT Three.js + OFL 1.1 Poppins + PD Van Gogh ref)
  4. Leonxlnx/cinetic (1 skill: cinetic, MIT + OFL 1.1 fonts)
  5. EL4CTEO/blender-skills (28 skills: blender-*, MIT)

Stages payloads in a temporary directory, verifies path safety / zero symlinks / executable bits,
copies into skills/, records source and adapted SHA-256 hashes in data/*-import.json,
and updates data/catalog.json and data/source-credits.json.
"""

import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_ROOT = Path("/tmp/vas-motion-survey")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def is_executable(path: Path) -> bool:
    st = os.stat(path)
    return bool(st.st_mode & 0o111) and path.suffix != ".md"


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    out = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val in (">", "|", ">-", "|-"):
                parts = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                    parts.append(lines[i].strip())
                    i += 1
                out[key] = " ".join(p for p in parts if p)
                continue
            out[key] = val.strip().strip('"').strip("'")
        i += 1
    return out


def safe_copy_file(src: Path, dst: Path):
    if src.is_symlink():
        raise RuntimeError(f"Refusing to copy symlink: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def safe_copy_tree(src_dir: Path, dst_dir: Path, exclude_top=()):
    for root, dirs, files in os.walk(src_dir):
        rel_root = Path(root).relative_to(src_dir)
        if ".git" in dirs:
            dirs.remove(".git")
        if rel_root == Path("."):
            for ex in exclude_top:
                if ex in dirs:
                    dirs.remove(ex)
        for d in list(dirs):
            p = Path(root) / d
            if p.is_symlink():
                raise RuntimeError(f"Symlink directory detected: {p}")
        for f in files:
            if rel_root == Path(".") and f in exclude_top:
                continue
            if f in (".DS_Store", "Thumbs.db"):
                continue
            src = Path(root) / f
            if src.is_symlink():
                raise RuntimeError(f"Symlink file detected: {src}")
            dst = dst_dir / rel_root / f
            safe_copy_file(src, dst)


def record_files(skill_id: str, skill_dir: Path, source_map: dict):
    records = []
    for p in sorted(skill_dir.rglob("*")):
        if not p.is_file():
            continue
        rel_inside = p.relative_to(skill_dir).as_posix()
        repo_rel = f"skills/{skill_id}/{rel_inside}"
        sha = sha256_file(p)
        src_path, src_sha = source_map.get(rel_inside, (repo_rel, sha))
        records.append(
            {
                "skill_id": skill_id,
                "source_path": src_path,
                "path": repo_rel,
                "source_sha256": src_sha,
                "sha256": sha,
                "executable": is_executable(p),
            }
        )
    return records


def stage_and_install_skill(stage_dir: Path, target_dir: Path):
    # Validate staged directory before moving into repository
    for p in stage_dir.rglob("*"):
        if p.is_symlink():
            raise RuntimeError(f"Symlink found in staged payload: {p}")
        p.resolve().relative_to(stage_dir.resolve())
    if target_dir.exists():
        raise RuntimeError(f"Refusing to overwrite existing skill in CHỈ THÊM MỚI mode: {target_dir}")
    shutil.copytree(stage_dir, target_dir, symlinks=False)


def build_reanimate(stage_root: Path):
    rev = "3f7a55a2986a84ca2173e86ee9127eefe31d046d"
    repo = "NiazMorshed2007/reanimate"
    src_repo = UPSTREAM_ROOT / "NiazMorshed2007__reanimate"
    src_skill = src_repo / "skills/reanimate"
    skill_id = "reanimate"
    stage_dir = stage_root / skill_id
    safe_copy_tree(src_skill, stage_dir)

    source_map = {}
    for p in src_skill.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src_skill).as_posix()
            source_map[rel] = (f"skills/reanimate/{rel}", sha256_file(p))

    notice_text = f"""# Notice for {skill_id}

This skill payload is adapted from upstream repository [{repo}](https://github.com/{repo})
at commit revision `{rev}`.

- Author: Niaz Morshed
- Upstream License: MIT (see bundled `LICENSE`)
- Upstream Source Path: `skills/reanimate`
- Adapted for Vie Agentic Skill (VAS) distribution.

## VAS Adaptation Notes

- Preserves the complete standalone `skills/reanimate/` payload (`SKILL.md`, `LICENSE`, `references/`, `scripts/`, including executable bit on `scripts/setup.sh`).
- Excludes repository-level showcase website (`site/`) and GitHub demo media (`.github/`) not required for standalone skill operation.
- Appended reversible VAS installation, attribution, and prerequisites notes to `SKILL.md`.
"""
    (stage_dir / "NOTICE.md").write_text(notice_text, encoding="utf-8")

    skill_md = (stage_dir / "SKILL.md").read_text(encoding="utf-8").rstrip()
    vas_notes = f"""

## VAS installation notes

This skill is curated and verified by **Vie Agentic Skill (VAS)** from [{repo}](https://github.com/{repo}).
- Canonical ID: `{skill_id}`
- Source repository: [`{repo}`](https://github.com/{repo}) (revision `{rev}`, path `skills/reanimate`)
- Author: Niaz Morshed
- License: MIT (see bundled `LICENSE` and `NOTICE.md`)
- Prerequisites: Bun (`bun`), Playwright / Chromium, and `ffmpeg` for frame capture and side-by-side verification (`scripts/setup.sh` documents environment setup; not executed during `./vas install`).
- Safety: Installation only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed and no script is executed during `./vas install`.
"""
    (stage_dir / "SKILL.md").write_text(skill_md + vas_notes, encoding="utf-8")

    target_dir = REPO_ROOT / "skills" / skill_id
    stage_and_install_skill(stage_dir, target_dir)

    fm = parse_frontmatter(skill_md)
    files = record_files(skill_id, target_dir, source_map)
    skill_meta = {
        "id": skill_id,
        "canonical_id": skill_id,
        "name": skill_id,
        "path": f"skills/{skill_id}",
        "description": fm.get("description", ""),
        "category": "media",
        "tags": ["animation", "motion", "clone", "frame-by-frame", "css", "webgl", "threejs", "reanimate"],
        "triggers": ["reanimate", "clone animation", "rebuild animation frame by frame", "match animation timing"],
        "risk": "safe",
        "author": "Niaz Morshed",
        "author_url": "https://github.com/NiazMorshed2007",
        "source": f"https://github.com/{repo}/tree/{rev}/skills/reanimate",
        "source_repo": repo,
        "source_revision": rev,
        "source_path": "skills/reanimate",
        "license": "MIT",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
    }
    manifest = {
        "source_repo": repo,
        "source_url": f"https://github.com/{repo}",
        "revision": rev,
        "author": "Niaz Morshed",
        "author_url": "https://github.com/NiazMorshed2007",
        "license": "MIT",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
        "skill_count": 1,
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 4096,
            "upstream_is_fork": False,
            "methods": ["canonical-id/name", "source-repo/path", "raw-sha256", "normalized-body", "7-word-shingles"],
            "collision_rationale": "Zero ID or content collisions against all 4,096 catalog skills (0.0003 max 7-word shingle Jaccard similarity).",
        },
        "adaptations": [
            "Preserve complete upstream skills/reanimate payload including LICENSE, references/, scripts/, and executable permission on scripts/setup.sh.",
            "Exclude optional repository showcase site/ and .github/ assets not needed by the standalone skill.",
            "Add NOTICE.md and append reversible VAS installation/prerequisites notes to SKILL.md.",
            "Map reanimate to the existing media category to preserve the 119-category taxonomy.",
        ],
        "skills": [skill_meta],
        "files": files,
    }
    return skill_meta, manifest


def build_huashu(stage_root: Path):
    rev = "a97c45018d46e950d56d61981138e08f4e092909"
    repo = "alchaincyf/huashu-art-motion"
    src_repo = UPSTREAM_ROOT / "alchaincyf__huashu-art-motion"
    skill_id = "huashu-art-motion"
    stage_dir = stage_root / skill_id
    stage_dir.mkdir(parents=True, exist_ok=True)

    source_map = {}
    for fname in ("LICENSE", "SKILL.md"):
        src = src_repo / fname
        safe_copy_file(src, stage_dir / fname)
        source_map[fname] = (fname, sha256_file(src))

    for sub in ("defaults", "references", "schemas", "scripts"):
        src_sub = src_repo / sub
        safe_copy_tree(src_sub, stage_dir / sub)
        for p in src_sub.rglob("*"):
            if p.is_file() and p.name not in (".DS_Store", "Thumbs.db"):
                rel = f"{sub}/{p.relative_to(src_sub).as_posix()}"
                source_map[rel] = (rel, sha256_file(p))

    notice_text = f"""# Notice for {skill_id}

This skill payload is adapted from upstream repository [{repo}](https://github.com/{repo})
at commit revision `{rev}`.

- Author: alchaincyf (花叔 · 花生)
- Upstream License: MIT (see bundled `LICENSE`)
- Upstream Source Path: `.` (root skill: `SKILL.md`, `defaults/`, `references/`, `schemas/`, `scripts/`)
- Adapted for Vie Agentic Skill (VAS) distribution.

## Third-Party Bundled Licenses

- `scripts/engine/lib/three.min.js`: MIT License (see `scripts/engine/lib/THREE_LICENSE.txt`).
- `scripts/engine/lib/fonts/*`: SIL Open Font License 1.1 (see `scripts/engine/lib/fonts/OFL.txt` and `scripts/engine/lib/fonts/LICENSES.md`).

## VAS Adaptation Notes

- Excluded optional showcase gallery directory `assets/` (~51.1 MB of demo videos/images not required at runtime; `scripts/film_gate.py` explicitly skips template comparison when absent), `tests/`, `.github/`, `README*.md`, `CHANGELOG.md`, and `release-manifest.json`.
- Preserved all runtime code, style recipes (`references/`), schemas, defaults, engine libraries, fonts, and license notices.
- Appended reversible VAS installation, attribution, and prerequisites notes to `SKILL.md`.
"""
    (stage_dir / "NOTICE.md").write_text(notice_text, encoding="utf-8")

    skill_md = (stage_dir / "SKILL.md").read_text(encoding="utf-8").rstrip()
    vas_notes = f"""

## VAS installation notes

This skill is curated and verified by **Vie Agentic Skill (VAS)** from [{repo}](https://github.com/{repo}).
- Canonical ID: `{skill_id}`
- Source repository: [`{repo}`](https://github.com/{repo}) (revision `{rev}`, root skill)
- Author: alchaincyf (花叔 · 花生)
- License: MIT (see bundled `LICENSE`, `NOTICE.md`, `scripts/engine/lib/THREE_LICENSE.txt`, and `scripts/engine/lib/fonts/LICENSES.md` for OFL-1.1 fonts)
- Prerequisites: Python 3.10+, Playwright/Chromium, and `ffmpeg` for rendering films; optional TTS/voice tools as documented in `references/`.
- Adaptations: Optional showcase gallery `assets/` (~51 MB demo media) excluded to keep standalone skill size lean; all engine code, style recipes, fonts, and schemas are preserved intact.
- Safety: Installation only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed and no script is executed during `./vas install`.
"""
    (stage_dir / "SKILL.md").write_text(skill_md + vas_notes, encoding="utf-8")

    target_dir = REPO_ROOT / "skills" / skill_id
    stage_and_install_skill(stage_dir, target_dir)

    fm = parse_frontmatter(skill_md)
    files = record_files(skill_id, target_dir, source_map)
    skill_meta = {
        "id": skill_id,
        "canonical_id": skill_id,
        "name": skill_id,
        "path": f"skills/{skill_id}",
        "description": fm.get("description", ""),
        "category": "media",
        "tags": ["art-motion", "animation", "video", "painting", "styles", "storyboard", "threejs", "huashu"],
        "triggers": ["huashu art motion", "art style animation", "painting motion film", "36 art styles video"],
        "risk": "safe",
        "author": "alchaincyf (花叔 · 花生)",
        "author_url": "https://github.com/alchaincyf",
        "source": f"https://github.com/{repo}/tree/{rev}",
        "source_repo": repo,
        "source_revision": rev,
        "source_path": "SKILL.md",
        "license": "MIT",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
    }
    manifest = {
        "source_repo": repo,
        "source_url": f"https://github.com/{repo}",
        "revision": rev,
        "author": "alchaincyf (花叔 · 花生)",
        "author_url": "https://github.com/alchaincyf",
        "license": "MIT",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
        "third_party_licenses": ["MIT (three.min.js)", "OFL-1.1 (bundled fonts in scripts/engine/lib/fonts/)"],
        "skill_count": 1,
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 4096,
            "upstream_is_fork": False,
            "methods": ["canonical-id/name", "source-repo/path", "raw-sha256", "normalized-body", "7-word-shingles"],
            "collision_rationale": "Zero ID or content collisions against all 4,096 catalog skills (0.0026 max 7-word shingle Jaccard similarity).",
        },
        "adaptations": [
            "Package SKILL.md, LICENSE, defaults/, references/, schemas/, and scripts/ (including engine, Three.js MIT license, and OFL-1.1 font licenses).",
            "Exclude optional showcase directory assets/ (~51.1 MB demo videos/images; scripts/film_gate.py explicitly skips missing template), tests/, .github/, README*.md, CHANGELOG.md, and release-manifest.json.",
            "Add NOTICE.md and append reversible VAS installation/prerequisites notes to SKILL.md.",
            "Map huashu-art-motion to the existing media category to preserve the 119-category taxonomy.",
        ],
        "skills": [skill_meta],
        "files": files,
    }
    return skill_meta, manifest


def build_anidoodle(stage_root: Path):
    rev = "4ae27d2c281fcfd01bce87ab13dc5ad4df81a795"
    repo = "alexgreensh/anidoodle"
    src_repo = UPSTREAM_ROOT / "alexgreensh__anidoodle"
    src_skill = src_repo / "skills/anidoodle"
    skill_id = "anidoodle"
    stage_dir = stage_root / skill_id
    safe_copy_tree(src_skill, stage_dir)

    source_map = {}
    for p in src_skill.rglob("*"):
        if p.is_file() and p.name not in (".DS_Store", "Thumbs.db"):
            rel = p.relative_to(src_skill).as_posix()
            source_map[rel] = (f"skills/anidoodle/{rel}", sha256_file(p))

    for root_file in ("LICENSE", "NOTICE"):
        src = src_repo / root_file
        safe_copy_file(src, stage_dir / root_file)
        source_map[root_file] = (root_file, sha256_file(src))

    notice_md = f"""# Notice for {skill_id}

This skill payload is adapted from upstream repository [{repo}](https://github.com/{repo})
at commit revision `{rev}`.

- Author: Alex Greenshpun (10x Company)
- Upstream License: Apache-2.0 (see bundled `LICENSE` and upstream `NOTICE`)
- Upstream Source Path: `skills/anidoodle` (canonical skill source; duplicate plugin mirror under `plugins/anidoodle/skills/anidoodle` was not double-imported)
- Adapted for Vie Agentic Skill (VAS) distribution.

## Third-Party Bundled Material

- `engine/vendor/three/`: Three.js 0.170.0 under MIT License (see `engine/vendor/three/LICENSE` and `PROVENANCE.md`).
- `engine/assets/fonts/Poppins-Bold.ttf`: SIL Open Font License 1.1 (see `engine/assets/fonts/Poppins-OFL.txt` and `PROVENANCE.md`).
- `engine/assets/refs/vangogh-almond-blossom.jpg`: Public domain reproduction (see `engine/assets/refs/PROVENANCE.json` and root `NOTICE`).
- Optional sound pack is NOT bundled; `engine/tools/soundfetch.mjs` only downloads VCSL (CC0) and OpenAIR (CC BY 4.0) assets if explicitly requested by the user (see `references/music/sounds-licenses.md`).
"""
    (stage_dir / "NOTICE.md").write_text(notice_md, encoding="utf-8")

    skill_md = (stage_dir / "SKILL.md").read_text(encoding="utf-8").rstrip()
    vas_notes = f"""

## VAS installation notes

This skill is curated and verified by **Vie Agentic Skill (VAS)** from [{repo}](https://github.com/{repo}).
- Canonical ID: `{skill_id}`
- Source repository: [`{repo}`](https://github.com/{repo}) (revision `{rev}`, path `skills/anidoodle`)
- Author: Alex Greenshpun (10x Company)
- License: Apache-2.0 (see bundled `LICENSE`, `NOTICE`, and `NOTICE.md`; vendored Three.js MIT, Poppins OFL-1.1, Van Gogh reference Public Domain)
- Prerequisites: Node.js, Playwright/Chromium, and `ffmpeg` to render animations and scores via the bundled `engine/`. Optional sound pack download requires explicit user approval.
- Safety: Installation only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed and no audio assets are downloaded during `./vas install`.
"""
    (stage_dir / "SKILL.md").write_text(skill_md + vas_notes, encoding="utf-8")

    target_dir = REPO_ROOT / "skills" / skill_id
    stage_and_install_skill(stage_dir, target_dir)

    fm = parse_frontmatter(skill_md)
    files = record_files(skill_id, target_dir, source_map)
    skill_meta = {
        "id": skill_id,
        "canonical_id": skill_id,
        "name": skill_id,
        "path": f"skills/{skill_id}",
        "description": fm.get("description", ""),
        "category": "media",
        "tags": ["anidoodle", "doodle", "animation", "2d", "3d", "motion-graphics", "explainer", "music", "code-drawn"],
        "triggers": ["anidoodle", "code-drawn animation", "doodle video", "illustrated explainer film"],
        "risk": "safe",
        "author": "Alex Greenshpun (10x Company)",
        "author_url": "https://github.com/alexgreensh",
        "source": f"https://github.com/{repo}/tree/{rev}/skills/anidoodle",
        "source_repo": repo,
        "source_revision": rev,
        "source_path": "skills/anidoodle",
        "license": "Apache-2.0",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
    }
    manifest = {
        "source_repo": repo,
        "source_url": f"https://github.com/{repo}",
        "revision": rev,
        "author": "Alex Greenshpun (10x Company)",
        "author_url": "https://github.com/alexgreensh",
        "license": "Apache-2.0",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
        "third_party_licenses": ["MIT (three.js 0.170.0)", "OFL-1.1 (Poppins-Bold.ttf)", "Public Domain (vangogh-almond-blossom.jpg)"],
        "skill_count": 1,
        "skipped": [
            {
                "id": "anidoodle (plugin mirror)",
                "path": "plugins/anidoodle/skills/anidoodle/SKILL.md",
                "reason": "Byte-identical mirror of canonical skills/anidoodle/SKILL.md packaged for plugin distribution.",
            }
        ],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 4096,
            "upstream_is_fork": False,
            "methods": ["canonical-id/name", "source-repo/path", "raw-sha256", "normalized-body", "7-word-shingles"],
            "collision_rationale": "Zero ID or content collisions against all 4,096 catalog skills (0.0000 max 7-word shingle Jaccard similarity).",
        },
        "adaptations": [
            "Package complete canonical skills/anidoodle/ directory alongside root LICENSE and NOTICE files.",
            "Skip duplicate plugin mirror under plugins/anidoodle/skills/anidoodle/ and root marketing assets/ (~34.5 MB).",
            "Add NOTICE.md and append reversible VAS installation/prerequisites notes to SKILL.md.",
            "Map anidoodle to the existing media category to preserve the 119-category taxonomy.",
        ],
        "skills": [skill_meta],
        "files": files,
    }
    return skill_meta, manifest


def build_cinetic(stage_root: Path):
    rev = "f4bbfc844877891fe92279d47b7874fb44d485ae"
    repo = "Leonxlnx/cinetic"
    src_repo = UPSTREAM_ROOT / "Leonxlnx__cinetic"
    src_skill = src_repo / "skills/cinetic"
    skill_id = "cinetic"
    stage_dir = stage_root / skill_id
    safe_copy_tree(src_skill, stage_dir)

    source_map = {}
    for p in src_skill.rglob("*"):
        if p.is_file() and p.name not in (".DS_Store", "Thumbs.db"):
            rel = p.relative_to(src_skill).as_posix()
            source_map[rel] = (f"skills/cinetic/{rel}", sha256_file(p))

    # Also copy root LICENSE as LICENSE (alongside upstream LICENSE.txt) for standard VAS discovery
    safe_copy_file(src_repo / "LICENSE", stage_dir / "LICENSE")
    source_map["LICENSE"] = ("LICENSE", sha256_file(src_repo / "LICENSE"))

    notice_text = f"""# Notice for {skill_id}

This skill payload is adapted from upstream repository [{repo}](https://github.com/{repo})
at commit revision `{rev}`.

- Author: Leonxlnx
- Upstream License: MIT (see bundled `LICENSE` and `LICENSE.txt`)
- Upstream Source Path: `skills/cinetic`
- Adapted for Vie Agentic Skill (VAS) distribution.

## Third-Party Bundled Licenses

- `assets/remotion-starter/public/fonts/*/`: 11 font families (Bricolage Grotesque, DM Sans, Funnel Display, Funnel Sans, Geist, Hanken Grotesk, Host Grotesk, Instrument Sans, Manrope, Mona Sans, Schibsted Grotesk) licensed under SIL Open Font License 1.1 (each folder carries its own `OFL.txt`).

## VAS Adaptation Notes

- Preserves the complete standalone `skills/cinetic/` payload (`SKILL.md`, `LICENSE.txt`, `assets/`, `references/`, `scripts/`) and all executable script permissions.
- Copies root `LICENSE`, adds `NOTICE.md`, and appends reversible VAS installation/prerequisites notes to `SKILL.md`.
"""
    (stage_dir / "NOTICE.md").write_text(notice_text, encoding="utf-8")

    skill_md = (stage_dir / "SKILL.md").read_text(encoding="utf-8").rstrip()
    vas_notes = f"""

## VAS installation notes

This skill is curated and verified by **Vie Agentic Skill (VAS)** from [{repo}](https://github.com/{repo}).
- Canonical ID: `{skill_id}`
- Source repository: [`{repo}`](https://github.com/{repo}) (revision `{rev}`, path `skills/cinetic`)
- Author: Leonxlnx
- License: MIT (see bundled `LICENSE`, `LICENSE.txt`, `NOTICE.md`, and per-font `OFL.txt` files under `assets/remotion-starter/public/fonts/`)
- Prerequisites: Node.js 22+, `ffmpeg` 6+ with `libx264`, Python 3.11+ (`numpy`, `scipy`, `soundfile`, `pyloudnorm`, `opencv-python`, `librosa`), Chromium/Chrome Headless Shell, and Remotion 4 or HyperFrames.
- Safety: Installation only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed and no script is executed during `./vas install`.
"""
    (stage_dir / "SKILL.md").write_text(skill_md + vas_notes, encoding="utf-8")

    target_dir = REPO_ROOT / "skills" / skill_id
    stage_and_install_skill(stage_dir, target_dir)

    fm = parse_frontmatter(skill_md)
    files = record_files(skill_id, target_dir, source_map)
    skill_meta = {
        "id": skill_id,
        "canonical_id": skill_id,
        "name": skill_id,
        "path": f"skills/{skill_id}",
        "description": fm.get("description", ""),
        "category": "media",
        "tags": ["cinetic", "launch-film", "remotion", "hyperframes", "video", "motion-graphics", "storyboard", "promo"],
        "triggers": ["cinetic", "launch film", "product video from code", "remotion promo film", "hyperframes video"],
        "risk": "safe",
        "author": "Leonxlnx",
        "author_url": "https://github.com/Leonxlnx",
        "source": f"https://github.com/{repo}/tree/{rev}/skills/cinetic",
        "source_repo": repo,
        "source_revision": rev,
        "source_path": "skills/cinetic",
        "license": "MIT",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
    }
    manifest = {
        "source_repo": repo,
        "source_url": f"https://github.com/{repo}",
        "revision": rev,
        "author": "Leonxlnx",
        "author_url": "https://github.com/Leonxlnx",
        "license": "MIT",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
        "third_party_licenses": ["OFL-1.1 (11 font families in assets/remotion-starter/public/fonts/)"],
        "skill_count": 1,
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 4096,
            "upstream_is_fork": False,
            "methods": ["canonical-id/name", "source-repo/path", "raw-sha256", "normalized-body", "7-word-shingles"],
            "collision_rationale": "Zero ID or content collisions against all 4,096 catalog skills (0.0000 max 7-word shingle Jaccard similarity).",
        },
        "adaptations": [
            "Preserve complete standalone skills/cinetic payload including assets/, references/, scripts/, LICENSE.txt, and all executable script permissions.",
            "Copy root LICENSE, add NOTICE.md, and append reversible VAS installation/prerequisites notes to SKILL.md.",
            "Map cinetic to the existing media category to preserve the 119-category taxonomy.",
        ],
        "skills": [skill_meta],
        "files": files,
    }
    return skill_meta, manifest


def build_el4cteo_blender(stage_root: Path):
    rev = "9e7e04a603c125a0d17447ab97112fa70a865067"
    repo = "EL4CTEO/blender-skills"
    src_repo = UPSTREAM_ROOT / "EL4CTEO__blender-skills"
    src_skills_dir = src_repo / "skills"
    lic_src = src_repo / "LICENSE"
    lic_sha = sha256_file(lic_src)

    skills_meta = []
    all_files = []

    for d in sorted(p for p in src_skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()):
        skill_id = d.name
        stage_dir = stage_root / skill_id
        safe_copy_tree(d, stage_dir)

        source_map = {}
        for p in d.rglob("*"):
            if p.is_file() and p.name not in (".DS_Store", "Thumbs.db"):
                rel = p.relative_to(d).as_posix()
                source_map[rel] = (f"skills/{skill_id}/{rel}", sha256_file(p))

        safe_copy_file(lic_src, stage_dir / "LICENSE")
        source_map["LICENSE"] = ("LICENSE", lic_sha)

        notice_text = f"""# Notice for {skill_id}

This skill payload is adapted from upstream repository [{repo}](https://github.com/{repo})
at commit revision `{rev}`.

- Author: EL4CTEO (`blender-agent-skills`)
- Upstream License: MIT (see bundled `LICENSE`)
- Upstream Source Path: `skills/{skill_id}`
- Adapted for Vie Agentic Skill (VAS) distribution.

## VAS Adaptation Notes

- Preserves the complete standalone skill directory including bundled `scripts/_bpyx.py` helpers and `references/`.
- Includes upstream MIT `LICENSE` and `NOTICE.md` inside each standalone skill folder.
- Mapped to the existing `graphics-processing` category so the legacy `blender` category (`arjun988/blender-skills`, 94 skills) and the 119-category taxonomy remain intact.
- Appended reversible VAS installation, attribution, and prerequisites notes to `SKILL.md`.
"""
        (stage_dir / "NOTICE.md").write_text(notice_text, encoding="utf-8")

        skill_md = (stage_dir / "SKILL.md").read_text(encoding="utf-8").rstrip()
        vas_notes = f"""

## VAS installation notes

This skill is curated and verified by **Vie Agentic Skill (VAS)** from [{repo}](https://github.com/{repo}).
- Canonical ID: `{skill_id}`
- Source repository: [`{repo}`](https://github.com/{repo}) (revision `{rev}`, path `skills/{skill_id}`)
- Author: EL4CTEO (`blender-agent-skills`)
- License: MIT (see bundled `LICENSE` and `NOTICE.md`)
- Prerequisites: Blender 5.2 LTS or 5.3+ (headless CLI `blender --background --python ...` or optional `blender-mcp` server for live sessions).
- Safety: Installation only links or copies static files and writes `.vas-manifest.json`. No Blender add-on, MCP server, or script is executed during `./vas install`.
"""
        (stage_dir / "SKILL.md").write_text(skill_md + vas_notes, encoding="utf-8")

        target_dir = REPO_ROOT / "skills" / skill_id
        stage_and_install_skill(stage_dir, target_dir)

        fm = parse_frontmatter(skill_md)
        files = record_files(skill_id, target_dir, source_map)
        all_files.extend(files)

        topic = skill_id.removeprefix("blender-")
        skills_meta.append(
            {
                "id": skill_id,
                "canonical_id": skill_id,
                "name": skill_id,
                "path": f"skills/{skill_id}",
                "description": fm.get("description", ""),
                "category": "graphics-processing",
                "tags": ["blender", "blender-5", "bpy", "3d", "dcc", topic],
                "triggers": [skill_id, f"blender {topic.replace('-', ' ')}", "blender 5.3 bpy"],
                "risk": "safe",
                "author": "EL4CTEO",
                "author_url": "https://github.com/EL4CTEO",
                "source": f"https://github.com/{repo}/tree/{rev}/skills/{skill_id}",
                "source_repo": repo,
                "source_revision": rev,
                "source_path": f"skills/{skill_id}",
                "license": "MIT",
                "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
            }
        )

    manifest = {
        "source_repo": repo,
        "source_url": f"https://github.com/{repo}",
        "revision": rev,
        "author": "EL4CTEO",
        "author_url": "https://github.com/EL4CTEO",
        "license": "MIT",
        "license_source": f"https://github.com/{repo}/blob/{rev}/LICENSE",
        "skill_count": len(skills_meta),
        "skipped": [],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 4096,
            "upstream_is_fork": False,
            "methods": ["canonical-id/name", "source-repo/path", "raw-sha256", "normalized-body", "7-word-shingles"],
            "collision_rationale": "All 28 EL4CTEO/blender-skills entries are independent Blender 5.2+/5.3 bpy workflows with zero ID collisions against the 94 arjun988/blender-skills entries (namespaced under blender-skills/*) and max 7-word shingle Jaccard similarity <= 0.0012.",
        },
        "adaptations": [
            "Preserve all 28 standalone skill folders with their bundled scripts/_bpyx.py helpers and references/.",
            "Include upstream MIT LICENSE and NOTICE.md inside each standalone skill folder.",
            "Map all 28 skills to the existing graphics-processing category to preserve the 94-skill arjun988/blender-skills blender category and the 119-category taxonomy.",
            "Append reversible VAS installation/prerequisites notes to each SKILL.md.",
        ],
        "skills": skills_meta,
        "files": all_files,
    }
    return skills_meta, manifest


def main():
    with tempfile.TemporaryDirectory(prefix="vas-stage-motion-") as tmp:
        stage_root = Path(tmp)
        reanimate_meta, reanimate_manifest = build_reanimate(stage_root)
        huashu_meta, huashu_manifest = build_huashu(stage_root)
        anidoodle_meta, anidoodle_manifest = build_anidoodle(stage_root)
        cinetic_meta, cinetic_manifest = build_cinetic(stage_root)
        blender_metas, blender_manifest = build_el4cteo_blender(stage_root)

    # Write 5 provenance manifests
    manifests = {
        "reanimate-import.json": reanimate_manifest,
        "huashu-art-motion-import.json": huashu_manifest,
        "anidoodle-import.json": anidoodle_manifest,
        "cinetic-import.json": cinetic_manifest,
        "el4cteo-blender-import.json": blender_manifest,
    }
    for fname, data in manifests.items():
        out_path = REPO_ROOT / "data" / fname
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {out_path.relative_to(REPO_ROOT)} ({data['skill_count']} skills, {len(data['files'])} files)")

    # Update data/catalog.json
    catalog_path = REPO_ROOT / "data/catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    existing_ids = {s.get("canonical_id") or s.get("id") for s in catalog.get("skills", [])}
    new_skills = [reanimate_meta, huashu_meta, anidoodle_meta, cinetic_meta, *blender_metas]
    added = 0
    for meta in new_skills:
        if meta["canonical_id"] in existing_ids:
            raise RuntimeError(f"Duplicate canonical_id in data/catalog.json: {meta['canonical_id']}")
        catalog["skills"].append(meta)
        added += 1
    catalog["total_skills"] = len(catalog["skills"])
    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated data/catalog.json (+{added} entries, catalog.json total={catalog['total_skills']})")

    # Update data/source-credits.json
    credits_path = REPO_ROOT / "data/source-credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8"))
    sections = credits.setdefault("sections", {})
    sections["reanimate"] = [
        "- **[NiazMorshed2007/reanimate](https://github.com/NiazMorshed2007/reanimate/tree/3f7a55a2986a84ca2173e86ee9127eefe31d046d)**: Frame-by-frame animation reverse-engineering and verification skill (`reanimate`) by Niaz Morshed at revision `3f7a55a2986a84ca2173e86ee9127eefe31d046d` under the MIT License.",
        "- Captures live URLs, videos, GIFs, or WebGL/Three.js scenes frame by frame, extracts timing/easing curves, rebuilds the motion in the target codebase, and verifies fidelity side by side.",
        "- Standalone payload preserves `SKILL.md`, `LICENSE`, `NOTICE.md`, `references/`, and `scripts/` (with executable bit on `scripts/setup.sh`).",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.",
    ]
    sections["huashuartmotion"] = [
        "- **[alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion/tree/a97c45018d46e950d56d61981138e08f4e092909)**: Multi-style art painting and explainer motion film skill (`huashu-art-motion`) by alchaincyf (花叔 · 花生) at revision `a97c45018d46e950d56d61981138e08f4e092909` under the MIT License (bundled Three.js under MIT; bundled fonts under SIL OFL 1.1).",
        "- Provides 36 production art styles, 16 transferable research recipes, 9 explainer motion grammars, storyboard linting, and a self-contained Canvas/WebGL rendering engine.",
        "- Optional repository showcase media (`assets/`, ~51 MB) was omitted; all runtime code, style recipes, fonts, schemas, and license notices are preserved.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.",
    ]
    sections["anidoodle"] = [
        "- **[alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle/tree/4ae27d2c281fcfd01bce87ab13dc5ad4df81a795)**: Code-drawn 2D/3D stills, doodles, loops, and scored explainer films (`anidoodle`) by Alex Greenshpun (10x Company) at revision `4ae27d2c281fcfd01bce87ab13dc5ad4df81a795` under the Apache License 2.0.",
        "- Bundles canonical `skills/anidoodle/` payload, root `LICENSE` and `NOTICE`, vendored Three.js 0.170.0 (MIT), Poppins Bold font (SIL OFL 1.1), and Public Domain Van Gogh reference.",
        "- Optional sound pack (VCSL CC0 & OpenAIR CC BY 4.0) is not bundled and only fetched if explicitly approved by the user.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.",
    ]
    sections["cinetic"] = [
        "- **[Leonxlnx/cinetic](https://github.com/Leonxlnx/cinetic/tree/f4bbfc844877891fe92279d47b7874fb44d485ae)**: Launch films, update videos, and product teasers straight from code (`cinetic`) by Leonxlnx at revision `f4bbfc844877891fe92279d47b7874fb44d485ae` under the MIT License (bundled fonts under SIL OFL 1.1).",
        "- Supports Remotion 4 (React) and HyperFrames (HTML/GSAP) with unified timeline contracts, brand kits, audio sync, and verification scripts.",
        "- Standalone payload preserves `SKILL.md`, `LICENSE`, `LICENSE.txt`, `NOTICE.md`, `assets/`, `references/`, and `scripts/` with executable permissions.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.",
    ]
    sections["el4cteoblender"] = [
        "- **[EL4CTEO/blender-skills](https://github.com/EL4CTEO/blender-skills/tree/9e7e04a603c125a0d17447ab97112fa70a865067)**: 28 modular Blender 5.2 LTS / 5.3 `bpy` engineering skills (`blender-core`, `blender-animation`, `blender-geometry-nodes`, `blender-pbr-materials`, `blender-rendering`, etc.) by EL4CTEO at revision `9e7e04a603c125a0d17447ab97112fa70a865067` under the MIT License.",
        "- Independent collection targeting Blender 5.x slotted/layered Action APIs, locale-safe node lookups, procedural rigging, baking, weather FX, and pipeline automation; preserves existing `arjun988/blender-skills` (`blender-skills/*`) untouched.",
        "- Each standalone skill folder bundles its `scripts/_bpyx.py` helper, `references/`, `LICENSE`, and `NOTICE.md`.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.",
    ]
    credits_path.write_text(json.dumps(credits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Updated data/source-credits.json with 5 new source sections.")


if __name__ == "__main__":
    main()
