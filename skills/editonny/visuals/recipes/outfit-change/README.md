# Outfit, body and environment changes

Use when a real performance needs another outfit, profession, body or setting, preferably switching on a snap, turn or spoken cue. Start with fixed-camera source footage and an approved cut. Preserve the original voice and performance through the synchronized picture-camera workflow in [RECIPES.md](../RECIPES.md).

## Models and observed costs

| Model | Observation |
|---|---|
| `kling_video_edit`, `mode: "pro"` | Preserved face, glasses, beard, background and gestures; lip correlation reached 0.94 after delay compensation. Accepts clothing `image_references`. Measured at 2 credits/second: 12 for 6 seconds, 28–30 for 14–15 seconds. A 15-second block took about 13 minutes in the observed queue. |
| `seedance_2_5`, `video_edit`, 1080p | Measured at 12 credits/second; invented garbled embroidery, shortened 6 seconds to 5.71, and produced weaker lip correlation (0.74). |
| Genjutsu `hf_mult_replace_object`, 1080p | Quoted 11 credits/second and required a clothing photo; not thoroughly tested. |
| Kling edit for camera-angle changes | Kept the original framing rather than moving the camera. |

A `gpt_image_2_5` target image at 2k/high measured 2.75 credits. Verify current cost and obtain authorization for every request.

## Workflow

1. Select source blocks, beginning about 0.3 seconds before the gesture and ending near the next change, with a maximum around 15 seconds. Split longer blocks at a speech cut. Locate a snap in its 30–50 ms audio peak or the finger-contact frame.
2. Extract with `clip_for_ai.py --source SOURCE.mp4 --start 8.6 --end 18.1 --output ai/input/outfit1.mp4`. Join source pieces with `--pieces 39.7-41.3,42.6-46.0,52.6-56.7` when appropriate; internal cuts were preserved in the observed output.
3. Agree on the outfit using a short sample and side-by-side alternatives. Generate one target image from a frontal frame with the mouth closed, then reuse it in every block for consistent clothing and background.
4. Use the [prompts](prompts.md) with `generate_video`, `model: "kling_video_edit"`, `mode: "pro"`, and the clip as `video_references`. Supply the clothing or target image as `image_references`. Estimate cost first.
5. Insert with `ai_in_cut.py --start <gesture-source-time> --name OUTFIT1 ...`, using a unique camera name per block. Inspect lips, hands, microphone, watch and consistency between blocks.

## Put an object in the correct hand

Text alone twice put a dumbbell into the microphone hand and erased the microphone. A green guide in the correct closed fist worked:

```sh
uv run --no-project --python 3.11 --with 'mediapipe==0.10.14' --with 'numpy<2' --with opencv-python-headless python recipes/outfit-change/reference_object.py ai/input/outfit1.mp4 ai/input/outfit1_guide.mp4 --hand right --shape hex
```

`--hand` refers to the person's own hand. Shapes are `bar` across the wrist, `horizontal` for frontal curls, `hex` for a dumbbell viewed end-on, and `ball`. `--scale` changes size. For joined pieces, supply `--request ai/input/outfit1.json` so smoothing does not cross cuts. Inspect at least two frames to verify placement.

Submit the guide clip and the object's photo using the replacement prompt. Clothing plus a guided object worked together (24 credits for 12.6 seconds); text-only object instructions were ignored when combined with clothing. Keep using the original timing JSON because the guide preserves its frame sequence. Open stationary hands were ignored even with the guide; choose a closed-fist segment or cut around it.

## Timing and visual checks

- Kling returned 24 fps with 55–85 ms delay, usually 67–71 ms. The insertion tool measures it, warns on weak movement and falls back to 71 ms.
- Outputs were up to 0.14 seconds shorter and contained `8k+1` frames. Add ending handles; uncovered source footage remains original.
- A 30 fps source converted to 24 fps repeated about one frame in five. Prefer shorter blocks during fast motion.
- A request starting 0.2 seconds before movement stretched a seated opening to 1.3 seconds. Start near the relevant action.
- “Muscular” alone produced a merely athletic result. The stronger prompt explicitly requests a dramatic transformation while retaining head size and identity.
- Thin-strap tank-top wording produced the wrong garment. Specify the intended cut, such as a men's crew neck, wide shoulders and straight armholes.
- Reference logos are copied; remove them. Generated clips may be slightly warmer, visible during mid-sentence switches. Reuse a target image to stabilize collars and straps.
- If wireless-microphone delay was corrected in a replacement source, extract from that exact file listed in `sources`.
- Image prompts may reject anatomy or underwear wording. Use an accurate neutral description; do not change the intended content to misrepresent the result.

Add `transition-glow` at the cut-time switch, for example `apply.py --project <PROJ> --use transition-glow --cut 12.40`. Profession titles can use `text-spring` or `text-impact`. Place an impact or snap sound peak on the switch frame; strong denoising can remove the recorded snap, so listen again. Custom muscle highlights and hand-built light sweeps are outside this recipe. Environment-only changes work, but use them when the speech actually calls for another setting.
