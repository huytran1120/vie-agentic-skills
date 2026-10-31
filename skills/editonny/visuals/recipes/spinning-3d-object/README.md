# Realistic spinning or transforming 3D objects

Use when the requested object is absent from the bundled spinning-object library, or must open, assemble or transform. Existing originals remain distributed with the skill; custom media belongs in the project or a personal library.

## Models and observed costs

| Model | Observation |
|---|---|
| `gpt_image_2_5`, 2k/high | Object image: 2.75 credits; generate two variants when shape matters |
| `minimax_h3`, 2K, start/end images | Successful rotation/transformation: 12 credits for 6 seconds, 20 for 10; approximately 15 credits total per object and 62 for one five-object video |
| `kling3_0`, start=end, 4k | Worked for a beating heart in place; more expensive |
| Flux 3 Video, 1080p | Observed 45–90 credits, poor value for this task |
| `seedance_2_5` | Observed 120 credits for 10 seconds, poor value for this task |

Verify current cost and obtain authorization. `key_black.py` needs numpy, OpenCV and FFmpeg, available through the engine Python environment.

## Workflow

1. Generate the complete centered object on pure #000000, occupying about 60% of a square frame, with studio lighting and no lettering, numbers, logos or brands. Use the [prompts](prompts.md).
2. For a transformation, edit the first image into the other state using its `job_id` as an image reference. For construction, create the finished house first, then edit it into just its foundation slab; animate from slab to house.
3. Request `minimax_h3`, `resolution: "2K"`, 6 seconds, with `start_image` and `end_image`. Use the same image for a complete rotation loop, different states for transformation. A slowly rotating sun used only `start_image`. The cash drawer example worked with `kling3_0` at 3 seconds; a house assembly used MiniMax at 6 seconds.
4. Extract and inspect:

```sh
python3 recipes/spinning-3d-object/key_black.py object_ai.mp4 object.webm
python3 recipes/spinning-3d-object/key_black.py object_ai.mp4 preview.png --png-at 2.0
```

For open structures such as DNA or a grid, use `--holes open`; for both genuine gaps and dark solid surfaces, use `--holes auto`. A cart's grid and a phone's black screen were preserved correctly with auto mode. For a sun/glowing object, begin with `--lim 0.5 --band 0.25 --distant 0.12`. To align an opening to a word, use `--mapping '0:0,1.2:1.2,2.0:5.8' --dur 3.0`: source frame time 5.8 appears at output time 2.0. Check the PNG over both light and dark backgrounds.

## Checks and assembly

Keep every moving part inside the frame. One opening-Earth variant threw a wedge beyond the edge; another opened like a door and stayed within bounds. An opening heart needed a narrower edge fade (`--border 0.035`). Explicitly exclude invented text, numbers and logos on products. If the provider returns a preset recommendation, use `declined_preset_id` on the next request. Compression specks beyond `--distant` from the silhouette are removed. Any numerical labels require real, checked information.

For an upper-screen information card, apply `object-card`, copy the new WebM to `assets/visuals/video/`, and replace the copied scene's video `src`. Edit card text in `P`; media is read from HTML rather than a parameter. Use `house-construction` for staged building or opening-Earth labels. Behind-person placement uses the engine's layered composition and approved person cutout; see `references/framing.md`.

Store reusable custom WebM files outside the skill/checkout with duration, size and looping notes, copying only used files into each project. Do not add personal files to the distributed-originals manifest. `brazil-map` and `solar-system` already exist as code scenes. Custom space backgrounds use the empty-set and recreated-environment techniques.
