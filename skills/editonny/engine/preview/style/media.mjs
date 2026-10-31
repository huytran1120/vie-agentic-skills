import { el, mediaUrl, normalizeHex } from '../dom.mjs';
import { DENOISE, MUSIC_ASK, MUSIC_FILE, MUSIC_OFF, baseName } from '../constants.mjs';

export class StyleMedia {
  constructor(view) { this.view = view; }

  sampleUrl(kind, id) {
    const idx = this.view.data && this.view.data.samples;
    const file = idx && idx[kind] && idx[kind][id];
    if (!file) return null;
    const samplesRel = (this.view.data.state && this.view.data.state.samples) || 'samples/index.json';
    const dir = samplesRel.includes('/') ? samplesRel.slice(0, samplesRel.lastIndexOf('/') + 1) : '';
    const rel = file.startsWith('/') ? null : `${dir}${file}`;
    if (!rel) return null;
    return mediaUrl(rel, this.view.data.files ? this.view.data.files[samplesRel] : null);
  }

  musicOptions() {
    const t = this.view.music;
    const opts = [{ key: MUSIC_OFF, mood: MUSIC_OFF, file: '', mark: '–', label: 'No music', desc: 'Your voice and sound effects only.' }];
    if (t && t.ok) {
      (t.moods || []).forEach((m) => {
        const count = `${m.count} ${m.count === 1 ? 'track' : 'music'}`;
        const fav = m.favorite_title ? ` · ★ ${m.favorite_title}` : ' · the agent chooses the best fit';
        opts.push({ key: m.id, mood: m.id, file: '', mark: '♪', label: m.label || m.id, desc: `${count}${fav}`, title: m.when || '' });
      });
      (t.edit_files || []).forEach((f) => {
        opts.push({ key: `${MUSIC_FILE}:${f}`, mood: MUSIC_FILE, file: f, mark: '♫', label: 'Use a project audio file', desc: baseName(f), title: f });
      });
    }
    return opts;
  }

  musicKey() {
    return this.view.picks.music_mood === MUSIC_FILE ? `${MUSIC_FILE}:${this.view.picks.music_file}` : this.view.picks.music_mood;
  }

  musicLabel() {
    const opt = this.musicOptions().find((o) => o.key === this.musicKey());
    if (opt) return opt.mood === MUSIC_FILE ? `File ${opt.desc}` : opt.label;
    if (this.view.picks.music_mood === MUSIC_ASK) return 'Music enabled; choose a track';
    return this.view.picks.music_mood === MUSIC_FILE ? `File ${baseName(this.view.picks.music_file)}` : this.view.picks.music_mood;
  }

  renderMusic() {
    const box = this.view.els.music;
    if (!box || !this.view.picks) return;
    box.textContent = '';
    const opts = this.musicOptions();
    const current = this.musicKey();
    if (current !== MUSIC_ASK && !opts.some((o) => o.key === current)) {
      // chosen before the library list arrived: show it so the pick stays visible
      opts.push({ key: current, mood: this.view.picks.music_mood, file: this.view.picks.music_file, mark: '♪',
        label: this.view.picks.music_mood === MUSIC_FILE ? 'Use a project audio file' : this.view.picks.music_mood,
        desc: this.view.picks.music_mood === MUSIC_FILE ? baseName(this.view.picks.music_file) : 'Checking the library…' });
    }
    opts.forEach((opt) => {
      const card = el('button', {
        class: 'type-card music-card', type: 'button', role: 'radio', 'aria-checked': String(opt.key === current),
        'data-id': opt.key, title: opt.title || '', 'aria-label': `${opt.label}. ${opt.desc}`,
      }, el('span', { class: 'music-mark', 'aria-hidden': 'true', text: opt.mark }),
      el('span', { class: 'tc-text' }, el('strong', { text: opt.label }), el('span', { class: 'tc-desc', text: opt.desc })));
      card.addEventListener('click', () => {
        this.view.picks.music_mood = opt.mood;
        this.view.picks.music_file = opt.file || '';
        this.view.picks.elements.music = opt.mood !== MUSIC_OFF;
        this.view.controls.syncChecked(box, opt.key);
        this.view.touch();
      });
      box.append(card);
    });
    const t = this.view.music;
    let help = 'Loading your music library…';
    if (t && !t.ok) help = 'The music library is unavailable. You can request a track in the conversation.';
    else if (t && t.error) help = `Music library problem: ${t.error}`;
    else if (t && !(t.moods || []).length) help = 'Your music library is empty. Ask the agent to save a track with a mood.';
    else if (t) help = 'Each mood uses your favorite track (★) or the best fit for the video length. Music stays quiet beneath the voice.';
    if (current === MUSIC_ASK) help = `Music is enabled. Choose a mood or file, or leave the choice to the conversation. ${help}`;
    this.view.els.musicHelp.textContent = help;
  }

  renderDenoise() {
    const box = this.view.els.denoise;
    box.textContent = '';
    DENOISE.forEach((opt, level) => {
      // little meter: the voice bar stays, the noise bars around it shrink with the level
      const meter = el('span', { class: `noise-meter lv-${level}`, 'aria-hidden': 'true' },
        el('i', { class: 'nz' }), el('i', { class: 'nz' }), el('i', { class: 'vc' }), el('i', { class: 'vc tall' }),
        el('i', { class: 'vc' }), el('i', { class: 'nz' }), el('i', { class: 'nz' }));
      const card = el('button', {
        class: 'type-card noise-card', type: 'button', role: 'radio', 'aria-checked': String(this.view.picks.denoise === opt.id),
        'data-id': opt.id, 'aria-label': `${opt.label}. ${opt.desc}`,
      }, meter, el('span', { class: 'tc-text' }, el('strong', { text: opt.label }), el('span', { class: 'tc-desc', text: opt.desc })));
      card.addEventListener('click', () => { this.view.picks.denoise = opt.id; this.view.controls.syncChecked(box, opt.id); this.view.touch(); });
      box.append(card);
    });
  }

  renderPreview() {
    if (!this.view.catalog || !this.view.picks) return;
    this.view.section.querySelectorAll('[data-pv]').forEach((b) => {
      const on = b.dataset.pv === this.view.pv;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', String(on));
    });
    const kind = this.view.hover ? this.view.hover.kind : this.view.pv;
    const id = this.view.hover ? this.view.hover.id : this.view.picks[`${kind}_style`];
    const url = this.sampleUrl(kind, id);
    const list = kind === 'hook' ? this.view.catalog.hook_styles : this.view.catalog.caption_styles;
    const { pvImg, pvPlaceholder, pvLabel, sampleNote } = this.view.els;
    if (url) {
      if (pvImg.getAttribute('src') !== url) pvImg.src = url;
      pvImg.hidden = false;
      pvPlaceholder.hidden = true;
    } else {
      pvImg.hidden = true;
      pvPlaceholder.hidden = false;
      pvLabel.textContent = this.view.labelOf(list, id);
    }
    const idx = this.view.data && this.view.data.samples;
    const sampleAccent = idx && normalizeHex(idx.accent);
    if (!idx) sampleNote.textContent = 'Samples appear here when the agent generates them.';
    else if (sampleAccent && sampleAccent !== this.view.picks.accent) sampleNote.textContent = `This sample uses ${sampleAccent}. Your chosen color is used in the video.`;
    else sampleNote.textContent = `${kind === 'hook' ? 'Hook' : 'Captions'} ${this.view.labelOf(list, id)} on a frame from your video.`;
  }
}
