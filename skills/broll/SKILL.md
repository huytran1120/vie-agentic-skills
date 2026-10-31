---
name: broll
description: How to find, watch and cut B-roll in a vlog - clips with no speech placed by time between talking clips, chosen by their action and story, not a fixed length. Use when footage mixes talking clips (A-roll) and silent clips, or when the creator says the B-roll pacing feels wrong.
category: media
risk: safe
author: appariciojunior
license: CC-BY-NC-4.0
source_repo: appariciojunior/video-editor-skills
---

# B-roll

A transcript-only cut silently drops every clip without words. Don't.

## Spot it
- A clip with **0 words** is B-roll.
- A clip whose "words" are **song lyrics or another language** (radio, a café) is B-roll too: check what the transcript says before treating it as speech.
- All clips recorded in sequence → keep the recorded order; B-roll sits where it was shot.

## Watch it (the step people skip)
Pulling 5 frames per clip led to bad cuts. **Look at 2 frames per second** (a contact sheet, 8 per row, small) for every B-roll clip, and read what the creator says right before and after it. Questions:
- What is the action? Where does it start and resolve?
- Is there a natural transition? Example from a real edit: the camera goes *into* a backpack (frames go black) in one clip, and the next clip starts black and comes *out* of the bag onto an airport table. Cutting black-to-black makes a free, perfect transition; cutting by fixed length destroyed it.
- Which part is steady and well framed? Which part is out of focus or the operator fumbling?
- Is it vertical (phone held upright)? It will crop to the middle in a horizontal/4:3 frame: flag it.

## Cut it
- Segment by time: `{"clip": "…", "broll": true, "in": s, "out": s, "why": "…"}`.
- Length follows the action: a quick cutaway 2–4 s, a transition sequence 6–8 s, an outro over a drive 10–15 s. A soft-focus shot gets the shortest slot.
- 100% framing, colour the timeline pieces green so A/B roll read at a glance.
- Natural sound stays on the voice track, but: a B-roll clip that is **silent** gets normalized up by +30 dB (pure hiss) → set it back to 0 dB; a clip with a **radio/music** in it fights the music bed → lower it 8 dB or so.
- The music rises on B-roll (see `music-and-sound`).

## Report
Each B-roll: timeline time, what it shows, why that range, anything flagged (vertical, soft focus).


## VAS installation notes

This is the `broll` skill by appariciojunior ([@appariciojunior](https://github.com/appariciojunior)),
from [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills/tree/6709678d7d5b169149e13480428e12b0f09a47f0),
upstream revision `6709678d7d5b169149e13480428e12b0f09a47f0`.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
The full license text is preserved in the bundled LICENSE file.
You MAY use, copy, share, and adapt these skills for free with attribution and a link back.
You may NOT sell them or use them in anything sold without permission from the author.
No endorsement by the author is implied.

VAS canonical ID and installed folder: `broll`.
Standalone payload includes `SKILL.md` and `LICENSE`.
External documentation and tool links remain live references, not bundled snapshots.

Use the VAS website's Copy Agent Prompt or `./vas install broll --target <agent> --mode copy`
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
