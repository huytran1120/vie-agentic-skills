// Brand tokens for "Teach It Once": the only place a colour, face or type size is written down.
// Source: script/design_system.md (the approved, supplied brand). Scenes import these;
// scripts/lint-film.mjs fails any hex colour that is not declared here.
//
// cinetic:brand-supplied ember accent (#E07A50 terracotta family), ember-glow and ember-deep from design_system.md
// cinetic:brand-supplied Instrument Serif Italic as the payoff-word face (design_system.md "Emphasis serif")
// cinetic:brand-supplied ember glow on the payoff words (design_system.md "Texture: Ember glow")
import type React from 'react';
import { safeInsets } from '../lib/safe';
import { H, W } from '../timeline';

export const C = {
  // v2.1 palette: a deep navy stage, Cobalt2-style blue terminals, and a fuller accent set.
  ink: '#081024', // background, always (deep navy)
  surface: '#10224A', // cards and code boxes
  surface2: '#163061', // elevated cards, chips
  line: '#213B6E', // 1px borders, hairlines, leader lines
  line2: '#2D4C85', // hairlines that must survive downscaling (thumbnails, nested frames)
  text: '#EEF2FF', // primary type
  muted: '#93A4C8', // secondary type, line numbers, labels
  dim: '#5E719A', // tertiary: placeholder labels, inactive rows
  // terminal windows: the popular Cobalt2 blue
  term: '#193549',
  termBar: '#15232D',
  termLine: '#2A5878',
  dotR: '#FF5F57',
  dotY: '#FEBC2E',
  dotG: '#28C840',
  // accents
  ember: '#E07A50', // the brand accent: the skill, the payoff word
  emberGlow: '#FFB38A', // glow core and bloom highlights only
  emberDeep: '#2A1A12', // highlight fills behind code, selection
  cyan: '#5EE7FF', // commands, step 1, discovery
  violet: '#B48CFF', // paths, step 2, activation
  gold: '#FFC857', // flags, numbers, the description
  pink: '#FF6FA3', // strings, highlights
  lime: '#9BE564', // step 3, execution
  success: '#5BD69B', // check chips only
  flash: '#FFFFFF', // the two flashes (S01 enter, S09 drop)
  black: '#000000',
  paper: '#081024', // alias: the stage (cinetic components read C.paper)
  accent: '#E07A50', // alias of ember for the starter's fx/ and lib/ components
  mute: '#93A4C8', // alias of muted (starter components)
  white: '#FFFFFF', // alias of flash (starter components)
};

/** rgba() from a token hex, so alpha variants never become off-token literals. */
export const a = (hex: string, alpha: number) => {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${alpha})`;
};

export const FONT = {
  text: '"Geist Variable", "Geist", system-ui, sans-serif',
  mono: '"JetBrains Mono", ui-monospace, monospace',
  serif: '"Instrument Serif", "Geist Variable", sans-serif', // cinetic:brand-supplied Instrument Serif
};

/** Faces the FontGate waits for before anything renders or measures. */
export const FACES = [
  '500 16px "Geist Variable"',
  '600 16px "Geist Variable"',
  '400 16px "JetBrains Mono"',
  '600 16px "JetBrains Mono"',
  'italic 400 16px "Instrument Serif"', // cinetic:brand-supplied Instrument Serif Italic
];

/** Layout unit: 1 at 1080p. */
export const U = Math.min(W, H) / 1080;

// One token per role (design_system.md scale: 16 24 34 44 64 88 120 140 180).
export const TYPE = {
  hero: { size: 180, weight: 400, track: -0.02, lead: 1.0 }, // serif payoff, S02
  display: { size: 120, weight: 600, track: -0.03, lead: 1.0 }, // kinetic statements
  statement: { size: 88, weight: 600, track: -0.03, lead: 1.05 }, // end-card statement, overlays
  line: { size: 64, weight: 500, track: -0.02, lead: 1.1 }, // overlay lines
  secondary: { size: 56, weight: 500, track: -0.01, lead: 1.1 }, // "Claude Code" in S02
  caption: { size: 40, weight: 500, track: -0.005, lead: 1.25 }, // burned-in subtitles
  ui: { size: 24, weight: 500, track: -0.01, lead: 1.3 }, // smallest readable size on screen
};

/** CSS for a type role at a size (px). Tabular figures always. */
export const typeStyle = (role: keyof typeof TYPE, size = TYPE[role].size * U): React.CSSProperties => ({
  fontFamily: FONT.text,
  fontSize: size,
  fontWeight: TYPE[role].weight,
  letterSpacing: `${TYPE[role].track}em`,
  lineHeight: TYPE[role].lead,
  fontVariantNumeric: 'tabular-nums',
  whiteSpace: 'pre',
});

/** Serif italic payoff style. */
export const serifStyle = (size: number): React.CSSProperties => ({
  fontFamily: FONT.serif,
  fontStyle: 'italic', // cinetic:brand-supplied Instrument Serif Italic
  fontWeight: 400,
  fontSize: size,
  letterSpacing: '-0.02em',
  lineHeight: 1.0,
  whiteSpace: 'pre',
});

/** Mono style (code, terminal, timers, chips). */
export const monoStyle = (size: number, weight = 400): React.CSSProperties => ({
  fontFamily: FONT.mono,
  fontSize: size,
  fontWeight: weight,
  letterSpacing: '0em',
  lineHeight: 1.4,
  fontVariantNumeric: 'tabular-nums',
  fontFeatureSettings: '"calt" 0, "liga" 0',
  whiteSpace: 'pre',
});

/** Ember text glow (design_system.md), alpha scaled by k (pulse on the beat in S09-S12). */
export const emberGlow = (k = 1): string => // cinetic:brand-supplied ember glow
  `0 0 ${24}px ${a(C.ember, 0.45 * k)}, 0 0 ${80}px ${a(C.ember, 0.18 * k)}`; // cinetic:brand-supplied ember glow

/** Window / card shadow from the design system. */
export const SHADOW = `0 40px 120px ${a(C.black, 0.6)}, inset 0 1px 0 ${a(C.flash, 0.04)}`;

export const safeArea = (w: number, h: number) => {
  const i = safeInsets(undefined, w, h);
  return { x: Math.max(i.left, i.right), y: Math.max(i.top, i.bottom) };
};
/** Design-system safe margins: 96 px sides, 72 px top and bottom. */
export const SAFE = { x: 96, y: 72 };
