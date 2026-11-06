# Voiceover pipeline

## Script format (`script/voiceover.txt`)
One line per scene, parsed by `vo.py`:
```
[S04] (0:22.3-0:33.4)  A skill is just a folder with one instruction file: ...   | 38
```
- The window is where the line *starts* and roughly ends. The scene end in `vo.py` (`SCENE_END`) is the hard limit.
- Below the lines, write an **ON-SCREEN TEXT** block per scene: every command, path and label. That is the build spec for the scenes.
- Add recording notes: stressed words, the pause across the drop, the target wpm.

## Draft voice (until the real recording exists)
- `vo.py` generates `audio/vo/vo_SXX.wav` with edge-tts (`en-US-AndrewMultilingualNeural`) **only if the file is missing**. It records the hash, so `--force-tts` regenerates only its own takes, never a student recording.
- Rate is one constant (`'+11%'` ≈ 160 wpm). Spoken forms differ from written: `SKILL.md` → "skill dot M D", an em dash → comma.
- Word timings come from edge-tts word boundaries (draft) or are spread by syllable weight over the detected speech (real recordings).
- `vo.json` holds, per line: `at` (placement), `onset`, `offset`, `words[{w, t0, t1}]` in absolute seconds. The picture reads cues from it (`vs()` in `timeline.ts`) and captions highlight the spoken word.

## Fitting lines to scenes
1. Generate the drafts and print each line's speech length.
2. Scene length = 0.3 s lead + speech + 0.4–0.8 s tail, rounded to the 0.5 s beat grid; keep the drop on a bar line.
3. Write the new scene table into both `timeline.ts` (`SCENE`) and `vo.py` (`SCENE_START`/`SCENE_END`), and update the windows in the script.
4. Re-run `vo.py`. There must be no "past its scene end" warnings.

## Real voice / voice clone hand-off
When the user wants their own voice but has little time, hand a coding agent a brief like this:
- Record a clean reference (3–5 min, quiet room, 48 kHz).
- Compare zero-shot models (IndexTTS2, F5-TTS, CosyVoice) with a fine-tune (GPT-SoVITS), 8 takes per line.
- Score each take on WER (faster-whisper), speaker similarity (ECAPA / WavLM-SV) and MOS (UTMOS), plus fit to the scene window. Shortlist the top 3 per line on a local listening page, and let the user pick.
- Deliver `audio/vo_clone/final/vo_SXX.wav` (48 kHz, −20 LUFS, 0.15 s silence each side) and `words.json`.
- Server rules (paths, non-interactive commands) and access restrictions go into the brief verbatim.

Then drop the files into `audio/vo/`, run `vo.py`, rebuild sound, re-render. Captions, cues and mascot lip-sync follow automatically.
