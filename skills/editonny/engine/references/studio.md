# Local studio and preview

Open the generated HyperFrames project using its README instructions. Use the layer timeline to inspect cut boundaries, text, scenes, face clearance, and audio cues. Keep the preview local. The exported video is the final timing reference; a preview does not prove an encoded file is correct.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/preview_server.py --help
uv run --directory '<ENGINE>' python helpers/watch_preview.py --help
```
