---
name: vlog-pacing
description: The numbers and rules that make a transcript-based cut feel natural instead of "popping" - silence detection, word pads, pause shortening, room at scene edges, jump-cut zoom alternation and punch-ins. Use when building the cut planner, tuning pauses, or when the creator says the edit is too choppy or too slow.
category: media
risk: safe
author: appariciojunior
license: CC-BY-NC-4.0
source_repo: appariciojunior/video-editor-skills
---

# Pacing: how much air to leave

A transcript cut is precise; the danger is that it is *too* precise. Every cut becomes a jump cut and the video "pops". These values came from real feedback.

## Cut from the transcript, never from volume
A volume-only silence cut (ffmpeg silencedetect on the whole file) gave ~800 choppy pieces on a 34-minute class. Cutting from the word timestamps gave 120 pieces the creator loved. Use the waveform only to *refine* edges.

## Planner algorithm (in words)
1. **Silence map** per clip: below **-43 dB** for at least **0.25 s**.
2. **Pause candidates** inside kept speech: gap between two words ≥ 0.25 s **and** ≥ 85% of it is silence on the waveform (an untranscribed sound is not a pause).
3. **Shorten** only pauses longer than `max_pause`, down to `pause_keep`. Split the leftover air 40% before / 60% after.
4. **Word edges:** start = word start − **0.08 s**, end = word end + **0.12 s**, refined to the nearest silence edge within 0.25 / 0.3 s so soft consonants aren't clipped; never reach into a word that was cut.
5. **Scene edges:** the first range of a clip gets **0.5 s** before the first word, the last range **0.6 s** after the last word (only *spoken* words limit this; a lighter click or ambience may stay). Override per range in the keep-list (`lead_in`, `tail`). Look at frames first: stop before the creator reaches for the camera.
6. Snap to frames (start floors, end ceils, end exclusive), remove overlaps, merge touching pieces.
7. Write a review file: the transcript with cut words struck through + a timeline list with times.

## Settings that worked

| Content | max_pause | pause_keep | Feel |
|---|---|---|---|
| Class / tutorial | 0.5 s | 0.3 s | tight, loved |
| Vlog | **1.0 s** | **0.6 s** | breathing room; 0.5/0.3 felt "popping" |

Rough check with a pause report ("what if max_pause = …: N cuts, saves X s") before choosing. On a dramatic slow opening, 0.5 s gave 7 jump cuts in 20 seconds; 1.0 s gave 3 in 53 seconds.

## Framing (zoom)
- Every **jump cut inside one scene** alternates **100% / 107.5%**, so it reads as a camera change.
- A **new scene** (new clip, or after B-roll) always opens at **100%**. Toggling zoom on scene changes adds pops.
- **Punch-in 115%** only for the punchline itself: split the piece at the line's first word and again right after its last word. Without the second split one punch-in held 83 seconds.
- B-roll is always 100%.

## When they say "it's choppy"
Measure first (how many cuts come from pause shortening vs. scene edges vs. zoom), then fix the actual cause: usually loosen pauses, add scene room, and stop zooming on scene changes. Don't guess.


## VAS installation notes

This is the `vlog-pacing` skill by appariciojunior ([@appariciojunior](https://github.com/appariciojunior)),
from [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills/tree/6709678d7d5b169149e13480428e12b0f09a47f0),
upstream revision `6709678d7d5b169149e13480428e12b0f09a47f0`.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
The full license text is preserved in the bundled LICENSE file.
You MAY use, copy, share, and adapt these skills for free with attribution and a link back.
You may NOT sell them or use them in anything sold without permission from the author.
No endorsement by the author is implied.

VAS canonical ID and installed folder: `vlog-pacing`.
Standalone payload includes `SKILL.md` and `LICENSE`.
External documentation and tool links remain live references, not bundled snapshots.

Use the VAS website's Copy Agent Prompt or `./vas install vlog-pacing --target <agent> --mode copy`
with VAS's existing destination mapping and receipt. Link mode (`--mode link`) requires
keeping the VAS checkout in place. Installing or reading this skill does not execute
code, install dependencies, configure MCP servers, modify DaVinci Resolve projects,
or make paid requests.

Prerequisites:
- DaVinci Resolve Studio (free version does not support external scripting) with
  Preferences > System > General > External scripting using: Local.
- Optional tools and services (ffmpeg, transcription APIs, Epidemic Sound, Remotion, Figma)
  require explicit user consent and separate API credentials where applicable.
  Never execute downloaded scripts or connect services without user permission.
