# Lettering

Place each major word at its measured spoken time, with sufficient reading time and safe spacing. Keep all meaning and caption coverage. Use the actual bundled font metrics; do not estimate glyph widths from character count. Keep punctuation and Unicode user text intact.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/screen_text.py --help
uv run --directory '<ENGINE>' python helpers/text_render.py --help
uv run --directory '<ENGINE>' python helpers/align_words.py --help
```
