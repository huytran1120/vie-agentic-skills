# Notice for huashu-art-motion

This skill payload is adapted from upstream repository [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion)
at commit revision `a97c45018d46e950d56d61981138e08f4e092909`.

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
