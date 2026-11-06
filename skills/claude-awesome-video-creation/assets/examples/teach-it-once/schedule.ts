// Discrete timing shared by picture (src/scenes) and sound (scripts/events.ts -> soundtrack.py).
// No React here: Node loads it through tsx. All frames are absolute film frames at 60 fps.
import { CUE, FPS, PROMPT_SHORT, S06_CMD_TEXT } from './timeline';

/** Deterministic pseudo-random in [0,1). */
export const rnd = (seed: number | string) => {
  const s = String(seed);
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  h ^= h >>> 16;
  h = Math.imul(h, 2246822507);
  h ^= h >>> 13;
  return (h >>> 0) / 4294967296;
};

/** Frames at which each character of `text` appears when typed at `cps` from `start`. */
export const typeTimes = (text: string, start: number, cps: number, seed: string) => {
  const out: number[] = [];
  let t = start;
  for (let i = 0; i < text.length; i++) {
    out.push(Math.round(t));
    t += (FPS / cps) * (0.75 + 0.5 * rnd(`${seed}${i}`));
  }
  return out;
};
/** Characters visible at frame f, given typeTimes. */
export const typed = (times: number[], f: number) => {
  let n = 0;
  while (n < times.length && times[n] <= f) n++;
  return n;
};

// S01: the cold-open prompt (without the "> " which is drawn as the prompt glyph).
export const S01_TEXT = PROMPT_SHORT.replace(/^> /, '');
export const S01_KEYS = typeTimes(S01_TEXT, CUE.s01Type, 28, 's01');

// S06: the skill install command (reconstructed Clip A), STEP 2.
export const S06_CMD = S06_CMD_TEXT;
export const S06_KEYS = typeTimes(S06_CMD, CUE.s06Type, 34, 's06');

// S07: the full prompt. First sentence in real time, the rest at 16x (badge on screen).
export const PROMPT_FULL =
  'make a launch video about agent skills. Use the claude-awesome-video-creation skill. Follow script/storyboard.md, script/design_system.md and script/voiceover.txt exactly. Write all scenes in React, compose original music and sound effects in code, add captions from the voiceover, place my vo_*.wav files at each scene start, and render 1920x1080 60fps. Keep it under 1:55.';
export const S07_SPLIT = PROMPT_FULL.indexOf('.') + 1;
const s07a = typeTimes(PROMPT_FULL.slice(0, S07_SPLIT), CUE.s07TypeAt, 28, 's07a');
const s07aEnd = s07a[s07a.length - 1] + 4;
const s07b = typeTimes(PROMPT_FULL.slice(S07_SPLIT), s07aEnd, 26 * 16, 's07b');
export const S07_KEYS = [...s07a, ...s07b];
export const S07_FAST = s07aEnd; // the 16x badge shows from here ...
export const S07_ENTER = s07b[s07b.length - 1] + 6; // ... until the prompt is submitted

// S10: the mkdir line, then SKILL.md: frontmatter on "name", the description on "description",
// the four steps on "steps"; then /skills and /lab-report are typed in the session on the right.
export const S10_MKDIR = 'mkdir -p .claude/skills/lab-report';
export const S10_MKDIR_KEYS = typeTimes(S10_MKDIR, CUE.s10Mkdir, 40, 's10m');
export const S10_LINES = [CUE.s10Line1, CUE.s10Line1 + 10, CUE.s10Desc, CUE.s10Desc + 30, CUE.s10Desc + 56, CUE.s10Steps, CUE.s10Steps + 12, CUE.s10Steps + 24, CUE.s10Steps + 36];
/** Frames each SKILL.md line takes to type. */
export const S10_LINE_DUR = [8, 14, 26, 22, 8, 14, 18, 16, 14];
export const S10_ASK = '/skills';
export const S10_ASK_KEYS = typeTimes(S10_ASK, CUE.s10Ten, 20, 's10');
export const S10_RUN = '/lab-report';
export const S10_RUN_KEYS = typeTimes(S10_RUN, CUE.s10One, 22, 's10r');

/** Real filenames this project's pipeline wrote (they fly out of the terminal in S07). */
export const S07_FILES = ['timeline.ts', 'Open.tsx', 'Captions.tsx', 'soundtrack.py', 'Demo.tsx']; // storyboard, React, captions, music, code
export const S07_CARDS = [CUE.s07Card0, CUE.s07Card1, CUE.s07Card2, CUE.s07Card3, CUE.s07Card4];

const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#%&*+=<>/';
/** Characters cycle through random glyphs, then lock left to right. */
export const scramble = (text: string, f: number, at: number, per = 2.2, spin = 10) =>
  text
    .split('')
    .map((ch, i) => {
      const lock = at + spin + i * per;
      if (f < at + i * 0.6) return ' ';
      if (f >= lock || ch === ' ') return ch;
      return GLYPHS[Math.floor(rnd(`${i}:${Math.floor(f / 2)}`) * GLYPHS.length)];
    })
    .join('');

