---
name: edit-video
description: The one-command first-pass edit. Takes footage from raw video/, transcribes it, cuts retakes and dead air while keeping a natural vlog rhythm, keeps B-roll, and builds the timeline in the open DaVinci Resolve project (footage in bins, a copy of the creator's template timeline, markers, zoom, grade, audio normalize). Use for "/edit-video", "edit the new video", "do it", or follow-up changes to a cut.
category: media
risk: safe
author: appariciojunior
license: CC-BY-NC-4.0
source_repo: appariciojunior/video-editor-skills
---

# Edit video (the whole flow)

The creator drops footage in `raw video/`, opens their Resolve project and says "do it". You run the whole thing and stop only for:
- **a frame-rate mismatch** between footage and template timeline (ask; never choose for them),
- **a failure that happened twice** (report the script's exact error and what they must fix).

Prerequisite: `video-editor-setup` is done (folders, scripts, CLAUDE.md).

## 1. Check
Run your `doctor` script. No video named? Pick what's in `raw video/` without a finished build report; if several, ask which.

## 2. Ingest
Probe, read picture profiles, transcribe (verbatim, word timestamps), detect silences, write a manifest. Report anything odd:
- picture profile *guessed* (no camera sidecar) → say so; never put a log LUT on non-log footage;
- voice on one channel only (wireless receiver in stereo mode) → make sure the voice plays on both sides;
- mixed frame rates; **vertical clips** (they will crop hard in a horizontal or 4:3 frame).

## 3. Cut
Follow `rough-cut` for what to keep (by word index) and `vlog-pacing` for how much air to leave. Clips with no speech are B-roll: follow `broll`. A subagent ("story editor") is a good fit: give it the video name and the skills; it writes the keep-list and the markers and runs the planner.

## 4. Build
Follow `resolve-scripting`. Order inside the build:
1. footage into the footage bin;
2. copy the template timeline into the timelines bin as "<video> - Transcript cut" (v2, v3… never overwrite) and empty the copy (it keeps the track FX chain);
3. set a custom frame if asked (e.g. 4:3 2880x2160, footage *scaled to fill with crop*);
4. lay the cut on V1/A1, alternate jump-cut zoom, colour B-roll pieces green;
5. grade (log footage only);
6. markers for spoken notes (pink);
7. **audio treatment last**: Normalize Audio Level on A1 (see `voice-and-audio`).

## 5. Report and stop
Short: timeline name, raw → cut length, number of pieces, each retake removed (timestamp + a few words, translated if needed), each marker and what goes there, punch-ins, B-roll placed, anything guessed or unsure. Then stop. They watch it.

## Follow-ups (they speak in plain words)

| They say | You do |
|---|---|
| "put back X", "cut 02:14 to 02:20" | edit the keep-list, re-plan, rebuild as v2 |
| "too choppy / pops" | loosen pauses (see `vlog-pacing`), give scenes room, rebuild |
| "add music" | `music-and-sound` |
| "captions" | `captions` |
| "graphics / overlays" | `motion-overlays` |
| "my voice sounds bad" | `voice-and-audio` |
| "export settings?" | `youtube-export` |
| "always …" | change the global default, and add a dated line to CLAUDE.md |

They will often fix things by hand in the timeline you built (trims, deleted clips). **Always re-read the timeline from Resolve before the next step** (B-roll positions, what they deleted) and never put back what they removed.


## VAS installation notes

This is the `edit-video` skill by appariciojunior ([@appariciojunior](https://github.com/appariciojunior)),
from [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills/tree/6709678d7d5b169149e13480428e12b0f09a47f0),
upstream revision `6709678d7d5b169149e13480428e12b0f09a47f0`.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
The full license text is preserved in the bundled LICENSE file.
You MAY use, copy, share, and adapt these skills for free with attribution and a link back.
You may NOT sell them or use them in anything sold without permission from the author.
No endorsement by the author is implied.

VAS canonical ID and installed folder: `edit-video`.
Standalone payload includes `SKILL.md` and `LICENSE`.
External documentation and tool links remain live references, not bundled snapshots.

Use the VAS website's Copy Agent Prompt or `./vas install edit-video --target <agent> --mode copy`
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
