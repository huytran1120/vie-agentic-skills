import { clamp, el, fmtTime } from '../dom.mjs';

export class Playback {
  constructor(view) { this.view = view; }

  now() {
    if (this.view.scrubbing) return this.view.scrubTime;
    if (this.view.seekTarget !== null) return this.view.seekTarget;
    return this.view.els.video.currentTime || 0;
  }

  togglePlay() {
    const { video } = this.view.els;
    if (!this.view.mediaKey) return;
    if (video.paused || video.ended) {
      if (video.ended || video.currentTime >= this.view.duration - 0.05) video.currentTime = 0;
      video.play().catch(() => {});
    } else {
      video.pause();
    }
  }

  seek(t) {
    const { video } = this.view.els;
    if (!this.view.duration) return;
    const target = clamp(t, 0, Math.max(0, this.view.duration - 0.001));
    this.view.seekTarget = target;
    if (!video.seeking) video.currentTime = target;
    this.renderTime();
  }

  onSeeked() {
    const { video } = this.view.els;
    if (this.view.seekTarget !== null && Math.abs(video.currentTime - this.view.seekTarget) > 0.0005) {
      video.currentTime = this.view.seekTarget;
      return;
    }
    this.view.seekTarget = null;
    this.renderTime();
  }

  stepFrames(dir) {
    const { video } = this.view.els;
    video.pause();
    const f = this.view.fps || 30;
    const idx = Math.round(this.now() * f);
    this.seek((idx + dir) / f + 0.0005);
  }

  jump(dir) {
    this.seek(this.now() + dir);
  }

  startLoop() {
    if (this.view.rafOn) return;
    this.view.rafOn = true;
    const loop = () => {
      this.renderTime();
      if (!this.view.els.video.paused || this.view.scrubbing) requestAnimationFrame(loop);
      else this.view.rafOn = false;
    };
    requestAnimationFrame(loop);
  }

  renderTime() {
    const t = this.now();
    this.view.els.time.textContent = fmtTime(t);
    this.view.els.playhead.style.left = this.view.timeline.pct(t);
    this.view.timeline.followPlayhead(t);
    if (this.view.pendingIn !== null || this.view.noteDraft) {
      const a = this.view.noteDraft ? this.view.noteDraft.in : Math.min(this.view.pendingIn, t);
      const b = this.view.noteDraft ? this.view.noteDraft.out : Math.max(this.view.pendingIn, t);
      this.view.els.selection.hidden = false;
      this.view.els.selection.style.left = this.view.timeline.pct(a);
      this.view.els.selection.style.width = this.view.duration ? `${((b - a) / this.view.duration) * 100}%` : '0';
    } else {
      this.view.els.selection.hidden = true;
    }
    let idx = -1;
    for (let i = 0; i < this.view.segments.length; i += 1) {
      const s = this.view.segments[i];
      if (t >= s.out_start - 1e-3 && t < s.out_end) { idx = i; break; }
    }
    if (idx === -1 && this.view.segments.length && t >= this.view.segments[this.view.segments.length - 1].out_start) idx = this.view.segments.length - 1;
    if (idx !== this.view.currentSeg) {
      this.view.currentSeg = idx;
      this.view.els.segments.querySelectorAll('.seg-block').forEach((b, i) => b.classList.toggle('is-current', i === idx));
      const seg = this.view.segments[idx];
      this.view.els.now.textContent = '';
      if (seg) {
        const label = seg.beat || `Segment ${idx + 1}`;
        this.view.els.now.append(el('b', { text: label }), seg.quote ? `“${seg.quote}”` : '');
        this.view.els.now.title = seg.quote || '';
      }
    }
    const items = this.view.els.marksList.children;
    this.view.marks.forEach((m, i) => { if (items[i]) items[i].classList.toggle('is-current', t >= m.in && t <= m.out); });
  }
}
