# Review and delivery

Inspect the exported video in motion, not just the browser preview. Listen to suspicious joins and reported clipping or echo. Check the actual audio track, encoded true peaks, caption coverage, face clearance, and frame dimensions. Never describe a metric as a listening test.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/audit_cut.py --help
uv run --directory '<ENGINE>' python helpers/voice_check.py --help
uv run --directory '<ENGINE>' python helpers/audit_data.py --help
uv run --directory '<ENGINE>' python helpers/quality_gate.py --help
```
