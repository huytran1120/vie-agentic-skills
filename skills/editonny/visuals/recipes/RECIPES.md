# AI-assisted visual recipes

These recipes extend the bundled scenes with footage generated for a particular source video. Read this overview, then the relevant recipe. Generated media remains project or personal-library content; it does not become part of the distributed library.

| Recipe | Use |
|---|---|
| [Outfit change](outfit-change/README.md) | Change clothing, body, environment or a handheld object while preserving the real performance |
| [Object to stone](object-to-stone/README.md) | Replace a thrown object, freeze it before impact, or make stone lettering break a floor |
| [Greenscreen effects](greenscreen-effects/README.md) | Generate and extract fire, explosions, smoke, glass and burning paper |
| [Empty set](empty-set/README.md) | Recover the real background and rotate a real person cutout through 180 degrees |
| [Spinning 3D object](spinning-3d-object/README.md) | Generate a realistic object rotation or transformation with transparency |
| [Recreated environment](recreated-environment/README.md) | Insert realistic room changes before or behind the person using aligned photos |

## Shared tools

`<SKILL>` is the skill directory, `<EDIT>` the edit directory, `<PROJ>` the generated project, and `<VISUALS>` this visual library. Use absolute script paths. The engine environment supplies numpy, Pillow and OpenCV: `uv run --directory '<SKILL>' python '<absolute-script>' ...`. MediaPipe recipes specify their isolated dependency command separately.

| Tool | Purpose |
|---|---|
| `common/clip_for_ai.py` | Extract source footage by frame number, join pieces, convert HDR to SDR and save exact timing metadata |
| `common/ai_in_cut.py` | Measure generated delay and register footage as a picture-only synchronized camera |
| `common/clean_plate.py` | Recover a fixed-camera background from frames where different regions are visible |
| `common/video-overlay.html` | Place a finished segment or transparent effect over the cut |

## Put generated picture into a cut

Generate from the original source listed in `edl_manual.json`, so subsequent cut changes can reuse the same generated clip. Keep the original voice; only switch picture.

```sh
python3 recipes/common/clip_for_ai.py --source SOURCE.mp4 --start 42.10 --end 55.80 --output ai/input/outfit1.mp4
uv run --directory '<SKILL>' python '<absolute-path>/recipes/common/ai_in_cut.py' --request ai/input/outfit1.json --ai ai/output/outfit1.mp4 --name OUTFIT1 --edit '<EDIT>' --edl '<EDIT>/edl_manual.json' --start 43.05
```

Upload and generate only with authorization, then download to the specified output path. The second command uses original-source seconds for the switch; without `--start`/`--end`, it uses all covered footage. Rerun `waveform_cut.py` and `render_cut.py`. Inspect lip sync immediately after the switch. For a one-frame adjustment, change `adjustment_s` by approximately ±0.033 in that camera's `synchronization.json` entry and render again.

The tool writes a `_cam.mp4` with unchanged picture and silent audio because waveform analysis needs an audio stream for every source. It preserves `.before-ai.json` backups of synchronization and EDL files; restore those before rebuilding multiple insertions. A rebuild that finds an unregistered `_cam.mp4` writes `_cam_2.mp4` instead of overwriting it. The tool stops before writing anything when a camera name is already used by another file or by the primary source, or when the EDL renders with a different synchronization file than `--edit`. A measured 24 fps clip delayed by 71 ms and shortened by 0.08 seconds aligned within one frame after 24→30 fps conversion; delay estimation error was about 4 ms. These observations are examples, not guarantees.

## Generation workflow

- Obtain authorization for uploads and spending. Before each paid request, query `get_cost: true` in `generate_video` or `generate_image`, then disclose the returned cost. Recipe credit figures are historical measurements; verify current pricing.
- Start with a 4–6 second sample and a contact sheet. Compare alternatives beside the original before generating all blocks. Keep each edit request at roughly 15 seconds or less; 15.57 seconds failed in the observed workflow.
- Authorized uploads use `media_upload`, PUT to its returned URL with the correct content type, then `media_confirm`. `media_import_url` imports an authorized remote reference. A previous result can be referenced by `job_id` without another upload.
- If the provider returns a preset recommendation instead of media, resend with its `declined_preset_id`.
- Prompts specify what changes and explicitly preserve face, glasses, beard, hair, hands, watch, microphone, background, lighting, framing, camera, gestures and lips. Adapt bracketed details to the source.
- Preserve the real person's identity. Video generated from a portrait changed the face in observed trials; editing the real video preserved it better. Do not promise a result, cost or completion time that has not been measured for the task.
- Remove unwanted branding from clothing references and crop out the reference model's face.
- Run one heavy render at a time. Segmentation, generation and rendering compete for resources.

A second generated camera angle, custom finger counters, head overlays and elaborate hand-built light sweeps are not packaged recipes. Use supported scene transitions and pointers where appropriate.

## Register a video overlay

Copy `common/video-overlay.html` to `compositions/scenes/` with a unique filename. Match its `<template>` ID (`name-template`), `data-composition-id`, `window.__scenes` key and `window.__timelines` key to the filename stem. When using multiple copies, also give each element-ID prefix a unique name. Put generated media in `assets/ai/` and update the video `src` directly.

Set `data-duration` to the exact media duration: a longer duration holds the last frame. Register the scene's `file`, `start` and `end` in `project.json`. Round the start down to three decimals (12.0333 → 12.033); rounding upward can delay the picture by a frame. Use an underlying `fullscreen` block with `zoom: 1.0` for an opaque matching overlay. Set `hidesCaptions: true` only when the overlay already displays the spoken text. Parameters `entrance` and `exit` are fade durations (zero for frame-matched cuts), and `opacity` controls layer strength. Validate the composed result with `build.py hf lint`, `build.py hf check` and frame inspection.
