# Object to stone, suspended impact and falling stone text

Use a real held or thrown object for literal weight jokes. There are three independent parts: replace the object with stone, freeze it just before impact, or cut to a generated floor where stone lettering lands. The bundled `stone-text` scene already handles illustrated falling stone text; generate a floor shot only when realistic damage is needed.

## Replace the object

Extract the complete pickup, lift, throw and landing from the fixed-camera source with `clip_for_ai.py`. Submit to `kling_video_edit` pro with the [replacement prompt](prompts.md). A 6–7 second clip measured 12–14 credits (2/second) and worked on the first attempt; verify cost and authorization.

Inspect impact frames with `freeze.py input.mp4 unused.mp4 --frame 106 --sheet sheet.jpg`. Two blurred/duplicated frames in the observed result were replaced with clean neighbors:

```sh
python3 recipes/object-to-stone/freeze.py ai/output/stone.mp4 ai/output/stone_clean.mp4 --replace 110:109,111:112
```

Insert using `ai_in_cut.py --start <source-time-object-appears> ...`. The measured delay was again 71 ms. Soft, pale props such as pillows or foam balls worked well because the generated edit mainly changed texture and apparent weight.

## Freeze before impact

The contact sheet shows eight neighboring frames. Pick the rock just above the head, before contact, then run:

```sh
python3 recipes/object-to-stone/freeze.py ai/output/stone.mp4 ai/output/stone_frozen.mp4 --frame 106 --hold 1.6
```

Timing remains unchanged before the hold. Insert the frozen clip as the generated camera and end the EDL range at the hold's end so the remaining fall is excluded. Original speech continues. Cut the music sharply and align a sustained impact or riser to the freeze; use authorized sound assets.

## Stone lettering breaks the floor

1. Generate the **after** image first: `gpt_image_2_5`, 2k/high, 9:16. Describe the real floor, baseboard, wall and visible furniture so the insert matches the room.
2. Edit that image into the **before** image, removing letters, cracks and debris while preserving the floor pattern. This keeps the surroundings aligned.
3. Generate between them with `kling3_0`, pro, 3 seconds, 9:16, `sound: "off"`, using `start_image` and `end_image`. A preset recommendation required `declined_preset_id`. Impact landed at frame 21 of 73 in the observed result; measure your own. `minimax_h3` failed on this fall and refunded the request.
4. Generate isolated matching letters on solid magenta and run `key_magenta.py letters_magenta.png letters.png --trim --width 900`. Gray granite disappears against black, making magenta preferable.

Historical cost: three 2k/high images at 2.75 credits each plus a 3-second video around 5–15 credits depending on references; one complete multi-effect joke totaled about 37 credits. Check live pricing.

Inspect exact spelling, accents and letter shapes. An accent appeared only at the end of one clip and required a separate overlay during the fall. Keep lettering within the safe horizontal zone, approximately x=140–940 on 1080-wide output; request at most 80% of image width. A floor insert can hide a mismatched pose between takes: enter with a downward whip and return upward. Add audible midrange texture (roughly 300–4000 Hz) to bass-heavy impacts for phone speakers.

## Assembly

The replacement and freeze enter as synchronized picture cameras. The floor insert uses `common/video-overlay.html`, an MP4 in `assets/ai/`, exact media duration and a registered scene in `project.json`. Use `transition-zoom` or `transition-glow` at entry and return, with a whoosh. Suspended letters can use `stone-text` or `entrance-zoom-one` with its `image` parameter. Align sound peaks to the impact frame.

The extra invisible-head prompt preserves the real body while removing head and neck for a clean comedic effect. Compositing the real head or duplicating the person requires project-specific masks and is outside this recipe. Protect a microphone crossing the neck by retaining that area from the original footage.
