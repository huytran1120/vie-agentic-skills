# Notices

`claude-awesome-video-creation` is imported from [HaochenSHI66/claude-awesome-video-creation](https://github.com/HaochenSHI66/claude-awesome-video-creation) at revision `4b0f8d89d50046ac13003e95bcde081e328c2373` under the MIT License (Copyright (c) 2026 SHI Haochen (HaochenSHI66); Copyright (c) 2026 Leonxlnx (cinetic, which this skill is built on)); see `LICENSE`.

## Runtime & Tool Prerequisites

- Making videos with Remotion requires Node.js 22+, Remotion 4+, ffmpeg 6+, and Python 3.11+ with `numpy`, `scipy`, `soundfile`, `pyloudnorm`, and `pillow` for audio scoring, sync checks, and QA scripts.
- Optional external tools: `edge-tts` for draft voiceover synthesis, or an OpenAI/ElevenLabs API key for voice cloning.
- Codex CLI / image generation models are optional for generating custom mascot presenter sprites.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No scripts, renders, or node processes are executed, no external dependencies or runtimes are installed, and no API services are connected during installation.
