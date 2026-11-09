# Notices

`motion-prompt` is imported from [`showheyohtaki/motion-prompt`](https://github.com/showheyohtaki/motion-prompt) at revision `7819d3879eb7d5a1475c11c001bedffb5cab64af` (`skills/motion-prompt/SKILL.md`) under the MIT License (Copyright (c) 2026 Shohei Ohtaki); see `LICENSE` and `THIRD-PARTY-NOTICES.md`.

## Purpose & Bundled Payload

- Provides a shared vocabulary of 192 numbered visual and motion effects (`#001`–`#192`) across 8 packs (`motion`, `camera`, `ui`, `lp`, `photo`, `motion2`, `lp2`, `camera2`), each paired with a runnable dependency-free Canvas 2D reference implementation (`cells[i](k, w, h, u)`) and concrete timing/easing specifications.
- Standalone payload includes `SKILL.md`, `references/porting.md` (translation playbook for HTML/Canvas, Remotion, CSS/WAAPI, GSAP/Motion, ffmpeg/Python/Manim, After Effects/Premiere, and generative video/image prompts), `scripts/motion-prompt.mjs` (zero-dependency Node.js 18+ CLI for `pick`, `search`, `list`, `get`, `prompt`, `kit`, and `info`), `LICENSE`, and `THIRD-PARTY-NOTICES.md`.
- Interactive gallery and live Canvas 2D previews are available on the VAS guide `/blog/thu-vien-motion-prompt-192-hieu-ung-canvas-2d/` as well as upstream at `https://showheyohtaki.github.io/motion-prompt/`.

## Prerequisites & Safe Operation

- Runtime prerequisites when executing `scripts/motion-prompt.mjs`: Node.js 18+ (`node`) and HTTPS network access to `https://showheyohtaki.github.io/motion-prompt/api/v1` or `https://raw.githubusercontent.com/showheyohtaki/motion-prompt/main/api/v1` (responses are cached locally in `~/.cache/motion-prompt/v1`).
- Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`. No script, local callback server, or network request is executed during installation.
