# Greenscreen Effects prompts

Replace bracketed details with the actual subject and scene. Preserve the identity, framing, motion and lighting constraints. Request a cost estimate and obtain authorization before generation. Model settings, observed limitations and assembly steps are in [README.md](README.md).

## 1. Request parameters

```json
{"model": "kling3_0_turbo", "duration": 5, "resolution": "720p",
 "medias": [{"role": "start_image", "value": "<green_plate_or_sticker_media_id>"}],
 "prompt": "...", "get_cost": true}
```

## 2. Fire from the bottom edge

```
Locked-off static camera. The whole frame is a flat solid chroma key green screen that stays perfectly flat green. From the very first second, huge roaring flames rise from the bottom edge of the frame across the full width: a wall of intense bright saturated [orange, yellow and red] fire with tall licking tongues of flame reaching up to the [middle] of the frame, hot glowing cores, dark red tips, and sparks and embers floating upward. Realistic stock footage fire element. The fire comes only from below the bottom edge, no burning object, no floor, no wood, no text, no smoke covering the screen.
```

## 3. Midair explosion

```
Locked-off static camera. The whole frame is a flat solid chroma key green screen that stays perfectly flat green the entire time. At [0.4] seconds a violent mid-air fireball explosion bursts in the [lower middle] of the frame: a wide round ball of bright orange and yellow fire blasting outward sideways and upward at the same time, mixed with thick black and dark grey smoke billowing outward, and hundreds of bright sparks and glowing embers shooting out in every direction. Classic action movie gas explosion, wide and irregular, floating in mid-air. Absolutely no mushroom cloud, no column, no stem, no pillar of fire, no ground, no floor, no debris, no objects, no text. The fire burns out quickly and the dark smoke spreads and fades over the green screen.
```

## 4. Smoke covering the frame

```
Locked-off static camera. The whole frame is a flat solid chroma key green screen. Thick dense grey smoke rolls in fast from the bottom and both sides and spreads across the whole frame, realistic billowing volumetric smoke clouds in neutral grey and dark grey, covering most of the screen by [2] seconds, then slowly thinning out and drifting. Only smoke, no fire, no objects, no floor, no text. Behind the smoke the background is the flat green screen.
```

## 5. Shattering glass

```
Locked-off static camera, the whole frame is a flat solid chroma key green screen. An invisible clear glass window fills the entire frame right in front of the camera from the first frame. At [0.4] seconds it is hit in the [center]: sharp irregular realistic cracks race out from the impact point across the glass, then at [1] second the whole glass shatters and hundreds of sharp jagged glass shards burst toward the camera and tumble down and fall out of the bottom of the frame, catching bright white highlights. Realistic high speed glass shattering stock footage element. No hand, no hammer, no bullet, no objects, no text, no frame. Background stays flat green.
```

## 6. Burning sticker falls away

```
Static locked-off camera, flat solid chroma green background stays perfectly uniform the whole time. The white paper sticker label near the top of the frame catches fire at its [bottom-left] corner. Realistic orange flames spread fast across it, the paper curls and chars, then the burning sticker breaks loose and FALLS STRAIGHT DOWN through the whole frame, tumbling and flaming, all the way past the bottom edge and out of frame, leaving a trail of glowing embers and ash drifting down. By the end the frame is empty green. Photorealistic fire VFX, no hands, no people, no camera movement, nothing else appears.
```

## 7. Other effects

```
Locked-off static camera. The whole frame is a flat solid chroma key green screen that stays perfectly flat green the entire time. At [time] seconds [effect, color, shape, origin and direction]. Realistic stock footage [type] element. [Excluded elements: no objects, no floor, no hands, no text]. [Ending: fades / falls out of frame / the frame is empty green by the end].
```
