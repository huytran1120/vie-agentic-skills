// Real screen recordings (shotlist_for_student.md). Drop the files into film/public/clips/ and the
// matching scene plays them instead of its RECONSTRUCTED mockup. `start` is the second in the clip
// that the scene's first frame shows, `rate` the playback speed (the speed badge stays on screen).
import { getStaticFiles } from 'remotion';

export type Clip = { file: string; start: number; rate: number };
export const CLIPS = {
  A: { file: 'clips/clipA.mp4', start: 0, rate: 1 }, // S06: npx skills add ... and ls
  B1: { file: 'clips/clipB.mp4', start: 0, rate: 1 }, // S07: typing the prompt, the skill loading
  B2: { file: 'clips/clipB.mp4', start: 60, rate: 16 }, // S08: the render progress
  C: { file: 'clips/clipC.mp4', start: 0, rate: 6 }, // S10 right: /lab-report in the toy project
} satisfies Record<string, Clip>;

export const hasClip = (c: Clip) => getStaticFiles().some((s) => s.name === c.file);

/**
 * Wall-clock seconds the full motion-blurred render of this film took (S08 timer: "<real> -> 12 s").
 * Must be the measured number: 295 s on an 18-core Mac, 2026-11-05 (v2.4 cut with the mascot, wall clock of
 * the three segment renders 16:13:46 -> 16:18:41, out/render_time_v24.txt; S09 renders with --concurrency=1).
 * null shows a dash.
 */
export const RENDER_SECONDS: number | null = 295;
