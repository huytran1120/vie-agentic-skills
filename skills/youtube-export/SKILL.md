---
name: youtube-export
description: DaVinci Resolve Deliver settings for great YouTube quality without 25 GB files - bitrate, profile, audio, burned-in subtitles and the colour tags that stop the "faded on YouTube" look. Use when the creator asks about export or render settings.
category: media
risk: safe
author: appariciojunior
license: CC-BY-NC-4.0
source_repo: appariciojunior/video-editor-skills
---

# YouTube export (Deliver page)

"Quality: Automatic" with H.264 picked ~300 Mb/s: **25 GB for an 11-minute video**. YouTube re-encodes everything; anything far above its recommendation is wasted upload time.

## Video
- Format **QuickTime**, codec **H.264** (hardware acceleration on, Network Optimization on).
- Resolution and frame rate: **timeline**.
- Quality: **Restrict to 50,000 Kb/s** for 4K-class frames (≈4.2 GB for 11 min). 40,000 is fine too (≈3.3 GB). Smaller: **H.265 at ~30,000** (≈2.5 GB) at the same quality.
- Encoding profile **High**, **Multi-pass** on (if available), key frames Automatic.

## Colour tags (check the project first)
Read the project's timeline colour space. If the project is **Rec.709-A** (common on Macs), set Color Space Tag and Gamma Tag to **Same as Project**. Tagging Rec.709 / Gamma 2.4 makes the video look lighter and washed out on Macs, iPhones and Chrome compared with the Resolve viewer. Data levels Auto; don't retain sub-black/super-white.

## Audio
AAC, **320 kb/s**, 48 kHz.

## Subtitles
If the creator wants captions always visible (people watching on mute): Subtitle Settings → Export Subtitle, Format **Burn into video**, **tick the subtitle track** (if it's unticked, nothing is exported). Optionally also export the SRT and upload it to YouTube as closed captions.

## File
Output to the workspace's `export edited video/` folder. Then save all of this into their preset ("…" → Update preset) so every export is one click.


## VAS installation notes

This is the `youtube-export` skill by appariciojunior ([@appariciojunior](https://github.com/appariciojunior)),
from [appariciojunior/video-editor-skills](https://github.com/appariciojunior/video-editor-skills/tree/6709678d7d5b169149e13480428e12b0f09a47f0),
upstream revision `6709678d7d5b169149e13480428e12b0f09a47f0`.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
The full license text is preserved in the bundled LICENSE file.
You MAY use, copy, share, and adapt these skills for free with attribution and a link back.
You may NOT sell them or use them in anything sold without permission from the author.
No endorsement by the author is implied.

VAS canonical ID and installed folder: `youtube-export`.
Standalone payload includes `SKILL.md` and `LICENSE`.
External documentation and tool links remain live references, not bundled snapshots.

Use the VAS website's Copy Agent Prompt or `./vas install youtube-export --target <agent> --mode copy`
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
