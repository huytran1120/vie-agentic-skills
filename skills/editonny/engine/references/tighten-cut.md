# Tighten pauses in an exported video

`helpers/tighten_cut.py` trims an already composed video, keeping its image and audio together. Use it only when the authorized scope includes changing those intervals. All captions, scenes, and sounds move with the video; regenerate any external timeline from the returned time map.

```sh
uv run --directory '<ENGINE>' python helpers/tighten_cut.py --help
```

The pause minimum identifies candidate gaps; the maximum sets the remaining gap. These thresholds are task choices, not proof that every detected gap should disappear. Preserve expressive pauses, complete words, and natural pacing. Protect sound-effect attacks, use a voice-only reference when available, and inspect frame changes so a join does not interrupt a visual entrance.

Use a plan-only pass and inspect proposed removals before rendering. Never overwrite the original. Listen across each changed transition and compare uncertain word edges with the source. The output sidecar records cuts and source-to-output timing.
