import { clamp, el, fmtTime, mediaUrl } from '../dom.mjs';
import { Playback } from './playback.mjs';
import { Timeline } from './timeline.mjs';
import { Trims } from './trims.mjs';
import { Marks } from './marks.mjs';
import { Approval } from './approval.mjs';
import { toast } from '../feedback.mjs';

export class Review {
  constructor(section, cfg) {
    this.cfg = cfg;
    this.section = section;
    section.append(document.getElementById('review-template').content.cloneNode(true));
    const q = (sel) => section.querySelector(sel);
    this.els = {
      empty: q('[data-empty]'), emptyTitle: q('[data-empty-title]'), emptyText: q('[data-empty-text]'),
      review: q('[data-review]'), frame: q('[data-frame]'), video: q('[data-video]'), bigPlay: q('[data-bigplay]'),
      videoMsg: q('[data-video-msg]'), play: q('[data-play]'), time: q('[data-time]'), duration: q('[data-duration]'),
      now: q('[data-now]'), timeline: q('[data-timeline]'), tlScroll: q('[data-tl-scroll]'),
      zoomLightl: q('[data-zoom-level]'), ruler: q('[data-ruler]'), layers: q('[data-layers]'),
      segments: q('[data-segments]'), strip: q('[data-filmstrip]'), stripImg: q('[data-filmstrip-img]'), wave: q('[data-wave]'),
      overlay: q('[data-marks-overlay]'), selection: q('[data-selection]'), playhead: q('[data-playhead]'),
      trimsCard: q('[data-trims-card]'), trimsList: q('[data-trims-list]'), trimCount: q('[data-trim-count]'),
      trimsState: q('[data-trims-state]'), saveTrims: q('[data-save-trims]'), clearTrims: q('[data-clear-trims]'),
      markCount: q('[data-mark-count]'), marksState: q('[data-marks-state]'), setIn: q('[data-set-in]'), setOut: q('[data-set-out]'), motionHere: q('[data-motion-here]'),
      pending: q('[data-pending]'), noteBox: q('[data-note-box]'), noteRange: q('[data-note-range]'), noteInput: q('[data-note-input]'),
      noteCancel: q('[data-note-cancel]'), marksList: q('[data-marks-list]'), marksEmpty: q('[data-marks-empty]'),
      banner: q('[data-banner]'), approveNote: q('[data-approve-note]'), download: q('[data-download]'),
      saveMarks: q('[data-save-marks]'), approve: q('[data-approve]'),
    };
    this.els.waveFill = el('div', { class: 'wave-fill' });
    this.els.wave.append(this.els.waveFill);
    this.els.approve.textContent = cfg.approveLabel;
    this.els.emptyTitle.textContent = cfg.emptyTitle;
    this.els.emptyText.textContent = cfg.emptyText;
    if (cfg.phase === 'final') this.els.layers.hidden = false;

    this.data = null;
    this.rel = null;
    this.info = null;
    this.mediaKey = null;
    this.candidateKey = null;
    this.duration = 0;
    this.fps = 30;
    this.segments = [];
    this.segKey = '';
    this.layersKey = '';
    this.currentSeg = -1;
    this.marks = [];
    this.dirty = false;
    this.marksSavedAt = null;
    this.trims = new Map();       // interval ID -> { start_delta, end_delta }
    this.trimsDirty = false;
    this.trimsSavedAt = null;
    this.trimsSeen = null;
    this.dragTrim = null;
    this.pendingIn = null;
    this.noteDraft = null;
    this.scrubbing = false;
    this.scrubTime = 0;
    this.seekTarget = null;
    this.rafOn = false;
    this.active = false;
    this.stripUrl = '';
    this.waveUrl = '';
    this.approving = false;
    this.zoom = 1;
    this.playback = new Playback(this);
    this.timeline = new Timeline(this);
    this.trimControls = new Trims(this);
    this.markControls = new Marks(this);
    this.approval = new Approval(this);
    this.bind();
  }

  bind() {
    const { video, timeline } = this.els;
    const refresh = () => this.playback.renderTime();
    video.addEventListener('play', () => { this.els.frame.classList.add('is-playing'); this.els.review.classList.add('is-playing'); this.playback.startLoop(); });
    video.addEventListener('pause', () => { this.els.frame.classList.remove('is-playing'); this.els.review.classList.remove('is-playing'); refresh(); });
    video.addEventListener('ended', refresh);
    video.addEventListener('timeupdate', () => { if (!this.rafOn) refresh(); });
    video.addEventListener('seeked', () => this.playback.onSeeked());
    video.addEventListener('loadedmetadata', () => this.onMetadata());
    video.addEventListener('error', () => this.onVideoError());
    video.addEventListener('click', () => this.playback.togglePlay());
    this.els.bigPlay.addEventListener('click', () => this.playback.togglePlay());
    this.els.play.addEventListener('click', () => this.playback.togglePlay());
    this.section.querySelectorAll('[data-step]').forEach((b) => b.addEventListener('click', () => this.playback.stepFrames(Number(b.dataset.step))));
    this.section.querySelectorAll('[data-jump]').forEach((b) => b.addEventListener('click', () => this.playback.jump(Number(b.dataset.jump))));

    timeline.addEventListener('pointerdown', (e) => this.timeline.onPointerDown(e));
    timeline.addEventListener('pointermove', (e) => this.timeline.onPointerMove(e));
    timeline.addEventListener('pointerup', (e) => this.timeline.onPointerUp(e));
    timeline.addEventListener('pointercancel', (e) => this.timeline.onPointerUp(e));
    timeline.addEventListener('lostpointercapture', (e) => this.timeline.onPointerUp(e));

    this.els.setIn.addEventListener('click', () => this.markControls.setIn());
    this.els.setOut.addEventListener('click', () => this.markControls.setOut());
    if (this.els.motionHere) this.els.motionHere.addEventListener('click', () => this.markControls.motionHere());
    this.els.noteBox.addEventListener('submit', (e) => { e.preventDefault(); this.markControls.addMark(); });
    this.els.noteCancel.addEventListener('click', () => { this.markControls.closeNote(); this.playback.renderTime(); });
    this.els.noteInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); this.markControls.closeNote(); this.playback.renderTime(); }
      if (e.key === 'Enter' && !e.isComposing) { e.preventDefault(); this.markControls.addMark(); }
    });
    this.els.saveMarks.addEventListener('click', () => this.markControls.saveMarks());
    this.els.approve.addEventListener('click', () => this.approval.approve());
    this.els.saveTrims.addEventListener('click', () => this.trimControls.saveTrims());
    this.els.clearTrims.addEventListener('click', () => {
      if (!this.trims.size) return;
      this.trims.clear();
      this.trimsDirty = true;
      this.timeline.renderSegments();
      this.trimControls.renderTrims();
    });

    this.section.querySelectorAll('[data-zoom]').forEach((b) => b.addEventListener('click', () => {
      const kind = b.dataset.zoom;
      if (kind === 'fit') this.timeline.setZoom(1);
      else this.timeline.zoomBy(kind === 'in' ? 1 : -1);
    }));
    this.els.tlScroll.addEventListener('wheel', (e) => {
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        this.timeline.zoomBy(e.deltaY < 0 ? 1 : -1, e.clientX);
      } else if (this.zoom > 1 && Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
        e.preventDefault();
        this.els.tlScroll.scrollLeft += e.deltaY;
      }
    }, { passive: false });

    let resizeTimer = null;
    new ResizeObserver(() => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => { this.timeline.renderRuler(); this.timeline.loadStrips(); }, 180);
    }).observe(timeline);

    this.timeline.applyZoom();
  }

  setActive(active) {
    this.active = active;
    if (!active && !this.els.video.paused) this.els.video.pause();
    if (active) requestAnimationFrame(() => { this.timeline.renderRuler(); this.timeline.loadStrips(); this.playback.renderTime(); });
  }

  update(data) {
    this.data = data;
    const state = data.state || {};
    const files = data.files || {};
    const rel = this.cfg.phase === 'cut' ? (state.cut_video || 'cut.mp4') : (state.final_video || null);
    const info = rel ? files[rel] : null;

    if (!rel || !info) {
      this.showEmpty(true);
      return;
    }
    const key = `${rel}|${info.mtime}|${info.size}|${info.sha256}`;
    if (key === this.mediaKey) this.info = info;
    if (key !== this.mediaKey) {
      const settled = info.age > 2.5 || key === this.candidateKey;
      if (settled) {
        this.loadMedia(rel, info, key);
      } else {
        this.candidateKey = key;
        if (!this.mediaKey) this.showEmpty(true);
      }
    }
    if (!this.mediaKey) return;
    this.showEmpty(false);

    const timeline = data.timeline && Array.isArray(data.timeline.segments) ? data.timeline : null;
    if (timeline && timeline.fps) this.fps = Number(timeline.fps) || 30;
    const segKey = JSON.stringify(timeline ? [timeline.duration, timeline.segments] : null);
    if (segKey !== this.segKey) {
      this.segKey = segKey;
      this.segments = timeline ? timeline.segments.slice().sort((a, b) => a.out_start - b.out_start) : [];
      this.timeline.renderSegments();
    }
    if (this.cfg.phase === 'final') {
      const layersKey = JSON.stringify([data.edit_data, this.duration]);
      if (layersKey !== this.layersKey) { this.layersKey = layersKey; this.timeline.renderLayers(); }
    }
    this.trimControls.syncTrims(data);
    this.approval.renderBanner();
  }

  showEmpty(isEmpty) {
    this.els.empty.hidden = !isEmpty;
    this.els.review.hidden = isEmpty;
    if (isEmpty && !this.els.video.paused) this.els.video.pause();
  }

  get draftKey() {
    return `preview:marks:${(this.data && this.data.edit_dir) || ''}:${this.cfg.phase}:${this.mediaKey}`;
  }

  loadMedia(rel, info, key) {
    const { video } = this.els;
    const hadMedia = Boolean(this.mediaKey);
    const resumeAt = hadMedia ? this.playback.now() : 0;
    const wasPlaying = hadMedia && !video.paused;
    const hadDirtyMarks = this.dirty && this.marks.length > 0;
    this.mediaKey = key;
    this.candidateKey = null;
    this.rel = rel;
    this.info = info;
    this.els.videoMsg.hidden = true;
    this.pendingResume = hadMedia ? { time: resumeAt, play: wasPlaying } : null;
    video.src = mediaUrl(rel, info);
    video.load();
    if (this.cfg.phase === 'final') {
      this.els.download.hidden = false;
      this.els.download.href = mediaUrl(rel, info);
      this.els.download.setAttribute('download', rel.split('/').pop());
    }
    this.stripUrl = '';
    this.waveUrl = '';
    this.showEmpty(false);

    // marks: keep unsent ones, drop the ones the agent already received
    if (hadMedia) {
      if (!hadDirtyMarks) { this.marks = []; this.dirty = false; this.marksSavedAt = null; }
      this.pendingIn = null;
      this.markControls.closeNote();
      toast(this.cfg.reloadedMsg + (hadDirtyMarks ? ' Review your marks before saving.' : ''));
    } else {
      this.markControls.restoreMarks();
    }
    this.markControls.renderMarks();
    this.approval.renderBanner();
    requestAnimationFrame(() => { this.timeline.renderRuler(); this.timeline.loadStrips(); });
  }

  onMetadata() {
    const { video } = this.els;
    const tlDur = this.data && this.data.timeline ? Number(this.data.timeline.duration) : 0;
    this.duration = isFinite(video.duration) && video.duration > 0 ? video.duration : tlDur;
    this.els.duration.textContent = fmtTime(this.duration);
    if (video.videoWidth && video.videoHeight) {
      this.els.frame.style.setProperty('--ar', `${video.videoWidth} / ${video.videoHeight}`);
      this.els.review.classList.toggle('is-horizontal', video.videoWidth > video.videoHeight * 1.05);
    }
    if (this.pendingResume) {
      const { time, play } = this.pendingResume;
      this.pendingResume = null;
      video.currentTime = clamp(time, 0, Math.max(0, this.duration - 1 / this.fps));
      if (play) video.play().catch(() => {});
    }
    this.timeline.renderSegments();
    this.timeline.renderLayers();
    this.timeline.renderRuler();
    this.markControls.renderMarks();
    this.timeline.loadStrips();
    this.playback.renderTime();
  }

  onVideoError() {
    if (!this.mediaKey) return;
    this.els.videoMsg.hidden = false;
    this.els.videoMsg.textContent = 'Could not open the video. If rendering is still in progress, it will appear shortly.';
    const failedKey = this.mediaKey;
    setTimeout(() => {
      if (this.mediaKey === failedKey) { this.mediaKey = null; this.candidateKey = failedKey; }
    }, 2500);
  }

  handleKey(e) {
    if (this.els.review.hidden) return false;
    const key = e.key;
    if (e.code === 'Space' || key === ' ') { if (!e.repeat) this.playback.togglePlay(); return true; }
    if (key === 'ArrowLeft' || key === 'ArrowRight') {
      const dir = key === 'ArrowLeft' ? -1 : 1;
      if (e.shiftKey) this.playback.jump(dir); else this.playback.stepFrames(dir);
      return true;
    }
    if (key === 'i' || key === 'I') { this.markControls.setIn(); return true; }
    if (key === 'o' || key === 'O') { this.markControls.setOut(); return true; }
    if (key === 'm' || key === 'M') { this.markControls.motionHere(); return true; }
    if (key === '+' || key === '=') { this.timeline.zoomBy(1); return true; }
    if (key === '-' || key === '_') { this.timeline.zoomBy(-1); return true; }
    if (key === '0') { this.timeline.setZoom(1); return true; }
    if (key === 'Escape') return this.markControls.cancelPending();
    return false;
  }
}
