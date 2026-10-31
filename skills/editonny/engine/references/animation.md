# Animation direction

Animate to the meaning and measured timing of the spoken phrase. Use one dominant action, readable holds, and controlled exits. Check the first, middle, and last frame and the exported transition. Hide duplicated captions only while the same spoken words are visibly written.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/render_visuals.py --help
uv run --directory '<ENGINE>' python helpers/screen_text.py --help
uv run --directory '<ENGINE>' python helpers/text_render.py --help
```
