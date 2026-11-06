---
name: claude-awesome-video-creation
description: "Make a complete, follow-along tutorial or explainer video from code with Claude Code. Use it whenever someone wants a demo video, tool walkthrough, course or assignment video, 'how to use X' explainer, launch film or feature showcase built with Remotion (React). The skill covers script and voiceover (draft TTS or a cloned voice, with word timings), a beat-locked timeline that drives picture, captions and an original code-made soundtrack, macOS-style glass terminals with syntax colour, an animated mascot presenter with lip-sync, segmented rendering that avoids headless-Chrome hangs, and measured QA (frozen-frame scan, contact sheets, loudness)."
category: media
tags: ["video", "remotion", "react", "tutorial", "video-creation", "voiceover", "motion-graphics", "claude-code"]
risk: safe
author: "SHI Haochen (HaochenSHI66)"
license: "MIT"
source_repo: "HaochenSHI66/claude-awesome-video-creation"
source_revision: "4b0f8d89d50046ac13003e95bcde081e328c2373"
source_path: "skills/claude-awesome-video-creation/SKILL.md"
---


# claude-awesome-video-creation

You are making a video someone will **learn from and act on**, not just admire. The viewer should be able to pause it, copy what is on screen and do it on their own computer. Craft (motion, sound, colour) serves that goal.

This skill extends **cinetic** (Leonxlnx, MIT). The full cinetic craft guide is in `references/cinetic-core.md` and still applies: one timeline file, beat grid, motion blur, a code-made score, and measuring before you call anything done. What this skill adds is a **tutorial mode**, a **mascot presenter**, a **voiceover pipeline**, a **render-and-QA recipe that survives heavy scenes**, and a **rule list distilled from real feedback** (`references/lessons.md`).

## 0. Decide the mode first

| Mode | Use when | Length | Pace | Look |
|---|---|---|---|---|
| **Tutorial** (default here) | the viewer must reproduce something: install a tool, use a feature, write a config | 90–120 s | VO about 160 wpm, every scene has 0.3–0.6 s slack, no dead air | colourful, high contrast, glass terminals, step chips |
| **Launch film** | pure showcase, no follow-along | 20–45 s | cinetic calm or crisp profile | follow cinetic's hard bans |

In tutorial mode some cinetic bans are lifted *on purpose*, because a student audience asked for "colourful, fancy, Mac-like": multi-hue accents, a serif payoff word, a light glass look on windows, and confetti on the call to action are all allowed. Keep the other discipline: one idea per scene, no filler text, everything eased and smooth.

## 1. The follow-along structure (tutorial mode)

Use this order. Each scene answers one question the viewer would ask next.

1. **Hook** (≤ 6 s): the end result or a surprising claim. Example: "This whole video came from one prompt and one skill."
2. **What it is** (≤ 7 s): the tool and the feature, plus one plain subtitle saying what the tool does.
3. **The problem** (≤ 9 s): pick examples from the audience's own life. For students: lab reports, slides, reference lists, not "data cleaning".
4. **How it works** (≤ 12 s each, at most 2 scenes): the real file layout and real paths on screen, each part labelled. Explain mechanisms in plain words ("an instruction file"), and show the filename (SKILL.md) next to the plain word, never alone.
5. **Try it: STEP 1/2/3** (about 10–12 s each): every command appears in full on screen *while* the voice says it:
   - one colour per step (cyan, violet, lime);
   - install commands for macOS/Linux **and** Windows;
   - the account or plan requirement as small print.
6. **The real run**: the prompt being typed, the moment the skill loads (freeze-frame plus callout: "matched by its description"), then sped up with a speed badge.
7. **Proof / reveal**: for example, "…is the video you're watching right now." Keep it short (≤ 5 s), and keep the two halves of a sentence that spans a cut within about 1.2 s of each other.
8. **Make your own**: the whole minimal file, readable on screen for at least 4 s, with labels hanging off the key lines ("the trigger: say WHEN").
9. **Share it**: commit the folder; the open standard and its link.
10. **Cheat sheet** (hold ≥ 5 s): every command and path from the video, numbered, so the viewer can pause and copy.
11. **"This is just the basics"**: what else the feature can do, as pills grouped "CAN" and "FOR STUDY", plus the author's contact.
12. **Tagline, then call to action** (vote, like, star) and the credit line. The credit line must be honest (§6).

Write `script/voiceover.txt` first (format in `references/voiceover.md`), get it approved, then build. Script changes are cheap; render changes are not.

## 2. Timeline and voice drive everything

- `src/timeline.ts` is the single source of time. Scenes are given in **seconds** on a 120 BPM grid (1 beat = 30 frames at 60 fps), and the drop sits on a bar line.
- `scripts/vo.py` turns the script into per-line takes. It uses edge-tts drafts until the real recording exists and never overwrites a recording. It writes `src/generated/vo.json` with word-level timings.
- **Every cue comes from a spoken word**: `vs('s05', 'loads')` gives the frame of that word, snapped to an 8th note and clamped inside its scene, and it throws if the word is missing. Re-recording a line moves its animation with it. Never hand-type cue frames that answer a word.
- Pace: draft TTS at `+11%` is about 160 wpm. If a line overruns its scene, re-split the scene lengths from the measured speech (scene = 0.3 s lead + speech + 0.4–0.8 s) rather than squeezing the voice.

## 3. Look (tutorial mode defaults)

Tokens live in one file (`brand/tokens.ts`); see `references/look-tutorial.md`.
- **Stage:** deep navy `#081024`, plus an **aurora** of three slow radial lights (cyan, violet, ember) blended with `screen`. Not flat black.
- **Windows:** macOS style:
  - 12 px radius, 38 px title bar with the title centred;
  - traffic lights with a soft highlight;
  - a hairline rim and a layered shadow so the window clearly separates from the stage;
  - a light **fake glass** body: a translucent Cobalt2-blue `#193549` gradient plus a diagonal sheen. **Never use real `backdrop-filter`**: in nested scenes it hangs the renderer.
- **Terminal text:** a zsh `%` prompt (`PS>` for the Windows line), with syntax colours from `<Sh>`:
  - commands cyan, flags gold, URLs and paths violet, strings pink, operators muted.
- **Transcript lines** (`● Read(…)`) are coloured by verb: Read cyan, Write violet, Bash gold, Edit pink, Skill ember.
- **Step chips:** solid colour pills with a glow. Labels and stages are colour-coded so each idea has its own hue.

## 4. Mascot presenter (optional, recommended for student audiences)

Pipeline in `references/mascot.md`. In short:
1. **Design:** design an **original** character. Never a franchise character, not even fan art of one: it breaks copyright and "all content must be your own" rules. Iterate on outfit and props from text prompts; do not feed an IP image as a reference.
2. **Frames:** lock one base image on a flat magenta `#FF00FF` background with about 15% margin. Make every other frame an **edit of the base** ("keep everything identical, only change X"), so mouth swaps don't jitter. The frame set:
   - 7 visemes: closed, half, open, ee, oo, wide, fv;
   - blink: half-closed and closed;
   - 2 typing frames;
   - gesture in-betweens: wave a/b/c, point half, cheer half.
3. **Keying:** `scripts/key_magenta.py <in> <out> --nocrop` (distance alpha plus magenta despill, same canvas for every frame). Check the silhouette IoU against the base: mouths ≥ 0.99, gestures ≥ 0.9.
4. **Animation:** see `assets/examples/teach-it-once/Mascot.tsx`.
   - **Lip-sync:** visemes come from the letters of each VO word, with a 3-frame crossfade between shapes.
   - **Idle:** typing when there is no speech; blinks pass through the half-closed lid.
   - **Gestures:** each plays as in, loop, out.
   - **Moves:** timed moves along a hop arc with squash and stretch; facing turns through `scaleX = 0`.
   - **Compositing:** composite blends so the result stays opaque (bottom sprite at 1, each layer above at `w / Σw`). A plain 50/50 opacity blend turns the character semi-transparent, which reads as flicker.
5. **Staying out of the way:** park it where no content or caption sits, hide it for the climax, bring it back for the contact and call-to-action moments. Credit it honestly ("Turtle mascot: original, generated with Codex").

## 5. Render and QA (do not skip)

Recipe in `references/render-qa.md`.
- **Render in segments:** `scripts/render_segments.sh Film out/final.mp4 "0-4439:8 4440-4739:1 4740-6839:8" public/audio/soundtrack.wav`. Any heavy nested 3D or blur scene gets `--concurrency=1`. With 8 tabs, headless Chrome's GPU process can deadlock silently: progress stops at a fixed frame and the log shows no error. Fix this instead of waiting.
- **No dead air:** never hold full black plus full silence. Viewers read it as the video buffering. Use a suck-in (zoom, brighten, blur) and keep a riser going into the drop.
- **Measured numbers:** an on-screen "render time" must be the **measured** wall-clock time of this cut. Re-render the segment that shows it after measuring.
- **QA gates on every cut:**
  1. `scripts/check_static.py out/final.mp4` finds no frozen runs ≥ 0.1 s, unless they are intended;
  2. `scripts/sheet.sh` contact sheets cover every scene: look for overflowing text, overlaps with captions or the mascot, and anything mid-scramble;
  3. ffprobe confirms the frame count and duration;
  4. loudness is −14 LUFS integrated with true peak ≤ −1 dBTP.
- **Fast preview:** `--props='{"mb":0}' --scale=0.5 --concurrency=2`, then single `remotion still` frames to check fixes.

## 6. Honesty rules

- Any mockup terminal carries a small `RECONSTRUCTED` label until the real screen recording replaces it (`footage.ts` swaps clips in automatically).
- The credit says "Voice: draft TTS" while the voice is synthetic.
- AI-generated assets are credited as such.
- The description says the film was built over several prompts, not one.
- Verify every command and path shown on screen against the tool's official docs on the day you build. Never quote install commands from memory.

## 7. Working with the user

The user steers by short messages ("faster", "more colourful", "the terminal should look like a Mac"). For each message:
1. restate the change as concrete parameters;
2. apply it everywhere it matters (script, timeline, scenes, sound);
3. preview and check;
4. render;
5. report what changed and what is still a draft.

`references/lessons.md` lists every such request from the original session and the rule it became. Read it before your first film.

## Files

- `references/lessons.md`: feedback turned into rules (read first)
- `references/voiceover.md`: script format, TTS drafts, voice-clone hand-off, word timings
- `references/look-tutorial.md`: palette, glass windows, syntax colours, chips, aurora
- `references/mascot.md`: original mascot pipeline, prompts, keying, lip-sync, motion
- `references/render-qa.md`: segmented render, timer honesty, QA gates
- `references/cinetic-core.md` and the other `references/*.md`: the inherited cinetic craft guide
- `scripts/`: `render_segments.sh`, `check_static.py`, `sheet.sh`, `key_magenta.py`, plus cinetic's scripts
- `assets/examples/teach-it-once/`: the complete source of the film this skill was built with (timeline, scenes, mascot, sound, VO script)

---

## VAS installation notes

- Canonical ID: `claude-awesome-video-creation`
- Source repository: [`HaochenSHI66/claude-awesome-video-creation`](https://github.com/HaochenSHI66/claude-awesome-video-creation) at commit `4b0f8d89d50046ac13003e95bcde081e328c2373` (`skills/claude-awesome-video-creation/SKILL.md`).
- License: MIT (Copyright (c) 2026 SHI Haochen (HaochenSHI66); Copyright (c) 2026 Leonxlnx (cinetic, which this skill is built on)); see `LICENSE` and `NOTICE.md`.
- Bundled references, scripts, and assets: 25 reference guides in `references/`, 31 helper scripts in `scripts/`, and full worked example/starters in `assets/`.
- Install via CLI: `./vas install claude-awesome-video-creation --target <agent> --mode link` (or `--mode copy`).
