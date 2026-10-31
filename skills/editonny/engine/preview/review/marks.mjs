import { el, fmtClock, fmtSeconds, fmtTime, parseMs, store } from '../dom.mjs';
import { handoff, toast } from '../feedback.mjs';
import { TRASH_SVG } from '../constants.mjs';
import { getSession, postJson } from '../api.mjs';

export class Marks {
  constructor(view) { this.view = view; }

  restoreMarks() {
    const saved = this.view.data && this.view.data.saved && this.view.data.saved.marks;
    const draft = store.get(this.view.draftKey);
    if (draft && Array.isArray(draft.marks)) {
      this.view.marks = draft.marks;
      this.view.dirty = true;
      return;
    }
    if (saved && saved.phase === this.view.cfg.phase && Array.isArray(saved.marks) && parseMs(saved.saved_at) >= this.view.info.mtime * 1000 - 1) {
      this.view.marks = saved.marks.map((m) => ({ in: m.in, out: m.out, note: m.note || '', ...(m.kind === 'motion' ? { kind: 'motion' } : {}) }));
      this.view.dirty = false;
      this.view.marksSavedAt = saved.saved_at;
    }
  }

  setIn() {
    if (!this.view.mediaKey) return;
    this.closeNote();
    this.view.pendingIn = this.view.playback.now();
    this.view.els.pending.hidden = false;
    this.view.els.pending.textContent = `Start at ${fmtTime(this.view.pendingIn)}. Move to the segment end and mark it.`;
    this.view.playback.renderTime();
  }

  setOut() {
    if (!this.view.mediaKey) return;
    const t = this.view.playback.now();
    let a = this.view.pendingIn;
    let b = t;
    let auto = false;
    if (a === null) { a = Math.max(0, t - 1); auto = true; }
    if (b < a) [a, b] = [b, a];
    if (b - a < 0.1) b = Math.min(this.view.duration, a + 0.5);
    this.view.els.video.pause();
    this.view.pendingIn = null;
    this.view.els.pending.hidden = true;
    this.view.noteDraft = { in: Math.round(a * 1000) / 1000, out: Math.round(b * 1000) / 1000 };
    this.view.els.noteRange.textContent = `${fmtTime(a)} → ${fmtTime(b)}`;
    this.view.els.noteRange.append(el('small', { text: auto ? `${fmtSeconds(b - a)}, the second before this point` : fmtSeconds(b - a) }));
    this.view.els.noteBox.hidden = false;
    this.view.els.noteInput.value = '';
    this.view.playback.renderTime();
    requestAnimationFrame(() => this.view.els.noteInput.focus());
  }

  markSegment(seg) {
    if (!this.view.mediaKey) return;
    this.view.els.video.pause();
    this.closeNote();
    this.view.pendingIn = null;
    this.view.els.pending.hidden = true;
    const a = Math.round(seg.out_start * 1000) / 1000;
    const b = Math.round(Math.min(this.view.duration, seg.out_end) * 1000) / 1000;
    this.view.playback.seek(a);
    this.view.noteDraft = { in: a, out: b };
    this.view.els.noteRange.textContent = `${fmtTime(a)} → ${fmtTime(b)}`;
    this.view.els.noteRange.append(el('small', { text: `${fmtSeconds(b - a)}, the whole segment` }));
    this.view.els.noteBox.hidden = false;
    this.view.els.noteInput.value = '';
    this.view.playback.renderTime();
    requestAnimationFrame(() => this.view.els.noteInput.focus());
  }

  closeNote() {
    this.view.noteDraft = null;
    this.view.els.noteBox.hidden = true;
  }

  cancelPending() {
    const had = this.view.pendingIn !== null || !this.view.els.noteBox.hidden;
    this.view.pendingIn = null;
    this.view.els.pending.hidden = true;
    this.closeNote();
    this.view.playback.renderTime();
    return had;
  }

  motionHere() {
    if (!this.view.mediaKey) return;
    this.view.els.video.pause();
    this.cancelPending();
    const t = Math.round(this.view.playback.now() * 1000) / 1000;
    this.view.marks.push({ in: t, out: Math.round(Math.min(this.view.duration || t + 1, t + 1) * 1000) / 1000, note: '', kind: 'motion' });
    this.view.marks.sort((x, y) => x.in - y.in || x.out - y.out);
    this.markDirty();
    toast(`Motion requested at ${fmtTime(t)}. Optionally describe what to show, then send the marks.`, 'ok', 3200);
  }

  addMark() {
    if (!this.view.noteDraft) return;
    this.view.marks.push({ ...this.view.noteDraft, note: this.view.els.noteInput.value.trim() });
    this.view.marks.sort((x, y) => x.in - y.in || x.out - y.out);
    this.closeNote();
    this.view.els.noteInput.blur();
    this.markDirty();
  }

  deleteMark(index) {
    this.view.marks.splice(index, 1);
    this.markDirty();
  }

  markDirty() {
    this.view.dirty = true;
    store.set(this.view.draftKey, { marks: this.view.marks });
    store.dropOthers(`preview:marks:${(this.view.data && this.view.data.edit_dir) || ''}:${this.view.cfg.phase}:`, this.view.draftKey);
    this.renderMarks();
  }

  renderMarks() {
    const list = this.view.els.marksList;
    list.textContent = '';
    const overlay = this.view.els.overlay;
    overlay.textContent = '';
    this.view.marks.forEach((m, i) => {
      const range = el('button', { class: 'mark-range', type: 'button', title: 'Go to this segment', text: `${fmtTime(m.in)} → ${fmtTime(m.out)}` });
      range.addEventListener('click', () => { this.view.els.video.pause(); this.view.playback.seek(m.in); });
      const isMotion = m.kind === 'motion';
      const note = el('input', {
        class: 'mark-note', type: 'text', maxlength: '500',
        placeholder: isMotion ? 'Optional: what to show (for example, a list of 3 items)' : 'Describe the change',
        'aria-label': `Mark note ${i + 1}`,
      });
      note.value = m.note || '';
      note.addEventListener('input', () => { m.note = note.value; this.view.dirty = true; store.set(this.view.draftKey, { marks: this.view.marks }); this.renderMarksState(); });
      note.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === 'Escape') note.blur(); });
      const del = el('button', { class: 'icon-btn small danger', type: 'button', 'aria-label': `Delete mark ${i + 1}`, title: 'Delete mark', html: TRASH_SVG });
      del.addEventListener('click', () => this.deleteMark(i));
      const number = el('span', { class: isMotion ? 'mark-number is-motion' : 'mark-number', text: isMotion ? '✦' : String(i + 1), title: isMotion ? 'Animation here' : '' });
      list.append(el('li', { class: isMotion ? 'mark-item is-motion' : 'mark-item' }, number, range, note, del));

      const region = el('div', { class: isMotion ? 'mark-region is-motion' : 'mark-region' }, el('span', { text: isMotion ? '✦' : String(i + 1) }));
      region.style.left = this.view.timeline.pct(m.in);
      region.style.width = this.view.duration ? `max(2px, ${((m.out - m.in) / this.view.duration) * 100}%)` : '0';
      overlay.append(region);
    });
    this.view.els.marksEmpty.hidden = this.view.marks.length > 0;
    this.view.els.markCount.textContent = this.view.marks.length ? `(${this.view.marks.length})` : '';
    this.renderMarksState();
    this.view.playback.renderTime();
  }

  renderMarksState() {
    const st = this.view.els.marksState;
    st.classList.remove('is-dirty', 'is-saved');
    if (this.view.dirty) {
      st.textContent = this.view.marks.length ? 'Not sent yet' : 'Change not sent';
      st.classList.add('is-dirty');
    } else if (this.view.marksSavedAt) {
      st.textContent = `Sent at ${fmtClock(this.view.marksSavedAt)}`;
      st.classList.add('is-saved');
    } else {
      st.textContent = '';
    }
    this.view.els.saveMarks.disabled = !this.view.dirty;
    this.view.els.saveMarks.classList.toggle('attention', this.view.dirty && this.view.marks.length > 0);
  }

  async saveMarks() {
    if (!this.view.dirty) return;
    if (!this.view.els.noteBox.hidden && this.view.noteDraft) this.addMark();
    this.view.els.saveMarks.disabled = true;
    try {
      const res = await postJson('/api/marks', { phase: this.view.cfg.phase, marks: this.view.marks });
      this.view.dirty = false;
      this.view.marksSavedAt = res.saved.saved_at;
      this.view.marks = res.saved.marks.map((m) => ({ ...m }));
      store.del(this.view.draftKey);
      if (this.view.data && this.view.data.saved) this.view.data.saved.marks = res.saved;
      toast(this.view.marks.length ? handoff(this.view.cfg.marksSavedMsg, 'Marks saved.')
        : handoff('Marks deleted. The agent was notified.', 'Marks deleted.'), 'ok', getSession().agentListening ? 3400 : 7000);
      this.renderMarks();
      this.view.approval.renderBanner();
    } catch (err) {
      toast(err.message, 'error', 5000);
      this.renderMarksState();
    }
  }
}
