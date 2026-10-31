# Empty set and 180-degree turn

Recover the recording location without the person for disappearances, spotlights, behind-person effects or an upside-down opening. Fixed-camera footage is required for a reusable plate; with handheld footage, a generated plate matches only one frame.

## Recover the background from video

```sh
uv run --no-project --python 3.11 --with 'mediapipe==0.10.14' --with 'numpy<2' --with opencv-python-headless python recipes/common/clean_plate.py '<EDIT>/cut.mp4' --output '<PROJ>/assets/ai/empty-room.png' --start 0 --end 40
```

The script samples every 1.5 seconds, masks the person and averages visible background pixels. Inspect the reported never-visible fraction and `_missing.png`. A moving person left about 9% missing and the result was usable; a stationary seated person left 25% and a visible blur. Repair that area with the [missing-region prompt](prompts.md), or generate a plate from a frame.

## Generate a plate from one frame

Extract a frame with minimal background occlusion: `ffmpeg -ss 7.8 -i '<EDIT>/cut.mp4' -frames:v 1 frame.png`. Use `gpt_image_2_5`, 9:16, and the removal prompt. A 2k/high image measured 2.75 credits; a lower-cost 1k/low result was sufficient behind a fast blurred turn. Verify current pricing and authorization.

Resize to 1080x1920 and inspect over the original. Generation may shift the room 1–5 pixels. For a plate visible beyond a brief instant, align with `recreated-environment/align_photo.py`, using the recovered plate or source frame as reference.

## Turn the real person upright

1. Save the plate to `assets/ai/empty-room.png`.
2. In the generated project, run `python3 tools/person_cutout.py --edit '<EDIT>' --start 0 --end 1.2`. Output is `assets/person.webm` with `person.json`. Initial segmentation measured roughly three minutes per minute of video in the observed setup.
3. Copy `half-turn.html` to `compositions/scenes/opening-turn.html`. Change the template ID, composition ID and both scene/timeline lookup IDs consistently. Set `data-media-start` to scene start minus the cutout's metadata start; set the exact video duration.
4. Parameters: `subject` is `person`, `room` or `all`; `turnAt` is local scene time; `word` overrides it with a spoken-word anchor; `duration` is typically 0.3–0.5 seconds; `direction` is ±1; `pivotX`/`pivotY` define the rotation point; `blur` controls peak blur. The default pivot 540,960 is the frame center.
5. Register `{"file":"compositions/scenes/opening-turn.html","start":0,"end":0.9,"hidesCaptions":true}` in `project.json`. End shortly after landing (about 0.1 seconds after the turn), preferably at a picture cut. Set the underlying `fullscreen` block's `zoom` to 1.0. Align a whoosh peak to mid-turn.
6. Run `python3 build.py sample 0 3`, `python3 build.py hf lint` and `python3 build.py hf check`. Inspect the upside-down pose, middle blur and precise landing alignment. Previous versions passed lint/check; validate every edited copy.

The scene rotates the real cutout, retaining identity. Generating a person hanging from the ceiling produced a different face; Seedance with a real-face reference was rejected, and a gravity-reversal Kling edit invented different hair. Do not treat those failed approaches as reliable. If generated motion includes a real person, ending on an actual source frame helps the final identity match, but still requires inspection.

Rotating `room` or `all` exposes frame corners mid-turn; blur helps. `person` avoids that issue. Inspect cutout leftovers such as a backpack, picture frame or bright strip; adjust `clip-path` on `#turn-person-wrap` or select cleaner footage. A static plate will mismatch changing sunlight or an opening door, so keep the interval short. Scene scaling is not supported by the engine contract; use block zoom outside the overlay interval.

The spotlight prompt removes the person while retaining a lit cone in the real room. The bundled `stage-spotlight` is preferable when a code scene is sufficient. Custom somersaults, generated alternate camera angles and multilayer spotlight masks remain project-specific work.
