// Shared picture pieces: easing helpers, the stage texture (grain, vignette, key light), window
// chrome, the reconstructed-terminal mockup, badges and type helpers. Everything is a pure function
// of the frame.
import React from 'react';
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from 'remotion';
import { a, C, FONT } from './brand/tokens';

export const EZ = {
  out: Easing.bezier(0.16, 1, 0.3, 1),
  in: Easing.bezier(0.7, 0, 0.84, 0),
  cam: Easing.bezier(0.65, 0, 0.35, 1),
  smooth: Easing.bezier(0.45, 0, 0.55, 1),
  lin: (t: number) => t,
};

export const clamp = (v: number, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, v));
/** Clamped 0..1 progress between two frames. */
export const p = (f: number, from: number, to: number, ease = EZ.out) =>
  interpolate(f, [from, Math.max(from + 0.001, to)], [0, 1], { easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
export const mix = (x: number, y: number, t: number) => x + (y - x) * t;
export const lmix = (x: number, y: number, t: number) => Math.exp(mix(Math.log(x), Math.log(y), t));

/** Standard entrance (design_system.md): opacity 0->1, y +dy->0, blur 8->0, 36 f expo-out. */
export const enter = (f: number, at: number, dur = 36, dy = 12, blur = 8): React.CSSProperties => {
  const t = p(f, at, at + dur);
  return {
    opacity: clamp(t * 1.4),
    transform: `translateY(${(1 - t) * dy}px)`,
    filter: blur ? `blur(${blur * clamp(1 - t / 0.6)}px)` : undefined,
  };
};
/** Standard exit: opacity ->0, blur ->24 px, 24 f expo-in. Returns multipliers. */
export const exitK = (f: number, at: number, dur = 24) => {
  const t = p(f, at, at + dur, EZ.in);
  return { o: 1 - t, blur: 24 * t };
};
/** Combine an entrance and an exit. */
export const inOut = (f: number, at: number, out: number, dur = 36, dy = 12): React.CSSProperties => {
  const e = enter(f, at, dur, dy);
  const x = exitK(f, out);
  const eb = parseFloat(String(e.filter ?? 'blur(0px)').replace(/[^0-9.]/g, '')) || 0;
  return { ...e, opacity: (e.opacity as number) * x.o, filter: `blur(${eb + x.blur}px)` };
};

/** Pulse envelope (attack 2 f, decay tau 5 f). */
export const pulse = (t: number, attack = 2, tau = 5) =>
  t <= 0 ? 0 : t < attack ? Math.sin((t / attack) * (Math.PI / 2)) : Math.exp(-(t - attack) / tau);

// ---------------------------------------------------------------------------------------------
// Type
// ---------------------------------------------------------------------------------------------
export const sans = (size: number, weight = 500): React.CSSProperties => ({
  fontFamily: FONT.text,
  fontSize: size,
  fontWeight: weight,
  letterSpacing: size >= 80 ? '-0.03em' : '-0.01em',
  lineHeight: 1.05,
  whiteSpace: 'pre',
  color: C.text,
});
export const serif = (size: number): React.CSSProperties => ({
  fontFamily: FONT.serif,
  fontStyle: 'italic',
  fontWeight: 400,
  fontSize: size,
  letterSpacing: '-0.02em',
  lineHeight: 1.0,
  whiteSpace: 'pre',
  color: C.text,
});
export const mono = (size: number, weight = 400): React.CSSProperties => ({
  fontFamily: FONT.mono,
  fontSize: size,
  fontWeight: weight,
  lineHeight: 1.4,
  whiteSpace: 'pre',
  fontVariantNumeric: 'tabular-nums',
  fontFeatureSettings: '"calt" 0, "liga" 0',
  color: C.text,
});
export const glow = (k = 1) => `0 0 24px ${a(C.ember, 0.45 * k)}, 0 0 80px ${a(C.ember, 0.18 * k)}`;
/** JetBrains Mono advance width. */
export const MONO_ADV = 0.6;

/** Text centred on (x, y). */
export const Center: React.FC<{ x?: number; y: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ x = 960, y, style, children }) => (
  <div style={{ position: 'absolute', left: x, top: y, transform: 'translate(-50%, -50%)', ...style }}>{children}</div>
);

// ---------------------------------------------------------------------------------------------
// Stage texture
// ---------------------------------------------------------------------------------------------
/** Full-frame film grain, reseeded every 2 frames (opacity 0.045, overlay). */
export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  const seed = Math.floor(f / 2) % 997;
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', mixBlendMode: 'overlay', opacity: 0.045 * 2.2 }}>
      <svg width={1920} height={1080}>
        <filter id={`g${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency={0.9} numOctaves={2} seed={seed} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#g${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};
export const Vignette: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: 'none', background: `radial-gradient(ellipse at center, ${a(C.black, 0)} 60%, ${a(C.black, 0.45)} 100%)` }} />
);
/** Aurora: three soft coloured lights (cyan, violet, ember) drifting behind the content. */
export const KeyLight: React.FC<{ strength?: number }> = ({ strength = 1 }) => {
  const f = useCurrentFrame();
  const t = f / 600;
  const blob = (hex: string, phase: number, rx: number, ry: number, r: number, k: number) => {
    const x = 960 + Math.cos((t + phase) * Math.PI * 2) * rx;
    const y = 540 + Math.sin((t * 0.8 + phase) * Math.PI * 2) * ry;
    return `radial-gradient(circle ${r}px at ${x}px ${y}px, ${a(hex, k * strength)}, ${a(hex, 0)} 100%)`;
  };
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        background: [blob(C.cyan, 0, 620, 260, 760, 0.09), blob(C.violet, 0.37, 560, 300, 820, 0.1), blob(C.ember, 0.71, 420, 200, 640, 0.08)].join(', '),
        mixBlendMode: 'screen',
      }}
    />
  );
};


// ---------------------------------------------------------------------------------------------
// Windows, terminals, chips
// ---------------------------------------------------------------------------------------------
export const Win: React.FC<{ w: number; h: number; title?: string; style?: React.CSSProperties; children?: React.ReactNode; bar?: boolean }> = ({
  w,
  h,
  title,
  style,
  children,
  bar = true,
}) => (
  <div
    style={{
      position: 'absolute',
      width: w,
      height: h,
      // a macOS window with a light glass look: translucent blue, a diagonal sheen, a hairline rim
      background: `linear-gradient(135deg, ${a(C.flash, 0.09)} 0%, ${a(C.flash, 0.02)} 28%, ${a(C.flash, 0)} 50%), linear-gradient(180deg, ${a(C.term, 0.92)}, ${a(C.term, 0.82)})`,
      borderRadius: 12,
      border: `1px solid ${a(C.flash, 0.16)}`,
      boxShadow: `0 0 0 1px ${a(C.black, 0.5)}, 0 34px 90px ${a(C.black, 0.55)}, 0 12px 30px ${a(C.black, 0.35)}, 0 0 70px ${a(C.cyan, 0.07)}`,
      overflow: 'hidden',
      ...style,
    }}
  >
    {bar && (
      <div style={{ position: 'relative', height: 38, display: 'flex', alignItems: 'center', padding: '0 14px', gap: 8, borderBottom: `1px solid ${a(C.black, 0.35)}`, boxShadow: `inset 0 1px 0 ${a(C.flash, 0.14)}`, background: `linear-gradient(180deg, ${a(C.flash, 0.1)}, ${a(C.termBar, 0.55)})` }}>
        {[C.dotR, C.dotY, C.dotG].map((c, i) => (
          <div key={i} style={{ width: 12, height: 12, borderRadius: 6, background: `radial-gradient(circle at 50% 35%, ${a(C.flash, 0.35)}, ${c} 55%)`, boxShadow: `inset 0 0 0 0.5px ${a(C.black, 0.35)}` }} />
        ))}
        {title && <div style={{ position: 'absolute', left: 80, right: 80, top: 0, height: 38, display: 'flex', alignItems: 'center', justifyContent: 'center', ...sans(15, 500), color: a(C.text, 0.62), overflow: 'hidden' }}>{title}</div>}
      </div>
    )}
    <div style={{ position: 'relative', width: '100%', height: bar ? h - 38 : h }}>{children}</div>
  </div>
);

/** The honesty label every mockup terminal carries (storyboard: RECONSTRUCTED, Mono 14, 40%). */
export const Recon: React.FC<{ style?: React.CSSProperties }> = ({ style }) => (
  <div style={{ position: 'absolute', left: 20, bottom: 14, ...mono(14, 600), color: a(C.text, 0.4), letterSpacing: '0.12em', ...style }}>RECONSTRUCTED</div>
);

/** Speed badge (4x, 8x, 16x): Mono 20 muted on a surface pill, top-left. */
export const Badge: React.FC<{ text: string; opacity?: number; style?: React.CSSProperties }> = ({ text, opacity = 1, style }) => (
  <div
    style={{
      position: 'absolute',
      left: 96,
      top: 72,
      padding: '6px 14px',
      borderRadius: 999,
      background: C.surface,
      border: `1px solid ${C.line}`,
      ...mono(20, 600),
      color: C.muted,
      opacity,
      ...style,
    }}
  >
    {text}
  </div>
);

export const Chip: React.FC<{ text: string; color?: string; style?: React.CSSProperties; size?: number }> = ({ text, color = C.muted, style, size = 22 }) => (
  <div
    style={{
      position: 'absolute',
      padding: '8px 16px',
      borderRadius: 10,
      background: C.surface,
      border: `1px solid ${C.line}`,
      ...mono(size, 600),
      color,
      ...style,
    }}
  >
    {text}
  </div>
);

/** A block caret. */
export const Caret: React.FC<{ on: boolean; h: number; w?: number; style?: React.CSSProperties }> = ({ on, h, w, style }) => (
  <span style={{ display: 'inline-block', width: w ?? h * 0.55, height: h, background: C.ember, opacity: on ? 1 : 0, verticalAlign: 'middle', ...style }} />
);

/** A 2 px line-drawn folder glyph. */
export const FolderGlyph: React.FC<{ size: number; color?: string; draw?: number }> = ({ size, color = C.ember, draw = 1 }) => {
  const len = 420;
  return (
    <svg width={size} height={size * 0.8} viewBox="0 0 120 96" fill="none">
      <path
        d="M6 18 V84 a6 6 0 0 0 6 6 H108 a6 6 0 0 0 6 -6 V30 a6 6 0 0 0 -6 -6 H54 L44 12 H12 a6 6 0 0 0 -6 6 Z"
        stroke={color}
        strokeWidth={2.4}
        strokeLinejoin="round"
        strokeDasharray={len}
        strokeDashoffset={len * (1 - draw)}
      />
    </svg>
  );
};

// ---------------------------------------------------------------------------------------------
// Premium motion primitives
// ---------------------------------------------------------------------------------------------
/**
 * Words rise out of a mask, one after another (expo-out), the way title cards are set in film.
 * `accent` words (by index) arrive in ember and relax to `color` over 30 f.
 */
export const Rise: React.FC<{
  text: string;
  f: number;
  at: number;
  style: React.CSSProperties;
  stagger?: number;
  dur?: number;
  accent?: number[];
  color?: string;
  out?: number;
  /** Extra style per word (e.g. sheen(), which must sit on the element that owns the text). */
  word?: (i: number) => React.CSSProperties;
}> = ({ text, f, at, style, stagger = 5, dur = 34, accent = [], color, out, word }) => {
  const words = text.split(' ');
  const ex = out === undefined ? 0 : p(f, out, out + 22, EZ.in);
  return (
    <span style={{ display: 'inline-flex', gap: '0.26em', ...style, whiteSpace: 'nowrap' }}>
      {words.map((w, i) => {
        const t = p(f, at + i * stagger, at + i * stagger + dur);
        const relax = p(f, at + i * stagger + dur * 0.6, at + i * stagger + dur * 0.6 + 30, EZ.smooth);
        const isAcc = accent.includes(i);
        const c = isAcc ? `color-mix(in srgb, ${C.ember} ${Math.round((1 - relax) * 100)}%, ${color ?? C.text})` : undefined;
        return (
          <span key={i} style={{ display: 'inline-block', overflow: 'hidden', padding: '0.08em 0.06em 0.18em', margin: '-0.08em -0.06em -0.18em' }}>
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${(1 - t) * 105 - ex * 105}%) rotate(${(1 - t) * 4}deg)`,
                transformOrigin: '0 100%',
                color: c ?? color,
                ...(word ? word(i) : {}),
              }}
            >
              {w}
            </span>
          </span>
        );
      })}
    </span>
  );
};

/** A light sheen sweeping once across text (background-clip: text), from frame `at` over `dur`. */
export const sheen = (f: number, at: number, dur = 50, base: string = C.text, hi: string = '#FFFFFF'): React.CSSProperties => {
  const t = p(f, at, at + dur, EZ.cam);
  const x = mix(-40, 140, t);
  return {
    backgroundImage: `linear-gradient(105deg, ${base} ${x - 18}%, ${hi} ${x}%, ${base} ${x + 18}%)`,
    WebkitBackgroundClip: 'text',
    backgroundClip: 'text',
    color: 'transparent',
  };
};

/** Horizontal (directional) motion blur for whips: an SVG blur on the x axis only. */
export const HBlur: React.FC<{ px: number; id: string; children: React.ReactNode; style?: React.CSSProperties }> = ({ px, id, children, style }) => {
  const v = Math.round(px * 2) / 2;
  if (v <= 0.5) return <AbsoluteFill style={style}>{children}</AbsoluteFill>;
  return (
    <AbsoluteFill style={style}>
      <svg width={0} height={0} style={{ position: 'absolute' }}>
        <filter id={`${id}-${v}`} x="-20%" y="-5%" width="140%" height="110%">
          <feGaussianBlur stdDeviation={`${v} 0`} />
        </filter>
      </svg>
      <AbsoluteFill style={{ filter: `url(#${id}-${v})` }}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Window entrance in depth: tilted back and pushed away, it swings up into place. */
export const win3d = (f: number, at: number, dur = 48, tilt = 22): React.CSSProperties => {
  const t = p(f, at, at + dur);
  return {
    transform: `perspective(2200px) translateZ(${(1 - t) * -320}px) translateY(${(1 - t) * 120}px) rotateX(${(1 - t) * tilt}deg)`,
    opacity: clamp(t * 2.2),
    transformOrigin: '50% 100%',
  };
};

/** Whip transition progress: exit in the last `n` frames of a scene (0..1, accelerating). */
export const whipOut = (f: number, dur: number, n = 16) => p(f, dur - n, dur, EZ.in);
/** Whip entrance: the first `n` frames of a scene (1..0, decelerating). */
export const whipIn = (f: number, n = 20) => 1 - p(f, 0, n, EZ.out);

/** Shell syntax colours: prompt, command, flags, URLs, paths, strings, placeholders, operators. */
export const Sh: React.FC<{ text: string }> = ({ text }) => {
  const parts = text.split(/("[^"]*"|\s+)/);
  let cmdNext = true;
  return (
    <>
      {parts.map((tok, i) => {
        if (/^\s+$/.test(tok) || tok === '') return <span key={i}>{tok}</span>;
        let color: string = C.text;
        let weight: number | undefined;
        if (tok === '$' || tok === '>' || tok === '%' || tok === 'PS>') color = C.lime;
        else if (tok === '&&' || tok === '|') {
          color = C.muted;
          cmdNext = true;
          return <span key={i} style={{ color }}>{tok}</span>;
        } else if (cmdNext) {
          color = C.cyan;
          weight = 600;
          cmdNext = false;
        } else if (/^-/.test(tok)) color = C.gold;
        else if (/^https?:/.test(tok)) color = C.violet;
        else if (/^["']/.test(tok) || /["']$/.test(tok)) color = C.pink;
        else if (/^</.test(tok)) color = C.gold;
        else if (/[/~.]/.test(tok)) color = C.violet;
        if (tok === '$' || tok === '>' || tok === '%' || tok === 'PS>') cmdNext = true;
        return (
          <span key={i} style={{ color, fontWeight: weight }}>
            {tok}
          </span>
        );
      })}
    </>
  );
};
