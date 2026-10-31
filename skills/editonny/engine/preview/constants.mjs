export const POLL_MS = 1500;
export const TAB_HASH = { cut: '#cut', style: '#style', final: '#final' };
export const HASH_TAB = { '#cut': 'cut', '#style': 'style', '#final': 'final' };
export const PHASE_TAB = { setup: 'cut', cut: 'cut', style: 'style', final: 'final' };
export const PHASE_LABEL = { setup: 'Setup', cut: 'Cut', style: 'Style', final: 'Final' };
export const AWAIT_TAB = { approval_cut: 'cut', style: 'style', approval_final: 'final' };
export const SWATCHES = ['#FFC400', '#FF6B35', '#FF3D7F', '#39D98A', '#3DA9FC', '#FFFFFF'];
export const DENOISE = [
  { id: 'off', label: 'Off', desc: 'Original recorded sound.' },
  { id: 'light', label: 'Light', desc: 'Reduce hiss and hum while preserving the voice.' },
  { id: 'strong', label: 'Strong', desc: 'For loud street or fan noise.' },
];
export const DENOISE_IDS = DENOISE.map((d) => d.id);
// edit_data "motion": how many animations the agent picks and their look
export const MOTION_COUNTS = [
  { id: 'few', n: 3, label: 'Few', desc: 'The 2 or 3 strongest speech moments.' },
  { id: 'some', n: 5, label: 'Some', desc: 'Up to 5, spread across the video.' },
];
// sw = the look's colors (base, highlight, text); null = the accent chosen for the video
export const MOTION_THEMES = [
  { id: 'paper', label: 'Lilac paper', desc: 'Light paper with lilac accents.', sw: ['#c7b7ef', '#665080', '#352c40'] },
  { id: 'bluePaper', label: 'Blue paper', desc: 'Light paper with blue accents and checks.', sw: ['#a9c7f2', '#2457c5', '#1f2a44'] },
  { id: 'greenPaper', label: 'Mint paper', desc: 'Light paper with mint accents.', sw: ['#a8dcc0', '#1f8a5b', '#1e3a2f'] },
  { id: 'orangePaper', label: 'Orange paper', desc: 'Light paper with peach and orange accents.', sw: ['#f6c29b', '#e0591f', '#3d2a1e'] },
  { id: 'graphitePaper', label: 'Graphite paper', desc: 'Light paper with gray and brick-red accents.', sw: ['#c9ccd1', '#d6452b', '#1d1f23'] },
  { id: 'pop', label: 'Pop', desc: 'Cream card with a thick black outline and hard shadow.', sw: ['#fff8e7', '#e8412c', '#111111'] },
  { id: 'neon', label: 'Neon', desc: 'Dark card with a glowing border and condensed type.', sw: ['#0a0a12', '#22d3ee', '#ffffff'] },
  { id: 'dark', label: 'Dark glass', desc: 'Dark card using the video accent color.', sw: ['#121214', null, '#ffffff'] },
  { id: 'light', label: 'White', desc: 'White card using the video accent color.', sw: ['#ffffff', null, '#111111'] },
];
export const MOTION_COUNT_IDS = MOTION_COUNTS.map((x) => x.id);
export const MOTION_THEME_IDS = MOTION_THEMES.map((x) => x.id);
export const MUSIC_OFF = 'off';
export const MUSIC_FILE = 'file';
export const MUSIC_ASK = ''; // music on, source not chosen yet (older saves, or "music": {"enabled": true} alone)
export const MUSIC_POLL_MS = 10000;
export const MOOD_ID_RE = /^[a-z0-9][a-z0-9_]{0,39}$/;
export const TV_ID = 'greenScreen';
export const TV_POSITIONS = [
  { id: 'left', label: 'Bottom left', desc: 'You at the bottom left.' },
  { id: 'right', label: 'Bottom right', desc: 'You at the bottom right.' },
  { id: 'center', label: 'Center', desc: 'You larger, at the bottom center.' },
];
export const TV_POS_IDS = TV_POSITIONS.map((x) => x.id);
export const TV_POS_DEFAULT = 'right';
export const slugify = (text) => String(text || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
  .replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 40).replace(/_+$/, '');
export const baseName = (rel) => String(rel || '').split('/').pop();
export const CHECK_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>';
export const TRASH_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';
