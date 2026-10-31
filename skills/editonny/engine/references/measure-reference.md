# Measuring a reference

Inspect actual reference frames and audio. Record dimensions, intervals, scene changes, colors, text regions, framing, motion, and sound relationships. Treat heuristic or OCR output as evidence requiring inspection. Do not upload private references without authorization.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/measure_reference.py --help
uv run --directory '<ENGINE>' python helpers/filmstrip.py --help
uv run --directory '<ENGINE>' python helpers/contact_sheet.py --help
```
