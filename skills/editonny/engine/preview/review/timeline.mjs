import { clamp, el, firstWords, fmtRuler, fmtTime, versionOf } from '../dom.mjs';
import { TV_ID } from '../constants.mjs';

export class Timeline {
  constructor(view) { this.view = view; }

  zoomBy(dir, anchorClientX) {
    const steps = [1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32];
    const i = steps.findIndex((s) => s >= this.view.zoom - 1e-6);
    const at = i < 0 ? steps.length - 1 : i;
    const next = steps[clamp(at + dir, 0, steps.length - 1)];
    this.setZoom(next, anchorClientX);
  }

  setZoom(z, anchorClientX) {
    const next = clamp(z, 1, 32);
    if (Math.abs(next - this.view.zoom) < 1e-6) return;
    const { tlScroll, timeline } = this.view.els;
    const box = tlScroll.getBoundingClientRect();
    // Keep the cursor position on screen, or the playhead when there is no cursor
    let anchorPx;
    let anchorT;
    if (typeof anchorClientX === 'number') {
      anchorPx = clamp(anchorClientX - box.left, 0, box.width);
      anchorT = this.view.duration
        ? ((tlScroll.scrollLeft + anchorPx) / Math.max(1, timeline.clientWidth)) * this.view.duration
        : 0;
    } else {
      anchorT = this.view.playback.now();
      const x = this.view.duration ? (anchorT / this.view.duration) * timeline.clientWidth - tlScroll.scrollLeft : 0;
      anchorPx = x >= 0 && x <= box.width ? x : box.width / 2;
    }
    this.view.zoom = next;
    this.applyZoom();
    const full = tlScroll.clientWidth * this.view.zoom;
    tlScroll.scrollLeft = this.view.duration
      ? clamp((anchorT / this.view.duration) * full - anchorPx, 0, Math.max(0, full - tlScroll.clientWidth))
      : 0;
  }

  applyZoom() {
    this.view.els.timeline.style.width = `${this.view.zoom * 100}%`;
    this.view.els.zoomLightl.textContent = this.view.zoom >= 10 || Number.isInteger(this.view.zoom)
      ? `${Math.round(this.view.zoom)}x` : `${this.view.zoom}x`;
    this.view.section.querySelectorAll('[data-zoom]').forEach((b) => {
      if (b.dataset.zoom === 'in') b.disabled = this.view.zoom >= 32;
      if (b.dataset.zoom === 'out') b.disabled = this.view.zoom <= 1;
      if (b.dataset.zoom === 'fit') b.disabled = this.view.zoom <= 1;
    });
    this.renderRuler();
    this.loadStrips();
  }

  followPlayhead(t) {
    if (this.view.zoom <= 1 || this.view.scrubbing || !this.view.duration) return;
    const { tlScroll, timeline } = this.view.els;
    const full = timeline.clientWidth;
    const view = tlScroll.clientWidth;
    if (full <= view) return;
    const x = (t / this.view.duration) * full;
    const margin = view * 0.15;
    const left = tlScroll.scrollLeft;
    if (x < left + margin || x > left + view - margin) {
      tlScroll.scrollLeft = clamp(x - view / 2, 0, full - view);
    }
  }

  timeAtX(clientX) {
    const rect = this.view.els.timeline.getBoundingClientRect();
    return clamp((clientX - rect.left) / Math.max(1, rect.width), 0, 1) * this.view.duration;
  }

  segmentAt(t) {
    return this.view.segments.find((s) => t >= s.out_start - 1e-3 && t < s.out_end) || null;
  }

  onPointerDown(e) {
    if (e.button !== 0 || !this.view.duration) return;
    e.preventDefault();
    const stamp = performance.now();
    const isDouble = this.view.lastDown && stamp - this.view.lastDown.t < 400 && Math.abs(e.clientX - this.view.lastDown.x) < 8;
    this.view.lastDown = isDouble ? null : { t: stamp, x: e.clientX };
    if (isDouble) {
      const seg = this.segmentAt(this.timeAtX(e.clientX));
      if (seg) { this.view.markControls.markSegment(seg); return; }
    }
    this.view.els.timeline.setPointerCapture(e.pointerId);
    this.view.scrubbing = true;
    this.view.resumeAfterScrub = !this.view.els.video.paused;
    this.view.els.video.pause();
    this.view.scrubTime = this.timeAtX(e.clientX);
    this.view.playback.seek(this.view.scrubTime);
    this.view.playback.startLoop();
  }

  onPointerMove(e) {
    if (!this.view.scrubbing) return;
    this.view.scrubTime = this.timeAtX(e.clientX);
    this.view.playback.seek(this.view.scrubTime);
  }

  onPointerUp() {
    if (!this.view.scrubbing) return;
    this.view.scrubbing = false;
    this.view.playback.seek(this.view.scrubTime);
    if (this.view.resumeAfterScrub) this.view.els.video.play().catch(() => {});
  }

  pct(t) {
    return this.view.duration ? `${clamp((t / this.view.duration) * 100, 0, 100)}%` : '0%';
  }

  renderRuler() {
    const ruler = this.view.els.ruler;
    ruler.textContent = '';
    const width = this.view.els.timeline.clientWidth;
    if (!this.view.duration || !width) return;
    const steps = [0.5, 1, 2, 5, 10, 15, 30, 60, 120, 300];
    const pxPerSec = width / this.view.duration;
    const step = steps.find((s) => s * pxPerSec >= 90) || 600;
    const minor = step / (step >= 10 ? 5 : 2);
    const frag = document.createDocumentFragment();
    for (let t = 0; t <= this.view.duration + 1e-6; t += minor) {
      const isMajor = Math.abs(t / step - Math.round(t / step)) < 1e-6;
      const tick = el('div', { class: isMajor ? 'tick' : 'tick minor' });
      tick.style.left = this.pct(t);
      if (isMajor && (this.view.duration - t) * pxPerSec > 28) tick.textContent = fmtRuler(t, step);
      frag.append(tick);
    }
    ruler.append(frag);
  }

  renderSegments() {
    const box = this.view.els.segments;
    box.textContent = '';
    this.view.currentSeg = -2;
    if (!this.view.duration) return;
    const segs = this.view.segments.length ? this.view.segments : [{ out_start: 0, out_end: this.view.duration, beat: 'Whole video', quote: '' }];
    segs.forEach((s, i) => {
      const label = s.beat || `Segment ${i + 1}`;
      const block = el('div', {
        class: 'seg-block',
        title: `${label} · ${fmtTime(s.out_start)} → ${fmtTime(s.out_end)}${s.quote ? `\n“${s.quote}”` : ''}\nDouble-click to mark this whole segment`,
      }, el('span', { class: 'seg-beat', text: label }), s.quote ? el('span', { class: 'seg-quote', text: firstWords(s.quote, 6) }) : null);
      if (s.id) block.dataset.segId = s.id;
      const tr = s.id ? this.view.trimControls.trimOf(s.id) : null;
      if (tr && (tr.start_delta || tr.end_delta)) block.classList.add('is-trimmed');
      this.view.trimControls.placeBlock(block, s, tr ? tr.start_delta : 0, tr ? tr.end_delta : 0);
      this.view.trimControls.addHandles(block, s);
      box.append(block);
    });
    this.view.playback.renderTime();
  }

  renderLayers() {
    if (this.view.cfg.phase !== 'final') return;
    const box = this.view.els.layers;
    box.textContent = '';
    const ed = this.view.data && this.view.data.edit_data;
    if (!ed || !this.view.duration) { box.hidden = true; return; }
    const items = [];
    if (ed.hook && ed.hook.enabled !== false && ed.hook.end > ed.hook.start) items.push({ start: ed.hook.start, end: ed.hook.end, label: 'Hook' });
    const insertLabel = { split_top: 'Image above', split_bottom: 'Image below', full: 'Fullscreen', pip: 'Picture in picture' };
    if (ed.edit_type === TV_ID) { insertLabel.split_top = 'Background'; insertLabel.split_bottom = 'Background'; }
    (ed.inserts || []).forEach((ins) => {
      if (ins.end > ins.start) items.push({ start: ins.start, end: ins.end, label: insertLabel[ins.type] || 'Image' });
    });
    if (ed.cta && ed.cta.enabled !== false) {
      const dur = Number(ed.cta.duration) || 2.5;
      const start = ed.cta.start === null || ed.cta.start === undefined ? this.view.duration - dur : Number(ed.cta.start);
      items.push({ start, end: Math.min(this.view.duration, start + dur), label: 'Call to action' });
    }
    box.hidden = items.length === 0;
    items.forEach((it) => {
      const pill = el('div', { class: 'layer-pill', text: it.label, title: `${it.label} · ${fmtTime(it.start)} → ${fmtTime(it.end)}` });
      pill.style.left = this.pct(it.start);
      pill.style.width = `max(6px, ${((it.end - it.start) / this.view.duration) * 100}%)`;
      box.append(pill);
    });
  }

  loadStrips() {
    if (!this.view.rel || !this.view.info || !this.view.active) return;
    const width = this.view.els.timeline.clientWidth;
    if (!width) return;
    const dpr = clamp(window.devicePixelRatio || 1, 1, 2);
    const { video } = this.view.els;
    const aspect = video.videoWidth && video.videoHeight ? video.videoWidth / video.videoHeight : 9 / 16;
    const stripH = this.view.els.strip.clientHeight || 64;
    const thumbW = stripH * aspect;
    const n = clamp(Math.ceil(width / thumbW / 4) * 4, 4, 160);
    const h = clamp(Math.round((stripH * dpr) / 16) * 16, 32, 192);
    const ver = versionOf(this.view.info);
    const file = encodeURIComponent(this.view.rel);
    const stripUrl = `/api/filmstrip?file=${file}&n=${n}&h=${h}&v=${ver}`;
    if (stripUrl !== this.view.stripUrl) {
      this.view.stripUrl = stripUrl;
      const { strip, stripImg } = this.view.els;
      strip.classList.add('is-loading');
      const img = new Image();
      img.onload = () => { if (this.view.stripUrl === stripUrl) { stripImg.src = stripUrl; strip.classList.remove('is-loading', 'is-empty'); } };
      img.onerror = () => { if (this.view.stripUrl === stripUrl) { strip.classList.remove('is-loading'); strip.classList.add('is-empty'); } };
      img.src = stripUrl;
    }
    const w = clamp(Math.round((width * dpr) / 250) * 250, 500, 4000);
    const waveUrl = `/api/waveform?file=${file}&w=${w}&h=104&v=${ver}`;
    if (waveUrl !== this.view.waveUrl) {
      this.view.waveUrl = waveUrl;
      const { wave, waveFill } = this.view.els;
      wave.classList.add('is-loading');
      const img = new Image();
      img.onload = () => {
        if (this.view.waveUrl !== waveUrl) return;
        waveFill.style.webkitMaskImage = `url("${waveUrl}")`;
        waveFill.style.maskImage = `url("${waveUrl}")`;
        wave.classList.remove('is-loading');
        wave.classList.add('is-ready');
      };
      img.onerror = () => { if (this.view.waveUrl === waveUrl) wave.classList.remove('is-loading'); };
      img.src = waveUrl;
    }
  }
}
