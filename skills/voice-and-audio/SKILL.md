---
name: voice-and-audio
description: Voice treatment for creator videos in DaVinci Resolve - loudness normalization, diagnosing a muffled or "underwater" voice from the spectrum, Voice Isolation, an EQ recipe, and fixing clips that normalization made worse. Use when building the timeline's audio step or when the creator says their voice sounds bad.
category: media
risk: safe
author: appariciojunior
license: CC-BY-NC-4.0
source_repo: appariciojunior/video-editor-skills
---

# Voice and audio

## Always, as the last build step
Normalize Audio Level on every voice-track piece:
- mode **ITU-R BS.1770-4**, target level **-2.0 dBTP**, target loudness **-16 LKFS**, set level **Independent**.
- Check the result line ("normalized N pieces"); if it fails, give the creator these values to do by hand (select A1 → Normalize Audio Levels).

## After normalizing, check for side effects
- A **silent** clip (B-roll with no sound) gets boosted up to +30 dB → hiss. Set it back to 0 dB.
- A B-roll clip with **music/radio** in it will fight the music bed: pull it down ~8 dB.

## "My voice sounds muffled / underwater"
Measure before touching anything:
1. **Phase check:** are left and right identical (true dual mono)? Compute L−R. If two different mics are summed (camera mic + lav), comb filtering causes exactly this sound: use one channel only.
2. **Spectrum:** compare band levels of a 20 s talking section: below 300 Hz, around 1 kHz, above 3 kHz, above 6 kHz. A clean voice has its 3 kHz+ band roughly 10–15 dB below the total; we measured **~22 dB** below with most energy under 300 Hz → the mic was covered (under a jacket) or badly placed.

## Fix (most of it is EQ, which is not scriptable)
- Scriptable: **Voice Isolation 50** per talking clip (cleans room and noise; leave B-roll alone so its natural sound stays).
- By hand (Inspector → Audio → EQ on one clip, then Paste Attributes with **only Equalizer ticked**, never Volume, so the normalize gains survive):
  - high-pass 80 Hz
  - −3 dB at 250 Hz, Q ~1.2 (boom)
  - +3 dB at 3.5 kHz, Q ~1 (presence)
  - +2 dB high shelf at 10 kHz (air)
- Ask before driving the UI with computer-use; the creator may prefer to do it.

## Prevention (tell the creator once)
Clip the lav on the outside of clothing, 15–20 cm below the chin; in stereo-mode receivers with one transmitter the voice is on one channel only.


## VAS installation notes

This is the `voice-and-audio` skill by appariciojunior ([@appariciojunior](https://github.com/appariciojunior)),
from [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills/tree/6709678d7d5b169149e13480428e12b0f09a47f0),
upstream revision `6709678d7d5b169149e13480428e12b0f09a47f0`.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
The full license text is preserved in the bundled LICENSE file.
You MAY use, copy, share, and adapt these skills for free with attribution and a link back.
You may NOT sell them or use them in anything sold without permission from the author.
No endorsement by the author is implied.

VAS canonical ID and installed folder: `voice-and-audio`.
Standalone payload includes `SKILL.md` and `LICENSE`.
External documentation and tool links remain live references, not bundled snapshots.

Use the VAS website's Copy Agent Prompt or `./vas install voice-and-audio --target <agent> --mode copy`
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
