import { StyleControls } from './controls.mjs';
import { StyleMedia } from './media.mjs';
import { el, fmtClock, normalizeHex, store, versionOf } from '../dom.mjs';
import { DENOISE, MUSIC_FILE, SWATCHES, TV_ID } from '../constants.mjs';
import { basePicks, sanitize } from './state.mjs';
import { handoff, toast } from '../feedback.mjs';
import { getSession, postJson } from '../api.mjs';

export class StyleView {
  constructor(section) {
    this.section = section;
    const q = (sel) => section.querySelector(sel);
    this.els = {
      empty: q('[data-style-empty]'), main: q('[data-style-main]'), types: q('[data-edit-types]'),
      picker: q('[data-accent-picker]'), hex: q('[data-accent-hex]'), hexHelp: q('[data-hex-help]'), swatches: q('[data-swatches]'),
      hookText: q('[data-hook-text]'), hookCount: q('[data-hook-count]'), hooks: q('[data-hook-styles]'), captions: q('[data-caption-styles]'),
      elements: q('[data-elements]'), denoise: q('[data-denoise]'), music: q('[data-music]'), musicHelp: q('[data-music-help]'),
      tvPos: q('[data-tv-pos]'), tvPosList: q('[data-tv-pos-list]'), tvNote: q('[data-tv-note]'),
      cta: q('[data-cta-text]'), ctaHelp: q('[data-cta-help]'), note: q('[data-style-note]'),
      pvImg: q('[data-pv-img]'), pvPlaceholder: q('[data-pv-placeholder]'), pvLabel: q('[data-pv-label]'), sampleNote: q('[data-sample-note]'),
      summary: q('[data-summary]'), saved: q('[data-style-saved]'), save: q('[data-save-style]'),
    };
    this.data = null;
    this.music = null;
    this.musicKey = '';
    this.catalog = null;
    this.catalogKey = '';
    this.samplesKey = '';
    this.picks = null;
    this.baseKey = '';
    this.dirty = false;
    this.savedAt = null;
    this.pv = 'hook';
    this.hover = null;
    this.saving = false;
    this.controls = new StyleControls(this);
    this.media = new StyleMedia(this);
    this.bind();
  }

  bind() {
    const { picker, hex, hookText, cta, note, save } = this.els;
    picker.addEventListener('input', () => this.controls.setAccent(picker.value, 'picker'));
    hex.addEventListener('input', () => {
      const norm = normalizeHex(hex.value);
      const full = /^#?[0-9a-f]{6}$/i.test(hex.value.trim());
      if (norm && full) { this.controls.setAccent(norm, 'hex'); this.controls.hexError(false); } else { this.controls.hexError(hex.value.trim().length >= 7 || !/^#?[0-9a-f]*$/i.test(hex.value.trim())); }
    });
    hex.addEventListener('blur', () => {
      const norm = normalizeHex(hex.value);
      if (norm) this.controls.setAccent(norm, 'blur');
      else if (this.picks) hex.value = this.picks.accent;
      this.controls.hexError(false);
    });
    hookText.addEventListener('input', () => { this.picks.hook_text = hookText.value; this.touch(); this.controls.renderCounter(); });
    cta.addEventListener('input', () => { this.picks.cta_text = cta.value; this.touch(); });
    note.addEventListener('input', () => { this.picks.note = note.value; this.touch(); });
    save.addEventListener('click', () => this.save());
    this.section.querySelectorAll('[data-pv]').forEach((b) => b.addEventListener('click', () => { this.pv = b.dataset.pv; this.media.renderPreview(); }));
    SWATCHES.forEach((c) => {
      const sw = el('button', { class: 'swatch', type: 'button', title: c, 'aria-label': `Use color ${c}`, 'aria-pressed': 'false', style: { background: c } });
      sw.addEventListener('click', () => this.controls.setAccent(c, 'swatch'));
      this.els.swatches.append(sw);
    });
  }

  get draftKey() { return `preview:style:${(this.data && this.data.edit_dir) || ''}`; }

  update(data) {
    this.data = data;
    const cat = data.catalog;
    const usable = cat && ((cat.caption_styles || []).length || (cat.hook_styles || []).length || (cat.edit_types || []).length);
    this.els.empty.hidden = Boolean(usable);
    this.els.main.hidden = !usable;
    if (!usable) return;

    const catalogKey = JSON.stringify(cat);
    const catalogChanged = catalogKey !== this.catalogKey;
    if (catalogChanged) { this.catalogKey = catalogKey; this.catalog = cat; }

    const saved = data.saved && data.saved.style;
    if (saved && saved.saved_at) this.savedAt = saved.saved_at;
    const base = basePicks(data, this.music);
    const baseKey = JSON.stringify(base);
    if (!this.picks) {
      const draft = store.get(this.draftKey);
      if (draft && draft.picks && draft.base === baseKey) { this.picks = sanitize(draft.picks, this.catalog || {}, this.music); this.dirty = true; } else { this.picks = base; }
      this.baseKey = baseKey;
      this.renderAll();
    } else if (baseKey !== this.baseKey) {
      this.baseKey = baseKey;
      if (!this.dirty) { this.picks = base; this.renderAll(); }
      else if (catalogChanged) this.renderAll();
    } else if (catalogChanged) {
      this.picks = sanitize(this.picks, this.catalog || {}, this.music);
      this.renderAll();
    }

    const samplesRel = (data.state && data.state.samples) || 'samples/index.json';
    const samplesInfo = data.files ? data.files[samplesRel] : null;
    const samplesKey = JSON.stringify([data.samples, versionOf(samplesInfo)]);
    if (samplesKey !== this.samplesKey) {
      this.samplesKey = samplesKey;
      this.controls.renderCards();
      this.media.renderPreview();
    }
    if (this.els.tvNote && this.picks && this.picks.edit_type === TV_ID) this.els.tvNote.textContent = this.controls.tvNoteText();
    this.renderSaved();
  }

  setMusic(t) {
    const key = JSON.stringify(t);
    if (key === this.musicKey) return;
    this.musicKey = key;
    this.music = t;
    if (!this.picks || !this.catalog) return;
    this.picks = sanitize(this.picks, this.catalog || {}, this.music);
    this.media.renderMusic();
    this.renderSummary();
  }

  touch() {
    this.dirty = true;
    store.set(this.draftKey, { picks: this.picks, base: this.baseKey });
    this.renderSummary();
    this.renderSaved();
  }

  renderAll() {
    const { hookText, cta, note } = this.els;
    this.controls.renderTypes();
    this.controls.renderCards();
    this.controls.renderElements();
    this.media.renderMusic();
    this.media.renderDenoise();
    hookText.value = this.picks.hook_text || '';
    cta.value = this.picks.cta_text || '';
    note.value = this.picks.note || '';
    this.controls.setAccent(this.picks.accent, 'init');
    this.controls.renderCounter();
    this.media.renderPreview();
    this.renderSummary();
    this.renderSaved();
  }

  labelOf(list, id) {
    const item = (list || []).find((x) => x.id === id);
    return item ? item.label || item.id : id || 'none';
  }

  renderSummary() {
    if (!this.catalog || !this.picks) return;
    const box = this.els.summary;
    box.textContent = '';
    const shown = (this.catalog.elements || []).filter((x) => x.id !== 'music');
    const on = shown.filter((x) => this.picks.elements[x.id]).length;
    const total = shown.length;
    const rows = [
      ['Type', this.labelOf(this.catalog.edit_types, this.picks.edit_type) + (this.picks.edit_type === TV_ID ? ` · ${this.controls.tvPosLabel().toLowerCase()}` : '')],
      ['Hook', this.labelOf(this.catalog.hook_styles, this.picks.hook_style)],
      ['Captions', this.labelOf(this.catalog.caption_styles, this.picks.caption_style)],
      ['Color', [el('span', { class: 'chip', style: { background: this.picks.accent } }), this.picks.accent]],
      ['Elements', `${on} of ${total} enabled`],
      ['Music', this.media.musicLabel()],
      ['Background noise', (DENOISE.find((d) => d.id === this.picks.denoise) || DENOISE[0]).label],
    ];
    rows.forEach(([k, v]) => box.append(el('dt', { text: k }), el('dd', {}, v)));
  }

  renderSaved() {
    const st = this.els.saved;
    st.classList.remove('is-dirty', 'is-saved');
    if (this.dirty) { st.textContent = 'Unsaved changes'; st.classList.add('is-dirty'); }
    else if (this.savedAt) { st.textContent = `Saved at ${fmtClock(this.savedAt)}`; st.classList.add('is-saved'); }
    else st.textContent = 'Nothing saved yet';
  }

  async save() {
    if (this.saving || !this.picks) return;
    const hexNorm = normalizeHex(this.els.hex.value);
    if (!hexNorm) { this.controls.hexError(true); this.els.hex.focus(); toast('Color must use #RRGGBB format.', 'error'); return; }
    this.controls.setAccent(hexNorm, 'blur');
    this.saving = true;
    this.els.save.disabled = true;
    try {
      const body = {
        edit_type: this.picks.edit_type, caption_style: this.picks.caption_style, hook_style: this.picks.hook_style,
        accent: this.picks.accent, hook_text: String(this.picks.hook_text || '').trim(), cta_text: String(this.picks.cta_text || '').trim(),
        elements: this.picks.elements, denoise: this.picks.denoise, note: String(this.picks.note || '').trim(),
        music_mood: this.picks.music_mood || null,
      };
      if (this.picks.music_mood === MUSIC_FILE) body.music_file = this.picks.music_file;
      if (this.picks.edit_type === TV_ID) body.greenScreenPosition = this.picks.greenScreenPosition;
      if (this.picks.elements.motion) { body.motionCount = this.picks.motionCount; body.motionTheme = this.picks.motionTheme; }
      const res = await postJson('/api/style', body);
      this.dirty = false;
      this.savedAt = res.saved.saved_at;
      if (this.data && this.data.saved) this.data.saved.style = res.saved;
      this.baseKey = JSON.stringify(basePicks(this.data, this.music));
      store.del(this.draftKey);
      toast(handoff('Style saved. The agent received your choices.', 'Style saved.'), 'ok', getSession().agentListening ? 3400 : 7000);
    } catch (err) {
      toast(err.message, 'error', 5000);
    } finally {
      this.saving = false;
      this.els.save.disabled = false;
      this.renderSaved();
    }
  }
}
