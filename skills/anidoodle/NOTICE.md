# Notice for anidoodle

This skill payload is adapted from upstream repository [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle)
at commit revision `4ae27d2c281fcfd01bce87ab13dc5ad4df81a795`.

- Author: Alex Greenshpun (10x Company)
- Upstream License: Apache-2.0 (see bundled `LICENSE` and upstream `NOTICE`)
- Upstream Source Path: `skills/anidoodle` (canonical skill source; duplicate plugin mirror under `plugins/anidoodle/skills/anidoodle` was not double-imported)
- Adapted for Vie Agentic Skill (VAS) distribution.

## Third-Party Bundled Material

- `engine/vendor/three/`: Three.js 0.170.0 under MIT License (see `engine/vendor/three/LICENSE` and `PROVENANCE.md`).
- `engine/assets/fonts/Poppins-Bold.ttf`: SIL Open Font License 1.1 (see `engine/assets/fonts/Poppins-OFL.txt` and `PROVENANCE.md`).
- `engine/assets/refs/vangogh-almond-blossom.jpg`: Public domain reproduction (see `engine/assets/refs/PROVENANCE.json` and root `NOTICE`).
- Optional sound pack is NOT bundled; `engine/tools/soundfetch.mjs` only downloads VCSL (CC0) and OpenAIR (CC BY 4.0) assets if explicitly requested by the user (see `references/music/sounds-licenses.md`).
