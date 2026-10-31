import { el, normalizeHex } from '../dom.mjs';
import { CHECK_SVG, MOTION_COUNTS, MOTION_THEMES, TV_ID, TV_POSITIONS } from '../constants.mjs';

export class StyleControls {
  constructor(view) { this.view = view; }

  renderTypes() {
    const box = this.view.els.types;
    box.textContent = '';
    (this.view.catalog.edit_types || []).forEach((t) => {
      const schema = el('span', { class: t.id === TV_ID ? `schema tv pos-${this.view.picks.greenScreenPosition}` : 'schema', 'aria-hidden': 'true' });
      if (t.id === 'split_top') schema.append(el('span', { class: 'band' }), el('span', { class: 'person' }));
      else if (t.id === 'split_bottom') schema.append(el('span', { class: 'person' }), el('span', { class: 'band' }));
      else schema.append(el('span', { class: 'person' }));
      const card = el('button', {
        class: 'type-card', type: 'button', role: 'radio', 'aria-checked': String(this.view.picks.edit_type === t.id), 'data-id': t.id,
        'aria-label': t.desc ? `${t.label || t.id}. ${t.desc}` : (t.label || t.id),
      },
        schema, el('span', { class: 'tc-text' }, el('strong', { text: t.label || t.id }), t.desc ? el('span', { class: 'tc-desc', text: t.desc }) : null));
      card.addEventListener('click', () => { this.view.picks.edit_type = t.id; this.syncChecked(box, t.id); this.renderTvPos(); this.view.touch(); });
      box.append(card);
    });
    this.renderTvPos();
  }

  tvAvailable() {
    return (this.view.catalog.edit_types || []).some((t) => t.id === TV_ID);
  }

  tvPosLabel() {
    const pos = TV_POSITIONS.find((x) => x.id === this.view.picks.greenScreenPosition) || TV_POSITIONS[1];
    return pos.label;
  }

  tvNoteText() {
    // Planned inserts stay in edit_data; green-screen mode uses split inserts as backgrounds
    const ed = this.view.data && this.view.data.edit_data;
    const list = ed && Array.isArray(ed.inserts) ? ed.inserts : [];
    const n = list.filter((x) => x && (x.type === 'split_top' || x.type === 'split_bottom')).length;
    if (n === 1) return 'The planned image or video becomes your background automatically.';
    if (n > 1) return `The ${n} planned images and videos become your background automatically.`;
    return 'Images and videos in the edit become your background.';
  }

  renderTvPos() {
    const { tvPos, tvPosList, tvNote } = this.view.els;
    if (!tvPos || !tvPosList) return;
    const on = this.view.picks.edit_type === TV_ID && this.tvAvailable();
    tvPos.hidden = !on;
    tvPosList.textContent = '';
    if (tvNote) tvNote.textContent = on ? this.tvNoteText() : '';
    if (!on) return;
    TV_POSITIONS.forEach((pos) => {
      const mini = el('span', { class: `schema tv pos-${pos.id}`, 'aria-hidden': 'true' }, el('span', { class: 'person' }));
      const card = el('button', {
        class: 'type-card tv-pos-card', type: 'button', role: 'radio', 'data-id': pos.id,
        'aria-checked': String(this.view.picks.greenScreenPosition === pos.id), 'aria-label': `${pos.label}. ${pos.desc}`,
      }, mini, el('span', { class: 'tc-text' }, el('strong', { text: pos.label }), el('span', { class: 'tc-desc', text: pos.desc })));
      card.addEventListener('click', () => {
        this.view.picks.greenScreenPosition = pos.id;
        this.syncChecked(tvPosList, pos.id);
        const main = this.view.els.types.querySelector(`[data-id="${TV_ID}"] .schema`);
        if (main) main.className = `schema tv pos-${pos.id}`;
        this.view.touch();
      });
      tvPosList.append(card);
    });
  }

  renderCards() {
    if (!this.view.catalog || !this.view.picks) return;
    const build = (box, list, kind, pickKey) => {
      box.textContent = '';
      (list || []).forEach((st) => {
        const url = this.view.media.sampleUrl(kind, st.id);
        const thumb = el('span', { class: 'thumb' });
        if (url) {
          const img = el('img', { src: url, alt: '', loading: 'lazy', draggable: 'false' });
          img.addEventListener('error', () => { img.remove(); thumb.append(el('span', { class: 'thumb-fallback', text: st.label || st.id })); });
          thumb.append(img);
        } else {
          thumb.append(el('span', { class: 'thumb-fallback', text: st.label || st.id }));
        }
        const card = el('button', {
          class: 'style-card', type: 'button', role: 'radio', 'aria-checked': String(this.view.picks[pickKey] === st.id),
          'data-id': st.id, title: st.desc || '',
          'aria-label': [st.label || st.id, kind === 'caption' && st.animated ? 'animated' : '', st.desc || ''].filter(Boolean).join('. '),
        },
        kind === 'caption' && st.animated ? el('span', { class: 'badge', text: 'Animated' }) : null,
        el('span', { class: 'check', html: CHECK_SVG }),
        thumb,
        el('span', { class: 'meta' }, el('strong', { text: st.label || st.id }), st.desc ? el('span', { text: st.desc }) : null));
        card.addEventListener('click', () => {
          this.view.picks[pickKey] = st.id;
          this.view.pv = kind;
          this.syncChecked(box, st.id);
          this.view.touch();
          this.view.media.renderPreview();
        });
        card.addEventListener('mouseenter', () => { this.view.hover = { kind, id: st.id }; this.view.media.renderPreview(); });
        card.addEventListener('mouseleave', () => { this.view.hover = null; this.view.media.renderPreview(); });
        box.append(card);
      });
    };
    build(this.view.els.hooks, this.view.catalog.hook_styles, 'hook', 'hook_style');
    build(this.view.els.captions, this.view.catalog.caption_styles, 'caption', 'caption_style');
  }

  renderElements() {
    const box = this.view.els.elements;
    box.textContent = '';
    (this.view.catalog.elements || []).forEach((item) => {
      if (item.id === 'music') return; // the "Background music" section below is the control for it
      const input = el('input', { class: 'switch', type: 'checkbox', 'data-id': item.id, 'aria-label': item.label || item.id });
      input.checked = Boolean(this.view.picks.elements[item.id]);
      input.addEventListener('change', () => {
        this.view.picks.elements[item.id] = input.checked;
        this.view.touch();
        this.renderCtaState();
        if (item.id === 'motion') this.renderMotionOptions();
      });
      box.append(el('label', { class: 'toggle' }, el('span', { text: item.label || item.id }), input));
      if (item.id === 'motion') box.append(el('div', { class: 'motion-options', 'data-motion-options': '' }));
    });
    this.renderCtaState();
    this.renderMotionOptions();
  }

  renderMotionOptions() {
    const box = this.view.els.elements.querySelector('[data-motion-options]');
    if (!box) return;
    box.textContent = '';
    box.hidden = !this.view.picks.elements.motion;
    if (box.hidden) return;
    const group = (title, opts, key) => {
      const list = el('div', { class: 'motion-choice', role: 'radiogroup', 'aria-label': title });
      opts.forEach((opt) => {
        const card = el('button', {
          class: 'type-card motion-card', type: 'button', role: 'radio', 'data-id': opt.id,
          'aria-checked': String(this.view.picks[key] === opt.id), 'aria-label': `${opt.label}. ${opt.desc}`,
        }, ...(opt.sw ? [el('span', { class: 'motion-sw', 'aria-hidden': 'true' },
          ...opt.sw.map((c) => { const dot = el('i'); dot.style.background = c || this.view.picks.accent; return dot; }))] : []),
        el('span', { class: 'tc-text' }, el('strong', { text: opt.label }), el('span', { class: 'tc-desc', text: opt.desc })));
        card.addEventListener('click', () => { this.view.picks[key] = opt.id; this.syncChecked(list, opt.id); this.view.touch(); });
        list.append(card);
      });
      return el('div', { class: 'motion-group' }, el('span', { class: 'motion-label', text: title }), list);
    };
    box.append(
      group('How many', MOTION_COUNTS, 'motionCount'),
      group('Visual', MOTION_THEMES, 'motionTheme'),
      el('p', { class: 'hint', text: 'The agent chooses key moments from the speech. For an exact time, pause the video and choose "Animation here".' }),
    );
  }

  renderCtaState() {
    const hasCta = this.view.catalog && (this.view.catalog.elements || []).some((x) => x.id === 'cta');
    const off = hasCta && !this.view.picks.elements.cta;
    this.view.els.cta.disabled = off;
    this.view.els.ctaHelp.textContent = off ? 'The call-to-action card is disabled in Elements.' : 'Leave blank for the agent to suggest text.';
  }

  syncChecked(box, id) {
    box.querySelectorAll('[role="radio"]').forEach((c) => c.setAttribute('aria-checked', String(c.dataset.id === id)));
  }

  setAccent(value, source) {
    const norm = normalizeHex(value);
    if (!norm || !this.view.picks) return;
    const changed = norm !== this.view.picks.accent;
    this.view.picks.accent = norm;
    if (source !== 'picker') this.view.els.picker.value = norm.toLowerCase();
    if (source !== 'hex') this.view.els.hex.value = norm;
    this.view.els.swatches.querySelectorAll('.swatch').forEach((sw) => sw.setAttribute('aria-pressed', String(normalizeHex(sw.title) === norm)));
    if (changed && source !== 'init') this.view.touch();
    this.view.media.renderPreview();
    this.view.renderSummary();
  }

  hexError(on) {
    this.view.els.hex.classList.toggle('is-invalid', on);
    this.view.els.hexHelp.classList.toggle('is-error', on);
    this.view.els.hexHelp.textContent = on ? 'Use #RRGGBB, for example #FFC400.' : 'Format: #RRGGBB.';
  }

  renderCounter() {
    const len = this.view.els.hookText.value.length;
    this.view.els.hookCount.textContent = len ? `${len}/90` : '';
  }
}
