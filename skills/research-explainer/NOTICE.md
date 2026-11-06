# Notices

`research-explainer` is imported from [sepi2p/research-explainer-skill](https://github.com/sepi2p/research-explainer-skill) at revision `374ecd10fdf60bd08269ff7f51464f754a504ce7` under the MIT License (Copyright (c) 2026 sepi2p); see `LICENSE`.

## Bundled Third-Party Components

- Inter Font: SIL Open Font License 1.1 (`github.com/rsms/inter`).
- Vazirmatn Font: SIL Open Font License 1.1 (`github.com/rastikerdar/vazirmatn`).
- JetBrains Mono Font: SIL Open Font License 1.1 (`github.com/JetBrains/JetBrainsMono`).
- Caveat Font: SIL Open Font License 1.1 (`github.com/googlefonts/caveat`).
- Sound Effects: CC0 1.0 by Kenney (`kenney.nl`).
- Rough.js 4.6.6: MIT (`github.com/rough-stuff/rough`, patched with seeded PRNG for deterministic rendering).
- Watercolor Paintings: Generated for this skill by the author, released under the repository MIT license.

## Runtime & Tool Prerequisites

- Making full explainer videos with Manim Community Edition requires Python 3.10+, `manim`, FFmpeg, and cairo/pango.
- Optional rendering tools: Playwright for HTML paper dioramas, Piper TTS for free offline narration, or an OpenAI API key for paid voiceover.
- HyperFrames CLI for vertical shorts (optional).

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No scripts, renders, or node processes are executed, no external dependencies or runtimes are installed, and no API services are connected during installation.
