// Burned-in captions from the voiceover's word timings (src/generated/vo.json). Chunks of at most
// ~42 characters, cut at punctuation where possible; the word being spoken is drawn in ember.
import React from 'react';
import { useCurrentFrame } from 'remotion';
import { a, C } from './brand/tokens';
import { FPS, SCENE, VO_LINES } from './timeline';
import { sans } from './ui';

type W = { w: string; t0: number; t1: number };
type Chunk = { words: W[]; from: number; to: number };

const MAX = 42;
export const CHUNKS: Chunk[] = (() => {
  const out: Chunk[] = [];
  const len = (ws: W[]) => ws.map((x) => x.w).join(' ').length;
  /** Split a run of words into pieces of at most MAX characters, as evenly as possible. */
  const balance = (ws: W[]): W[][] => {
    if (len(ws) <= MAX) return [ws];
    const parts = Math.ceil(len(ws) / MAX);
    const target = len(ws) / parts;
    const res: W[][] = [];
    let cur: W[] = [];
    for (const w of ws) {
      if (cur.length && len([...cur, w]) > target + 4 && res.length < parts - 1) {
        res.push(cur);
        cur = [];
      }
      cur.push(w);
    }
    res.push(cur);
    return res.flatMap((r) => (len(r) > MAX ? balance(r) : [r]));
  };
  for (const line of VO_LINES) {
    // phrases end at punctuation; merge short neighbours up to MAX, balance long ones
    const phrases: W[][] = [];
    let cur: W[] = [];
    // the take's word list drops the script's dashes: put them back after the word they follow
    const toks = line.text.split(/\s+/);
    const norm = (x: string) => x.toLowerCase().replace(/[^a-z0-9]/g, '');
    let ti = 0;
    const words = line.words.map((w) => {
      while (ti < toks.length && norm(toks[ti]) !== norm(w.w)) ti++;
      const dash = toks[ti + 1] === '—' || toks[ti + 1] === '–';
      ti++;
      return dash ? { ...w, w: `${w.w} —` } : w;
    });
    for (const w of words) {
      cur.push(w);
      if (/[.,:;!?…—]$/.test(w.w)) {
        phrases.push(cur);
        cur = [];
      }
    }
    if (cur.length) phrases.push(cur);
    let acc: W[] = [];
    const push = (ws: W[]) => out.push({ words: ws, from: ws[0].t0, to: ws[ws.length - 1].t1 });
    for (const ph of phrases) {
      if (acc.length && len([...acc, ...ph]) <= MAX) acc = [...acc, ...ph];
      else {
        if (acc.length) balance(acc).forEach(push);
        acc = ph;
      }
    }
    if (acc.length) balance(acc).forEach(push);
  }
  // hold each chunk until the next one starts (or 0.5 s after its last word)
  for (let i = 0; i < out.length; i++) {
    const next = out[i + 1];
    out[i].to = Math.min(out[i].to + 0.5, next ? Math.max(out[i].to, next.from - 0.05) : out[i].to + 0.5);
  }
  return out;
})();

export const Captions: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  // S09 carries its own kinetic type, synced to the voice: no caption pill over it
  if (f >= SCENE.s09.from && f < SCENE.s09.from + SCENE.s09.dur) return null;
  const c = CHUNKS.find((x) => t >= x.from - 0.08 && t < x.to);
  if (!c) return null;
  const o = Math.min(1, (t - (c.from - 0.08)) / 0.1) * Math.min(1, (c.to - t) / 0.1);
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: 72, display: 'flex', justifyContent: 'center', opacity: o, pointerEvents: 'none' }}>
      <div style={{ background: a(C.ink, 0.7), borderRadius: 12, padding: '12px 24px', ...sans(40, 500), whiteSpace: 'pre', letterSpacing: '-0.005em' }}>
        {c.words.map((w, i) => (
          <span key={i} style={{ color: t >= w.t0 && t < w.t1 + 0.05 ? C.ember : C.text }}>
            {w.w}
            {i < c.words.length - 1 ? ' ' : ''}
          </span>
        ))}
      </div>
    </div>
  );
};
