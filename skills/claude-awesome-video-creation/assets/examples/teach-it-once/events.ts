// Exports every sound event of the film (in seconds) to out/events.json for scripts/soundtrack.py.
// The frames come from the same timeline and schedule the picture uses, never typed by hand.
// Run: npx tsx scripts/events.ts
import { mkdirSync, writeFileSync } from 'node:fs';
import { S04_LABELS } from '../src/scenes/Explain';
import { S05_SEG_AT } from '../src/scenes/Explain';
import { S11_NODE_AT } from '../src/scenes/Close';
import { S06_OUT_AT } from '../src/scenes/Demo';
import { S01_KEYS, S06_KEYS, S07_CARDS, S07_FAST, S07_KEYS, S10_ASK_KEYS, S10_LINES, S10_MKDIR_KEYS, S10_RUN_KEYS } from '../src/schedule';
import { BEAT, CUE, FPS, SCENE, TOTAL, VO_LINES } from '../src/timeline';

type Ev = { t: number; kind: string; gain?: number; pan?: number; dur?: number };
const ev: Ev[] = [];
const s = (f: number) => f / FPS;
const add = (f: number, kind: string, gain = 1, pan = 0, dur?: number) => ev.push({ t: s(f), kind, gain, pan, dur });

// typing
S01_KEYS.forEach((f, i) => add(f, 'key', 0.8, -0.1 + 0.2 * ((i * 7) % 5) / 4));
S06_KEYS.forEach((f) => add(f, 'key', 0.55));
S10_MKDIR_KEYS.forEach((f) => add(f, 'key', 0.35, -0.3));
S10_RUN_KEYS.forEach((f) => add(f, 'key', 0.35, 0.4));
S07_KEYS.filter((f) => f < S07_FAST).forEach((f) => add(f, 'key', 0.45));
S10_ASK_KEYS.forEach((f) => add(f, 'key', 0.35, 0.4));
// S01
add(CUE.s01Enter, 'thock', 1.2);
add(CUE.s01Enter, 'burst', 0.7);
add(CUE.s01Enter, 'sub', 1.0);
// S02
add(CUE.s02Serif - 6, 'whoosh', 0.7, 0, 0.5);
add(CUE.s02Serif + 36 + 48, 'ting', 0.6);
// S03
[CUE.s03Words, CUE.s03Slides, CUE.s03Data].forEach((f, i) => add(f, 'rim', 0.9, [-0.2, 0.2, 0][i]));
[0, 1, 2].forEach((i) => add(CUE.s03Again + i * BEAT, 'stutter', 0.8 + 0.1 * i));
add(CUE.s03Grid, 'swell', 0.6, 0, 1.4);
// S04
add(CUE.s04Folder, 'unfold', 0.7, 0, 0.4);
[0, 1, 2, 3].forEach((i) => add(CUE.s04Tree + i * 6, 'tick', 0.5, -0.3));
S04_LABELS.forEach((l) => add(l.cue - 4, 'scratch', 0.5, 0.4));
add(CUE.s04Home, 'tick', 0.5, -0.2);
add(CUE.s04Home + 14, 'tick', 0.45, -0.2);
add(CUE.s04Share, 'ping', 0.45, 0.2);
// S05
add(CUE.s05Scan - 30, 'ping', 0.6, -0.3);
add(CUE.s05Expand, 'latch', 0.9, -0.2);
[0, 1, 2, 3, 4, 5, 6, 7].forEach((i) => add(S05_SEG_AT(i), 'bloop', 0.35, 0.3));
add(CUE.s05Expand + 10, 'bloop', 0.6, 0.3);
add(CUE.s05Extra, 'ping', 0.5, 0.3);
// S06
[0, 1, 2, 3, 4].forEach((i) => add(S06_OUT_AT(i), 'tick', 0.3));
add(CUE.s06Done, 'ding', 0.7, 0.4);
add(CUE.s06Step1, 'latch', 0.6, -0.4);
add(CUE.s06Step2 - 10, 'latch', 0.6, 0.4);
[CUE.s06Cmd1, CUE.s06Cmd1 + 18, CUE.s06Cmd3].forEach((f) => add(f, 'tick', 0.45, -0.4));
// S07
add(CUE.s07Freeze, 'tapestop', 0.8);
S07_CARDS.forEach((f, i) => add(f, 'whoosh', 0.45, i % 2 === 0 ? -0.6 : 0.6, 0.45));
// S08: a riser all the way into the drop (the music drops out for the last beat, the riser does not)
add(SCENE.s08.from + 30, 'whirr', 0.5, 0, s(CUE.drop - SCENE.s08.from - 30));
add(CUE.s08Black, 'swell', 0.7, 0, s(CUE.drop - CUE.s08Black));
// S09
add(CUE.drop, 'boom', 1.2);
add(CUE.s09Now, 'ting', 0.7);
// S10
add(CUE.s10Trigger, 'ping', 0.5, -0.2);
S10_LINES.forEach((f) => add(f, 'tick', 0.45, -0.3));
add(CUE.s10Save, 'thock', 0.9);
add(CUE.s10Save, 'tick', 0.6);
// S11
[0, 1, 2, 3, 4, 5].forEach((i) => add(S11_NODE_AT(i), 'pluck', 0.4, -0.5 + i * 0.2));
add(CUE.s11Ring2, 'shimmer', 0.5, 0, 1.6);
// S12
add(CUE.s12Once, 'thock', 1.1);
add(CUE.s12Vote, 'ding', 0.8, 0);
add(CUE.s12Vote, 'shimmer', 0.7, 0, 1.8);
add(CUE.s12Vote - 4, 'whoosh', 0.5, 0, 0.4);
// designed transitions (src/scenes): one whoosh each, apex on the cut
add(SCENE.s03.from, 'whoosh', 0.8, 0, 0.6); // S02 zoom-through
add(SCENE.s05.from, 'whoosh', 0.7, -0.5, 0.45); // S04 -> S05 whip
add(SCENE.s07.from, 'whoosh', 0.6, 0, 0.55); // S06 push into the window
add(SCENE.s08.from, 'whoosh', 0.7, -0.5, 0.45); // S07 -> S08 whip
add(SCENE.s11.from, 'whoosh', 0.5, 0, 0.5); // S10 folds into the folder
add(SCENE.s12.from, 'whoosh', 0.4, 0, 0.5); // S11 converges

const out = {
  fps: FPS,
  total: TOTAL / FPS,
  cue: Object.fromEntries(Object.entries(CUE).map(([k, v]) => [k, v / FPS])),
  scene: Object.fromEntries(Object.entries(SCENE).map(([k, v]) => [k, { from: v.from / FPS, dur: v.dur / FPS }])),
  vo: VO_LINES.map((l) => ({ id: l.id, file: l.file, at: l.at, onset: l.onset })),
  events: ev.sort((a, b) => a.t - b.t),
};
mkdirSync('out', { recursive: true });
writeFileSync('out/events.json', JSON.stringify(out, null, 1));
console.log(`events.json: ${ev.length} events`);
