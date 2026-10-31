import { motionOn, normalizeHex } from '../dom.mjs';
import { DENOISE_IDS, MOOD_ID_RE, MOTION_COUNT_IDS, MOTION_THEME_IDS, MUSIC_ASK, MUSIC_FILE, MUSIC_OFF, TV_ID, TV_POS_DEFAULT, TV_POS_IDS, slugify } from '../constants.mjs';

export function basePicks(data, music = null) {
  const cat = data.catalog || {};
  const d = cat.defaults || {};
  const first = (list) => (list && list[0] ? list[0].id : null);
  const p = {
    edit_type: d.edit_type || first(cat.edit_types),
    caption_style: d.caption_style || first(cat.caption_styles),
    hook_style: d.hook_style || first(cat.hook_styles),
    accent: normalizeHex(d.accent) || '#FFC400',
    hook_text: '',
    cta_text: '',
    elements: {},
    denoise: 'off',
    music_mood: MUSIC_OFF,
    music_file: '',
    greenScreenPosition: TV_POS_DEFAULT,
    motionCount: 'few',
    motionTheme: 'paper',
    note: '',
  };
  (cat.elements || []).forEach((item) => { p.elements[item.id] = Boolean(item.default); });
  const ed = data.edit_data;
  if (ed && typeof ed === 'object') {
    if (normalizeHex(ed.accent)) p.accent = normalizeHex(ed.accent);
    if (ed.audio && ed.audio.enabled !== false && DENOISE_IDS.includes(ed.audio.denoise)) p.denoise = ed.audio.denoise;
    if (ed.hook) { if (ed.hook.style) p.hook_style = ed.hook.style; if (ed.hook.text) p.hook_text = ed.hook.text; }
    if (ed.captions && ed.captions.style) p.caption_style = ed.captions.style;
    if (ed.cta && ed.cta.text) p.cta_text = ed.cta.text;
    if (ed.edit_type === TV_ID) p.edit_type = TV_ID;
    if (ed.greenScreen && TV_POS_IDS.includes(ed.greenScreen.position)) p.greenScreenPosition = ed.greenScreen.position;
    if (ed.motion && typeof ed.motion === 'object' && !Array.isArray(ed.motion)) {
      if (MOTION_THEME_IDS.includes(ed.motion.theme)) p.motionTheme = ed.motion.theme;
      if (Number(ed.motion.count) > 0) p.motionCount = Number(ed.motion.count) <= 3 ? 'few' : 'some';
    }
    const fromEd = {
      zoom_cuts: ed.camera && ed.camera.zoom_cuts, push_in: ed.camera && ed.camera.push_in,
      flash: Array.isArray(ed.transitions) ? ed.transitions.some((t) => t.type === 'flash') : undefined,
      sfx: ed.sfx && ed.sfx.enabled, music: ed.music && ed.music.enabled,
      cta: ed.cta && ed.cta.enabled, disclaimer: ed.disclaimer && ed.disclaimer.enabled,
      motion: motionOn(ed.motion),
    };
    Object.entries(fromEd).forEach(([k, v]) => { if (typeof v === 'boolean' && k in p.elements) p.elements[k] = v; });
    const mu = ed.music;
    if (mu && typeof mu === 'object') {
      if (mu.enabled === false) p.music_mood = MUSIC_OFF;
      else if (typeof mu.file === 'string' && mu.file) { p.music_mood = MUSIC_FILE; p.music_file = mu.file; }
      else if (typeof mu.mood === 'string' && slugify(mu.mood)) p.music_mood = slugify(mu.mood);
      else if (Object.keys(mu).length) p.music_mood = MUSIC_ASK;
    }
  }
  const merge = (src) => {
    if (!src || typeof src !== 'object') return;
    ['edit_type', 'caption_style', 'hook_style'].forEach((k) => { if (src[k]) p[k] = src[k]; });
    if (normalizeHex(src.accent)) p.accent = normalizeHex(src.accent);
    ['hook_text', 'cta_text', 'note'].forEach((k) => { if (typeof src[k] === 'string') p[k] = src[k]; });
    if (src.elements && typeof src.elements === 'object') Object.entries(src.elements).forEach(([k, v]) => { p.elements[k] = Boolean(v); });
    if (DENOISE_IDS.includes(src.denoise)) p.denoise = src.denoise;
    if (TV_POS_IDS.includes(src.greenScreenPosition)) p.greenScreenPosition = src.greenScreenPosition;
    if (MOTION_COUNT_IDS.includes(src.motionCount)) p.motionCount = src.motionCount;
    if (MOTION_THEME_IDS.includes(src.motionTheme)) p.motionTheme = src.motionTheme;
    if (typeof src.music_mood === 'string' && (src.music_mood === MUSIC_OFF || MOOD_ID_RE.test(src.music_mood))) {
      p.music_mood = src.music_mood;
      p.music_file = src.music_mood === MUSIC_FILE && typeof src.music_file === 'string' ? src.music_file : '';
    } else if (src.elements && typeof src.elements.music === 'boolean') {
      // saved before the Music choice existed: keep "count track" without inventing a source
      if (!src.elements.music) p.music_mood = MUSIC_OFF;
      else if (p.music_mood === MUSIC_OFF) p.music_mood = MUSIC_ASK;
    }
  };
  merge(data.state && data.state.style);
  merge(data.saved && data.saved.style);
  return sanitize(p, cat, music);
}

export function sanitize(p, cat = {}, music = null) {
  const ids = (list) => (list || []).map((x) => x.id);
  const fix = (value, list, fallback) => (ids(list).includes(value) ? value : (fallback && ids(list).includes(fallback) ? fallback : (ids(list)[0] || null)));
  const d = cat.defaults || {};
  const out = { ...p, elements: { ...(p.elements || {}) } };
  out.edit_type = fix(out.edit_type, cat.edit_types, d.edit_type);
  out.caption_style = fix(out.caption_style, cat.caption_styles, d.caption_style);
  out.hook_style = fix(out.hook_style, cat.hook_styles, d.hook_style);
  out.accent = normalizeHex(out.accent) || '#FFC400';
  ['hook_text', 'cta_text', 'note'].forEach((k) => { out[k] = typeof out[k] === 'string' ? out[k] : ''; });
  (cat.elements || []).forEach((item) => { if (!(item.id in out.elements)) out.elements[item.id] = Boolean(item.default); });
  out.denoise = DENOISE_IDS.includes(out.denoise) ? out.denoise : 'off';
  out.greenScreenPosition = TV_POS_IDS.includes(out.greenScreenPosition) ? out.greenScreenPosition : TV_POS_DEFAULT;
  out.motionCount = MOTION_COUNT_IDS.includes(out.motionCount) ? out.motionCount : 'few';
  out.motionTheme = MOTION_THEME_IDS.includes(out.motionTheme) ? out.motionTheme : 'paper';
  out.music_file = typeof out.music_file === 'string' ? out.music_file : '';
  if (typeof out.music_mood !== 'string' || !(out.music_mood === MUSIC_OFF || out.music_mood === MUSIC_ASK || MOOD_ID_RE.test(out.music_mood))) out.music_mood = MUSIC_OFF;
  if (out.music_mood === MUSIC_FILE && !out.music_file) out.music_mood = MUSIC_OFF;
  if (out.music_mood !== MUSIC_FILE) out.music_file = '';
  const t = music;
  if (t && t.ok) {
    // Keep music enabled when a selected mood or file disappears; let the user choose a replacement
    const moods = (t.moods || []).map((m) => m.id);
    if (out.music_mood === MUSIC_FILE && !(t.edit_files || []).includes(out.music_file)) out.music_mood = MUSIC_ASK;
    else if (![MUSIC_OFF, MUSIC_FILE, MUSIC_ASK].includes(out.music_mood) && !moods.includes(out.music_mood)) out.music_mood = MUSIC_ASK;
    if (out.music_mood !== MUSIC_FILE) out.music_file = '';
  }
  if ('music' in out.elements || out.music_mood !== MUSIC_OFF) out.elements.music = out.music_mood !== MUSIC_OFF;
  return out;
}
