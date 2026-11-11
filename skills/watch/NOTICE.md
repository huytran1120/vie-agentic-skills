# Notice for watch

This skill payload is adapted from upstream repository [bradautomates/claude-video](https://github.com/bradautomates/claude-video)
at commit revision `03ceb42f7fa2c4439aca01752118044baabffb8f`.

- Author: Bradley Bonanno
- Upstream License: MIT License (see bundled LICENSE)
- Upstream Source Path: `skills/watch`
- Adapted for Vie Agentic Skill (VAS) distribution.

## Bundled Components and Provenance

- `SKILL.md`: Core runbook and Agent Skills specification for video inspection, multimodal understanding, frame extraction, and transcription.
- `scripts/`: Standalone Python scripts implementing the watch pipeline (`watch.py`, `setup.py`, `frames.py`, `download.py`, `transcribe.py`, `whisper.py`, `local_whisperx.py`, `gemini.py`, `config.py`, `runtime.py`, `build-skill.sh`).
  - Base runtime operates entirely on Python's standard library (Python 3.10+).
  - External binaries (`ffmpeg`, `yt-dlp`) and optional models (`whisperx`, `groq`, `openai`, `gemini`) are user-configured prerequisites and are never executed or downloaded during VAS skill installation.

## VAS Adaptation Notes

- Preserves upstream directory structure and standalone execution semantics.
- Appended standard VAS installation, attribution, and safety notes to `SKILL.md`.
- Mapped to existing `media` category to preserve the exact 119-category taxonomy.
- Managed by Vie Agentic Skill (VAS) with zero external package manager dependencies (no NPX).
