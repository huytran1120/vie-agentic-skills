# Mascot presenter

## 1. Design an original character
- **Never a franchise character**, and not fan art of one either. If the user offers one (an avatar they like), say why not (copyright, plus "all content must be your own" in coursework) and keep only the *vibe*: the props, the palette, the mood.
- Generate 2–3 designs from text-only prompts (no IP reference image) and let the user pick. Then iterate by **edits** of the chosen image: outfit colour, a cap, glasses, a body shape ("chubbier, rounder, mochi-like"), props. A laptop is "silver aluminium, MacBook-like, absolutely no logo".
- Prompt pattern for the base:
  > Original cartoon mascot, NOT any existing franchise character. <species, colours, outfit, props>. Chibi hand-drawn sticker style, thick dark-navy outline, soft cel shading. Background: perfectly flat solid pure magenta #FF00FF everywhere, no floor, no shadow. Square 1:1, centred, full body, ≥ 14% margin on all sides.

## 2. Frame set (all edits of ONE locked base)
Edit prompt pattern:
> Edit the reference image. Keep EVERYTHING identical (same character, pose, position, size, framing, colours, style, magenta background). ONLY CHANGE <one thing>.

| group | frames |
|---|---|
| visemes | closed, half, open, ee (wide grin, upper teeth), oo (small round), wide (tall, tongue), fv (teeth on lower lip) |
| blink | blink_half, blink |
| idle | type_a, type_b (one flipper on the keys each) |
| gestures | wave + wave_a (low), wave_b (out), wave_c (in); point + point_half; cheer + cheer_half |

Generate them in parallel (about 1 min each). Edits keep alignment: silhouette IoU against the base is 0.999 for mouths and 0.90–0.97 for gestures.

## 3. Keying
`scripts/key_magenta.py in.png out.png --nocrop`:
- alpha from the distance to pure magenta, with a soft ramp;
- magenta despill (`min(R,B) − G`) subtracted on edge pixels;
- output 768×768 on the **same canvas** for every frame. Don't crop to the bounding box, or the swaps will shift.

A naive `colorkey` + `despill` turns blue clothes purple. Use this script instead.

## 4. Animation (`Mascot.tsx`)
- **Visemes from letters:** a → wide (alternate with open), e/i/y → ee, o/u → oo, m/b/p → closed, f/v → fv, anything else → half. Spread them evenly across the word's `t0..t1`, with a 3-frame crossfade. A gap of more than 3 frames between words closes the mouth.
- **Idle:** after 30 frames without speech, a typing loop (type_a/type_b every 9 frames, 4-frame crossfade). A blink every 200 frames: closed → half → blink → half → closed over 12 frames.
- **Gestures:** wave = in (wave_a), loop (wave, wave_b, wave, wave_c at 7 frames each), out; point = half → full, hold, back to half; cheer = half → loop (cheer, cheer, cheer_half). Each gesture fades in and out against the body pose over 4 frames.
- **Opaque blending:** sort sprites by weight; the heaviest is drawn at opacity 1, and each layer above at `w / (sum of weights so far)`. A plain opacity blend makes the character see-through mid-blend.
- **Movement:** a list of timed moves `{at, dur, x, y, size, face}`:
  - eased position;
  - a hop arc `sin(πu) · min(90, 30 + 0.18·distance)` whenever the move is more than 30 px;
  - stretch in the air, squash at the ends;
  - facing changes turn through `scaleX = from.face · cos(π·ease(u))`;
  - a contact shadow that shrinks with height;
  - breathing `scaleY 1 + 0.014·sin(f/13)` and a small talk wobble.
- **Placement:** keep a home position (bottom-right, out of the captions' width). Hop to free space near what it points at, hop off-screen for the climax, and come back big next to the call-to-action card, cheering.
