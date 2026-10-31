# Greenscreen fire, explosions, smoke, glass and burning paper

Prefer bundled transparent effects first: `explosion`, `fire`, `smoke` and `shattered-glass`. Generate a new effect when its shape, color, lettering or position must differ.

Use `solid-green-portrait.png`, a 1080x1920 plate in #00B140. `kling3_0_turbo` at 5 seconds measured about 8–10 credits and 10 minutes per effect; ordinary `kling3_0` queued for over 40 minutes on the same request. Turbo output included usable fire crackle. Check current cost and obtain authorization. Scripts require numpy, Pillow and FFmpeg.

## Generate and extract

1. Prepare a 9:16 start image with the effect's final position. For burning text: `sticker_on_green.py --lines 'Line one|Line two' --y 268 --output green_start.png`. Keep lettering away from the face.
2. Upload with authorization and request `kling3_0_turbo`, 5 seconds, with the image as `start_image` and the relevant [prompt](prompts.md). Use 720p for ordinary effects, 1080p for fullscreen text. Generate two variants when shape matters.
3. Inspect a frame, then extract only the effect area. These measured settings reproduced the bundled effect dimensions; adapt them to each clip:

```sh
python3 recipes/greenscreen-effects/extract_effect.py fire_ai.mp4 fire.webm --crop 0,640,720,520 --warm
python3 recipes/greenscreen-effects/extract_effect.py explosion_ai.mp4 explosion.webm --speed 1.2 --crop 0,120,720,960 --lit-green --fade-bottom 0.74,0.86
python3 recipes/greenscreen-effects/extract_effect.py smoke_ai.mp4 smoke.webm --mode neutral --crop 0,340,720,940
python3 recipes/greenscreen-effects/extract_effect.py glass_ai.mp4 glass.webm --mode neutral --speed 1.28
python3 recipes/greenscreen-effects/extract_effect.py paper_ai.mp4 paper.webm --width 1080 --speed 1.25
```

Crop values are x,y,width,height in source pixels (turbo 720p output is 720x1280). The contact sheet shows light and dark backgrounds. Increase `--margin` toward 20 or 26 to remove green/pink edges; use `--fade-bottom` or `--erase x0,y0,x1,y1` for unwanted floors or invented objects, and `--min-alpha 0.08` for dirty haze.

## Visual checks

- Keep portrait effects in 9:16 at their final size. Burning paper generated in 16:9 left the frame and appeared clipped near the person's head.
- Explicitly exclude a mushroom cloud, column, stem, floor and pillar of fire when requesting an irregular midair explosion.
- `--lit-green` handles green illuminated yellow by an explosion. `--mode neutral` neutralizes white smoke and glass; `--warm` restores pale fire. Green effects cannot be keyed from green; request another background or effect color.
- Generated effects can feel slow; `--speed 1.2` to `1.6` often helps. Light smoke may disappear on a bright video; use darker late smoke or a temporary `effect-vignette`.
- Trim the beginning with `--start` to align the burst with the person's reaction. Explosion and glass scenes expect the event around 0.4–0.5 seconds into the clip; verify your output.

## Assembly

Apply a matching scene, for example `apply.py --project <PROJ> --use explosion --start 20.3 --end 23.5`. Copy the new WebM into `assets/visuals/video/` under a unique name and change the copied scene's video `src`. Media paths are read directly from HTML, not a scene parameter.

| Scene | Bundled file | Expected geometry |
|---|---|---|
| `explosion` | `41-explosion.webm` | 720x960; burst near 50% x, 51% y; plays once |
| `fire` | `42-fire.webm` | 720x520; wide strip with flame base at the bottom |
| `smoke` | `43-smoke.webm` | 720x940; enters below and fades at the top |
| `shattered-glass` | `44-glass.webm` | 720x1280; break near 50% x, 37% y |

Adjust position, size and strength in the scene's `P` object. Use `--sounds` to align the bundled impact. Fullscreen burning paper or other standalone effects use `common/video-overlay.html` with exact media duration; transparency is supported. Extract authorized generated audio with FFmpeg `-vn` if useful. Start burning text a few frames before its spoken phrase. Matching a real lighter to the sticker requires source-specific placement and scale; generated sound beyond the returned clip was not tested.
