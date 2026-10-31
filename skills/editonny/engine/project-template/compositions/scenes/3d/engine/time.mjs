export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const mix = (a, b, p) => a + (b - a) * p;
export const smooth = (p) => { p = clamp(p); return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
export const easeOut = (p) => 1 - Math.pow(1 - clamp(p), 3);
export const interval = (t, start, dur, curve = smooth) => (dur <= 0 ? (t >= start ? 1 : 0) : curve(clamp((t - start) / dur)));

const normalizeWord = (s) => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
export function word(C, text, after = 0, standard = after) {
  const target = normalizeWord(text);
  const p = (C.words || []).find((w) => w.t >= after - 1e-3 && normalizeWord(w.text).startsWith(target));
  return p ? p.t : standard;
}
export function moment(C, m, standard = 0) {
  if (typeof m === 'number') return m;
  if (typeof m === 'string') return word(C, m, 0, standard);
  if (m && typeof m === 'object') {
    const after = m.after == null ? 0 : moment(C, m.after, 0);
    return word(C, m.word || '', after, m.standard == null ? standard : m.standard);
  }
  return standard;
}
