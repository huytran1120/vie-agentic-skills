# Render and QA

## Segmented render
```
scripts/render_segments.sh Film out/final.mp4 "0-4439:8 4440-4739:1 4740-6839:8" public/audio/soundtrack.wav
```
- Find the heavy scene (deep nesting, `filter: blur`, many 3D layers, motion blur at 8 samples) and render it alone at `--concurrency=1`. Its frames take 2–4 s as single stills, but with 8 tabs headless Chrome's GPU process can deadlock: "Rendered 4698/6840" repeats forever with no error.
- **How to diagnose:** check whether the encoder's temp output (`lsof -p <ffmpeg pid>`) is still growing. Render stills of the frames around the stuck one; if they are fine on their own, the cause is concurrency, not the frame.
- `pkill -f chrome-headless-shell || true` between segments. In zsh, a cleanup glob with no match aborts an `&&` chain; use `find out -name 'seg_*.mp4' -delete`.
- Joining with `-c copy` is lossless; each segment starts on a keyframe.

## Measured render time on screen
1. Render all segments and record the wall clock (`RENDER_SECONDS`).
2. Write the number into `footage.ts` with a comment (date, machine, start → end).
3. Re-render only the segment that shows the timer, then concat and mux.

## Gates (run all; report the numbers)
| check | tool | pass |
|---|---|---|
| duration and frames | `ffprobe -count_packets` | exactly TOTAL frames |
| frozen stretches | `scripts/check_static.py` | none ≥ 0.1 s unless intended |
| loudness | `ffmpeg -af ebur128=peak=true` | −14 LUFS integrated, true peak ≤ −1 dBFS |
| layout | `scripts/sheet.sh` on every scene | no overflow (watch inherited `white-space: pre`), no overlap with captions or mascot |
| sync | a frame at each cut ±0.1 s | joins clean; the drop flash lands on the drop |
| mascot | a tile of every 6th frame across a move and a gesture | no pops or see-through frames |

## Fast loops
- Preview: `npx remotion render Film out/preview.mp4 --props='{"mb":0}' --scale=0.5 --concurrency=2` (about 100 s for 2 min).
- Spot fixes: `npx remotion still Film --frame=N --props='{"mb":0}' --scale=0.5 out.png`.
