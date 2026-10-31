# editonny engine

The local processing engine used by the [editonny skill](../SKILL.md). Start with the skill for editorial decisions and [WORKFLOW.md](WORKFLOW.md) for execution. This directory is `<ENGINE>` in commands.

The engine provides local transcription, waveform timing, cut verification, captions, framing, audio processing, motion overlays, and the pinned HyperFrames project template. Its Python dependencies are declared in `pyproject.toml` and locked in `uv.lock`; do not upgrade them as part of an edit.

```sh
uv sync --directory '<ENGINE>'
uv run --directory '<ENGINE>' python helpers/transcribe_batch.py '<VIDEOS>' --language auto
```

Keep originals unchanged. Store generated work in the project's `edit/` directory. A generated HyperFrames project uses `project.json`; the template README documents its commands. Run any helper with `--help` for its exact arguments.

First-party code is MIT licensed; dependency and bundled resource licenses remain listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Author and contact

Created and maintained by **Matheus Gomes**. [Instagram: @matheusgomes](https://instagram.com/matheusgomes) · [Email: eu@matheusgom.es](mailto:eu@matheusgom.es) · [GitHub](https://github.com/soumatheusgomes/editonny).
