# Recreate an environment with a photo chain

Use a fixed camera when speech calls for realistic objects inside the actual room, before or behind the person. Each generated photo edits the same room; alignment and local masks preserve the original video elsewhere.

Use `gpt_image_2_5`, 2k/high, one object per image. Historical cost was 2.75 credits/image, about 36 credits for 13 photos; recording the composite took roughly one minute per ten seconds of video. Verify current pricing and authorization. Scripts require numpy, OpenCV and FFmpeg. Behind-person changes also need an approved person cutout.

## Workflow

1. Recover a clean plate with `common/clean_plate.py`, repairing missing areas using the [empty-set recipe](../empty-set/README.md).
2. Generate a chain with the [prompts](prompts.md): first edit the plate, then pass each preceding image's `job_id` into the next request. Specify object position and size as image percentages. Default 752x1344 output was weak; explicitly request 2k/high.
3. Align and isolate changes:

```sh
uv run --directory '<SKILL>' python '<absolute-path>/recipes/recreated-environment/align_photo.py' --plate plate.png --photos f1.png f2.png f3.png --boxes '0,62,100,100' '8,70,48,96' '55,60,95,90' --folder chain/
```

Supply one generous percentage box per photo. The tool aligns each image, matches color and extracts changed regions. Inspect `N_preview.jpg`: the first mask should contain the whole counter, for example, while the next contains only the newly added tomatoes and their reflection.

4. Generate the person cutout in the project with `tools/person_cutout.py --edit '<EDIT>' --start 12 --end 18.5`.
5. Render steps at cut-word times:

```sh
uv run --directory '<SKILL>' python '<absolute-path>/recipes/recreated-environment/record_environment.py' --video '<EDIT>/cut.mp4' --start 12 --end 18.5 --plate plate.png --cutout '<PROJ>/assets/person.webm' --step chain/1_photo.png chain/1_mask.png 13.20 0.5 from-bottom+front --step chain/2_photo.png chain/2_mask.png 15.05 0.3 appear --output '<PROJ>/assets/ai/environment_12.mp4'
```

Entrances are `appear`, `from-bottom`, `from-top`, `from-left`, `from-right`. Append `+front` for foreground objects. Without a cutout all steps are foreground. Use `--test 13.5,15.4` first to save preview frames instead of a complete video.

6. Copy `common/video-overlay.html` into project scenes, point its video at the generated MP4 and use its exact duration. Register the start printed by the script, rounded down to three decimal places. Set underlying `fullscreen` zoom to 1.0 so pointers and overlay geometry remain aligned.

## Compositing and checks

Foreground blending uses `output = V*(1-A) + photo*A`, with A equal to mask times entrance progress. Behind-person blending uses `output = V + beta*changedMask*(newBackground-oldBackground)`. The old background comes from video outside the person and the clean plate at their edge. Beta is one minus the person mask with a physical/color-derived ceiling near the edge; this prevents a dark fringe when an eroded cutout exposes a formerly bright background.

- Small unrelated generation changes are constrained by each step's box. For holes in similar-colored surfaces, increase `--close` from its default 33.
- Replacing the entire room with one image made plants and vases look illustrated and doubled leaves during partial blends. Retain the real video outside local object masks.
- Generated clothing footage can shift by 1–5 pixels and change color per shot. Align plate and photo chain separately for each take, using that take's frame as `--plate`.
- For falling/growing objects, use an isolated layer anchored at its base; reveal the reflection only at contact.
- Place labels away from the face. With block zoom 1.0, labels stay aligned with recorded objects. Synchronize short pops/whooshes to each entrance.
- Neutral, accurate anatomy/clothing descriptions can avoid unintended model interpretations; inspect any rejected or altered result before continuing.

For a wireframe-to-solid reveal, generate the object, then edit that image into a wireframe version. Align both in order, but use the object's `1_mask.png` for both steps: show `2_photo.png` with `appear`, then about 0.3 seconds later `1_photo.png` with `from-bottom`. Animated wireframe sweeps, floor grids and half-photo room warming are project-specific effects outside this recipe.
