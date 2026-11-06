// The presenter: an original turtle mascot (sprites in public/mascot, generated with Codex for this
// film). Every frame is a blend of at most two neighbouring sprites, so nothing pops:
//  - mouth: visemes from the letters of each VO word, spread over the word's timing (3 f crossfade)
//  - idle: types on the laptop, blinks through a half-closed lid
//  - gestures: wave / point / cheer play as in-between sequences (in -> loop -> out)
//  - movement: timed moves along a hop arc with squash & stretch; facing turns through scaleX = 0
import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from 'remotion';
import { a, C } from './brand/tokens';
import { CUE, FPS, SCENE, TOTAL, VO_LINES } from './timeline';
import { clamp, EZ, mix, p } from './ui';

const SPRITES = ['closed', 'half', 'open', 'ee', 'oo', 'wide', 'fv', 'blink_half', 'blink', 'type_a', 'type_b', 'point_half', 'point', 'wave_a', 'wave', 'wave_b', 'wave_c', 'cheer_half', 'cheer'] as const;
type S = (typeof SPRITES)[number];
type Mix = Partial<Record<S, number>>;

// ---------------------------------------------------------------------------------------------
// mouth: letters -> visemes
// ---------------------------------------------------------------------------------------------
const visemesOf = (word: string): S[] => {
  const w = word.toLowerCase().replace(/[^a-z]/g, '');
  const out: S[] = [];
  for (const ch of w) {
    const v: S | null = /[a]/.test(ch) ? 'wide' : /[eiy]/.test(ch) ? 'ee' : /[ou]/.test(ch) ? 'oo' : /[mbp]/.test(ch) ? 'closed' : /[fv]/.test(ch) ? 'fv' : null;
    const s = v ?? 'half';
    if (out[out.length - 1] !== s) out.push(s);
  }
  if (!out.length) out.push('half');
  if (out.length > 1 && out[out.length - 1] === 'half') out.pop();
  return out;
};
type Seg = { a: number; b: number; v: S };
const MOUTH: Seg[] = (() => {
  const segs: Seg[] = [];
  for (const l of VO_LINES)
    for (const w of l.words) {
      const vs = visemesOf(w.w);
      const a0 = w.t0 * FPS;
      const d = Math.max(4, (w.t1 - w.t0) * FPS);
      vs.forEach((v, i) => segs.push({ a: a0 + (d * i) / vs.length, b: a0 + (d * (i + 1)) / vs.length, v: v === 'wide' && i % 2 ? 'open' : v }));
    }
  return segs.sort((x, y) => x.a - y.a);
})();
const mouthAt = (f: number): { v: S; prev: S; t: number } | null => {
  let i = MOUTH.findIndex((s) => f >= s.a && f < s.b + 3);
  if (i < 0) return null;
  // a short gap between words closes the mouth
  while (i + 1 < MOUTH.length && MOUTH[i + 1].a <= f) i++;
  const s = MOUTH[i];
  if (f >= s.b + 3) return null;
  const prev = i > 0 && s.a - MOUTH[i - 1].b < 4 ? MOUTH[i - 1].v : 'closed';
  return { v: s.v, prev, t: clamp((f - s.a) / 3) };
};

// ---------------------------------------------------------------------------------------------
// gestures as sequences
// ---------------------------------------------------------------------------------------------
type G = { at: number; dur: number; kind: 'wave' | 'point' | 'cheer' };
const GESTURES: G[] = [
  { at: SCENE.s03.from + 40, dur: 80, kind: 'wave' },
  { at: CUE.s04Home, dur: 80, kind: 'point' },
  { at: CUE.s05Expand, dur: 70, kind: 'point' },
  { at: CUE.s06Cmd1, dur: 70, kind: 'point' },
  { at: CUE.s07Freeze, dur: 80, kind: 'point' },
  { at: SCENE.s10.from + 40, dur: 70, kind: 'wave' },
  { at: CUE.s10Trigger, dur: 70, kind: 'point' },
  { at: CUE.s11Team, dur: 70, kind: 'cheer' },
  { at: CUE.s12Mail, dur: CUE.s12Stop - CUE.s12Mail, kind: 'wave' },
  { at: CUE.s12Vote, dur: TOTAL - CUE.s12Vote, kind: 'cheer' },
];
const blend = (x: S, y: S, t: number): Mix => (x === y ? { [x]: 1 } : { [x]: 1 - t, [y]: t });
/** A looping sequence with crossfades: each step `step` frames, `xf` frames of blend. */
const loop = (seq: S[], f: number, step: number, xf = 3): Mix => {
  const i = Math.floor(f / step);
  const u = f - i * step;
  const cur = seq[i % seq.length];
  const prev = seq[(i - 1 + seq.length) % seq.length];
  return i === 0 ? { [cur]: 1 } : blend(prev, cur, clamp(u / xf));
};
const gestureMix = (g: G, f: number): Mix => {
  const t = f - g.at;
  const left = g.at + g.dur - f;
  const IN = 6;
  if (g.kind === 'point') {
    if (t < IN) return blend('point_half', 'point_half', 1);
    if (t < IN + 4) return blend('point_half', 'point', (t - IN) / 4);
    if (left < IN + 4 && left >= IN) return blend('point', 'point_half', 1 - (left - IN) / 4);
    if (left < IN) return { point_half: 1 };
    return { point: 1 };
  }
  if (g.kind === 'wave') {
    if (t < IN) return { wave_a: 1 };
    if (left < IN) return { wave_a: 1 };
    return loop(['wave', 'wave_b', 'wave', 'wave_c'], t - IN, 7);
  }
  // cheer
  if (t < IN) return { cheer_half: 1 };
  if (t < IN + 4) return blend('cheer_half', 'cheer', (t - IN) / 4);
  if (left < IN) return { cheer_half: 1 };
  return loop(['cheer', 'cheer', 'cheer_half'], t - IN - 4, 10, 4);
};
/** How far into a gesture we are, for the cross-fade from/to the body pose (0..1). */
const gestureWeight = (g: G, f: number) => clamp((f - g.at + 4) / 4) * clamp((g.at + g.dur - f + 4) / 4);

const bodyMix = (f: number): Mix => {
  const m = mouthAt(f);
  if (m) return blend(m.prev, m.v, m.t);
  // idle: type, and blink every ~3.3 s
  const bt = f % 200;
  if (bt < 12) {
    const k = bt < 3 ? ['closed', 'blink_half', bt / 3] : bt < 6 ? ['blink_half', 'blink', (bt - 3) / 3] : bt < 9 ? ['blink', 'blink_half', (bt - 6) / 3] : ['blink_half', 'closed', (bt - 9) / 3];
    return blend(k[0] as S, k[1] as S, k[2] as number);
  }
  // typing only after a pause of 30 f in the voice
  const lastWord = MOUTH.filter((s) => s.b <= f).pop();
  const nextWord = MOUTH.find((s) => s.a > f);
  if ((!lastWord || f - lastWord.b > 30) && (!nextWord || nextWord.a - f > 12)) return loop(['type_a', 'type_b'], f, 9, 4);
  return { closed: 1 };
};

const frameMix = (f: number): Mix => {
  const g = GESTURES.find((x) => f >= x.at - 4 && f < x.at + x.dur + 4);
  const body = bodyMix(f);
  if (!g) return body;
  const w = gestureWeight(g, f);
  const gm = gestureMix(g, Math.min(Math.max(f, g.at), g.at + g.dur - 1));
  const out: Mix = {};
  for (const [k, v] of Object.entries(body)) out[k as S] = (out[k as S] ?? 0) + (v as number) * (1 - w);
  for (const [k, v] of Object.entries(gm)) out[k as S] = (out[k as S] ?? 0) + (v as number) * w;
  return out;
};

// ---------------------------------------------------------------------------------------------
// movement: timed moves (x, y = centre of the 1:1 sprite box), hop arcs, turns
// ---------------------------------------------------------------------------------------------
type St = { x: number; y: number; s: number; face: number };
type Move = { at: number; dur: number } & St;
const HOME: St = { x: 1765, y: 940, s: 270, face: 1 };
const OFF: St = { ...HOME, x: 2160 };
const MOVES: Move[] = [
  { at: SCENE.s03.from + 10, dur: 40, ...HOME },
  { at: CUE.s03Grid - 10, dur: 36, x: 1735, y: 600, s: 270, face: -1 },
  { at: SCENE.s04.from + 6, dur: 34, ...HOME },
  { at: CUE.s04Home - 34, dur: 30, x: 1805, y: 640, s: 260, face: -1 },
  { at: CUE.s04Home + 90, dur: 32, ...HOME, face: -1 },
  { at: SCENE.s05.from + 20, dur: 30, ...HOME, x: 1785, face: 1 },
  { at: CUE.s05Expand - 20, dur: 20, ...HOME, x: 1785, face: -1 },
  { at: SCENE.s06.from + 10, dur: 30, ...HOME, face: 1 },
  { at: CUE.s06Cmd1 - 20, dur: 20, ...HOME, face: -1 },
  { at: CUE.s06Step2 + 40, dur: 24, ...HOME, face: 1 },
  { at: CUE.s07Freeze - 30, dur: 24, ...HOME, face: -1 },
  { at: CUE.s07FreezeEnd + 80, dur: 34, ...HOME, face: 1 },
  { at: SCENE.s08.from - 30, dur: 30, ...OFF },
  { at: SCENE.s10.from + 4, dur: 2, ...OFF },
  { at: SCENE.s10.from + 10, dur: 40, ...HOME },
  { at: CUE.s10Trigger - 20, dur: 20, ...HOME, face: -1 },
  { at: SCENE.s11.from + 4, dur: 34, x: 1735, y: 780, s: 270, face: -1 },
  { at: SCENE.s12.from - 30, dur: 30, ...OFF, y: 780 },
  { at: CUE.s12Mail - 30, dur: 2, ...OFF },
  { at: CUE.s12Mail - 24, dur: 36, x: 1730, y: 930, s: 270, face: -1 },
  { at: CUE.s12Vote - 8, dur: 30, x: 1690, y: 690, s: 430, face: -1 },
];
const stateAt = (f: number): St & { hop: number; fx: number } => {
  let st: St = OFF;
  let hop = 0;
  let fx = OFF.face;
  for (const m of MOVES) {
    if (f < m.at) break;
    const u = clamp((f - m.at) / m.dur);
    const e = EZ.cam(u);
    const dist = Math.hypot(m.x - st.x, m.y - st.y);
    const from = st;
    st = { x: mix(from.x, m.x, e), y: mix(from.y, m.y, e), s: mix(from.s, m.s, e), face: m.face };
    fx = m.face;
    hop = 0;
    if (u < 1) {
      hop = dist > 30 ? Math.sin(Math.PI * u) * Math.min(90, 30 + dist * 0.18) : 0;
      if (from.face !== m.face) fx = from.face * Math.cos(Math.PI * EZ.cam(u)); // turns through 0
      else fx = m.face;
    }
  }
  return { ...st, hop, fx };
};
const VISIBLE: [number, number][] = [
  [SCENE.s03.from + 10, SCENE.s08.from],
  [SCENE.s10.from + 10, SCENE.s12.from],
  [CUE.s12Mail - 24, TOTAL],
];

export const Mascot: React.FC = () => {
  const f = useCurrentFrame();
  if (!VISIBLE.some(([s, e]) => f >= s && f < e)) return null;
  const st = stateAt(f);
  const fade = 1 - p(f, CUE.s12Fade, CUE.s12Fade + 50);
  const mixw = frameMix(f);
  const speaking = !!mouthAt(f);
  // squash & stretch: stretch in the air, squash on take-off and landing
  const air = st.hop > 0 ? Math.sin(Math.PI * clamp(st.hop / 90)) : 0;
  const sy = 1 + 0.07 * air + 0.012 * Math.sin(f / 13) + (speaking ? 0.008 * Math.sin(f / 3) : 0);
  const sx = (1 - 0.05 * air) * st.fx;
  const bob = Math.sin(f / 24) * 3;
  const shadowK = 1 - clamp(st.hop / 120) * 0.6;
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', opacity: fade }}>
      <div style={{ position: 'absolute', left: st.x - st.s / 2, top: st.y - st.s / 2, width: st.s, height: st.s }}>
        <div style={{ position: 'absolute', left: '24%', right: '24%', bottom: '11%', height: '7%', borderRadius: '50%', background: `radial-gradient(ellipse, ${a(C.black, 0.45 * shadowK)}, ${a(C.black, 0)} 70%)`, transform: `scaleX(${0.7 + 0.3 * shadowK})` }} />
        <div style={{ position: 'absolute', inset: 0, transformOrigin: '50% 88%', transform: `translateY(${bob - st.hop}px) scale(${sx}, ${sy})` }}>
          {(() => {
            // composite so the weights add up to a fully opaque turtle: the heaviest sprite is drawn
            // opaque at the bottom, each layer above gets w / (sum of weights so far)
            const order = SPRITES.filter((q) => (mixw[q] ?? 0) > 0.001).sort((x, y) => (mixw[y] ?? 0) - (mixw[x] ?? 0));
            const op: Partial<Record<S, number>> = {};
            let W = 0;
            order.forEach((q, i) => {
              W += mixw[q] ?? 0;
              op[q] = i === 0 ? 1 : (mixw[q] ?? 0) / W;
            });
            const z = (q: S) => order.indexOf(q);
            return SPRITES.map((q) => (
              <Img key={q} src={staticFile(`mascot/${q}.png`)} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: op[q] ?? 0, zIndex: z(q) < 0 ? 0 : z(q) + 1, filter: `drop-shadow(0 0 16px ${a(C.cyan, 0.2)})` }} />
            ));
          })()}
        </div>
      </div>
    </AbsoluteFill>
  );
};
