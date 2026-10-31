# Visual template catalog

Use the registry to inspect template parameters, defaults, required values, duration, region, and sound cues. Templates validate before rendering; invalid parameters must not produce a partial final project. Keep independent instances separate.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/render_visuals.py --help
uv run --directory '<ENGINE>' python helpers/suggest_visuals.py --help
```
