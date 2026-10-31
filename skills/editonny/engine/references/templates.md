# Using motion templates

Inspect the template registry, choose a template by purpose, and validate its parameters before rendering. Use local media and deterministic frame timing. A render failure must remain visible, without silently dropping the requested scene.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/render_visuals.py --help
```
