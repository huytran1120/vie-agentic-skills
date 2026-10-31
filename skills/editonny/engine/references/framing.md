# Framing and face clearance

Measure source rotation and display dimensions before cropping. Preserve eyes and mouth, leave room for captions, and review tracking at transitions. Face detection failure must be disclosed rather than silently treated as proof of safe placement. Keep a stable frame unless movement supports the story.

See [WORKFLOW.md](../WORKFLOW.md) for scope, originals, source-language fidelity, and sample review.

## Helpers

Run the relevant helper with `--help` before supplying task-specific paths:

```sh
uv run --directory '<ENGINE>' python helpers/face_layout.py --help
uv run --directory '<ENGINE>' python helpers/track_faces.py --help
uv run --directory '<ENGINE>' python helpers/camera_motion.py --help
uv run --directory '<ENGINE>' python helpers/person_cutout.py --help
```
