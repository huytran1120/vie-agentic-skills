import { clamp, el, fmtClock, fmtTime, parseMs } from '../dom.mjs';
import { getSession, postJson } from '../api.mjs';
import { handoff, toast } from '../feedback.mjs';

export class Trims {
  constructor(view) { this.view = view; }

  canTrim() {
    return this.view.cfg.phase === 'cut';
  }

  trimOf(id) {
    return this.view.trims.get(id) || { start_delta: 0, end_delta: 0 };
  }

  addHandles(block, seg) {
    if (!this.canTrim() || !seg.id) return;
    ['start', 'end'].forEach((side) => {
      const grip = el('button', {
        class: `seg-handle ${side}`,
        type: 'button',
        tabindex: '-1',
        'aria-label': side === 'start' ? 'Extend the segment start' : 'Extend the segment end',
        title: side === 'start'
          ? 'Drag left to restore the word start (Shift for finer dragging; arrow keys: 0.01 s)'
          : 'Drag right to restore the word end (Shift for finer dragging; arrow keys: 0.01 s)',
      });
      grip.addEventListener('keydown', (e) => {
        if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
        e.preventDefault();
        e.stopPropagation();
        const step = (e.key === 'ArrowLeft' ? -1 : 1) * (e.shiftKey ? 0.05 : 0.01);
        this.nudgeTrim(seg, side, step);
      });
      grip.addEventListener('pointerdown', (e) => this.onTrimDown(e, seg, side, block, grip));
      grip.addEventListener('pointermove', (e) => this.onTrimMove(e));
      grip.addEventListener('pointerup', (e) => this.onTrimUp(e));
      grip.addEventListener('pointercancel', (e) => this.onTrimUp(e));
      grip.addEventListener('lostpointercapture', (e) => this.onTrimUp(e));
      block.append(grip);
    });
  }

  onTrimDown(e, seg, side, block, grip) {
    if (e.button !== 0 || !this.view.duration) return;
    e.preventDefault();
    e.stopPropagation();
    grip.setPointerCapture(e.pointerId);
    grip.focus({ preventScroll: true });
    grip.classList.add('is-on');
    block.classList.add('is-dragging');
    const cur = this.trimOf(seg.id);
    this.view.dragTrim = {
      seg, side, block, grip,
      x0: e.clientX,
      base: side === 'start' ? cur.start_delta : cur.end_delta,
      delta: side === 'start' ? cur.start_delta : cur.end_delta,
      badge: el('div', { class: 'seg-delta' }),
    };
    block.append(this.view.dragTrim.badge);
    this.paintDrag();
  }

  trimRate(fine) {
    const perSec = this.view.els.timeline.clientWidth / Math.max(0.001, this.view.duration);
    return Math.min(1 / Math.max(1, perSec), 0.01) / (fine ? 3 : 1);
  }

  onTrimMove(e) {
    const d = this.view.dragTrim;
    if (!d) return;
    e.preventDefault();
    const raw = d.base + (e.clientX - d.x0) * this.trimRate(e.shiftKey);
    d.delta = clamp(Math.round(raw * 100) / 100, -2, 2);
    this.paintDrag();
  }

  nudgeTrim(seg, side, step) {
    const cur = { ...this.trimOf(seg.id) };
    const key = side === 'start' ? 'start_delta' : 'end_delta';
    cur[key] = clamp(Math.round((cur[key] + step) * 100) / 100, -2, 2);
    if (!cur.start_delta && !cur.end_delta) this.view.trims.delete(seg.id);
    else this.view.trims.set(seg.id, { ...cur, beat: seg.beat || '', quote: seg.quote || '' });
    this.view.trimsDirty = true;
    this.view.timeline.renderSegments();
    this.renderTrims();
    const again = [...this.view.els.segments.children].find((b) => b.dataset.segId === seg.id);
    if (again) {
      const grip = again.querySelector(`.seg-handle.${side}`);
      if (grip) { grip.classList.add('is-on'); grip.focus({ preventScroll: true }); }
    }
  }

  onTrimUp() {
    const d = this.view.dragTrim;
    if (!d) return;
    this.view.dragTrim = null;
    d.grip.classList.remove('is-on');
    d.block.classList.remove('is-dragging');
    d.badge.remove();
    const cur = { ...this.trimOf(d.seg.id) };
    cur[d.side === 'start' ? 'start_delta' : 'end_delta'] = d.delta;
    if (!cur.start_delta && !cur.end_delta) this.view.trims.delete(d.seg.id);
    else this.view.trims.set(d.seg.id, { ...cur, beat: d.seg.beat || '', quote: d.seg.quote || '' });
    this.view.trimsDirty = true;
    this.view.timeline.renderSegments();
    this.renderTrims();
  }

  paintDrag() {
    const d = this.view.dragTrim;
    if (!d) return;
    const cur = this.trimOf(d.seg.id);
    const sd = d.side === 'start' ? d.delta : cur.start_delta;
    const ed = d.side === 'end' ? d.delta : cur.end_delta;
    this.placeBlock(d.block, d.seg, sd, ed);
    const seg = d.delta;
    const label = seg === 0 ? 'unchanged'
      : `${seg > 0 ? '+' : '−'}${Math.abs(seg).toFixed(2)} s ${d.side === 'start' ? 'at the start' : 'at the end'}`;
    d.badge.textContent = label;
  }

  placeBlock(block, seg, sd, ed) {
    const a = seg.out_start + (sd || 0);
    const b = seg.out_end + (ed || 0);
    block.style.left = `calc(${this.view.timeline.pct(a)} + 1px)`;
    block.style.width = `calc(${this.view.duration ? clamp(((b - a) / this.view.duration) * 100, 0, 100) : 0}% - 2px)`;
  }

  renderTrims() {
    const list = this.view.els.trimsList;
    list.textContent = '';
    const rows = [...this.view.trims.entries()]
      .map(([id, t]) => ({ id, ...t, seg: this.view.segments.find((s) => s.id === id) }))
      .sort((a, b) => (a.seg ? a.seg.out_start : 0) - (b.seg ? b.seg.out_start : 0));
    rows.forEach((r) => {
      const bits = [];
      if (r.start_delta) bits.push(`${r.start_delta < 0 ? 'extend' : 'shorten'} ${Math.abs(r.start_delta).toFixed(2)} s at the start`);
      if (r.end_delta) bits.push(`${r.end_delta > 0 ? 'extend' : 'shorten'} ${Math.abs(r.end_delta).toFixed(2)} s at the end`);
      const row = el('li', { class: 'trim-row' },
        el('span', { class: 'trim-when', text: r.seg ? fmtTime(r.seg.out_start) : r.id }),
        el('span', { class: 'trim-what', text: r.quote ? `“${r.quote}”` : (r.beat || r.id), title: r.quote || r.id }),
        el('span', { class: 'trim-delta', text: bits.join(' · ') }));
      const del = el('button', { class: 'icon-btn small danger', type: 'button', 'aria-label': 'Undo this adjustment', title: 'Undo' });
      del.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';
      del.addEventListener('click', () => {
        this.view.trims.delete(r.id);
        this.view.trimsDirty = true;
        this.view.timeline.renderSegments();
        this.renderTrims();
      });
      row.append(del);
      list.append(row);
    });
    const n = this.view.trims.size;
    this.view.els.trimsCard.hidden = !this.canTrim() || (n === 0 && !this.view.trimsSavedAt && !this.view.trimsDirty);
    this.view.els.trimCount.textContent = n ? String(n) : '';
    const st = this.view.els.trimsState;
    st.classList.remove('is-dirty', 'is-saved');
    if (this.view.trimsDirty) {
      st.textContent = n ? 'Not sent yet' : 'Change not sent';
      st.classList.add('is-dirty');
    } else if (this.view.trimsSavedAt) {
      st.textContent = `Sent at ${fmtClock(this.view.trimsSavedAt)}`;
      st.classList.add('is-saved');
    } else {
      st.textContent = '';
    }
    this.view.els.saveTrims.disabled = !this.view.trimsDirty;
    this.view.els.saveTrims.classList.toggle('attention', this.view.trimsDirty && n > 0);
    this.view.els.clearTrims.disabled = n === 0;
  }

  async saveTrims() {
    if (!this.view.trimsDirty) return;
    this.view.els.saveTrims.disabled = true;
    const payload = [...this.view.trims.entries()].map(([id, t]) => ({
      id, start_delta: t.start_delta, end_delta: t.end_delta, beat: t.beat || '', quote: t.quote || '',
    }));
    try {
      const res = await postJson('/api/trims', { phase: this.view.cfg.phase, trims: payload });
      this.view.trimsDirty = false;
      this.view.trimsSavedAt = res.saved.saved_at;
      if (this.view.data && this.view.data.saved) this.view.data.saved.trims = res.saved;
      toast(payload.length
        ? handoff('Adjustments sent. The agent will extend the segments and render again.', 'Adjustments sent.')
        : handoff('Adjustments cleared. The agent was notified.', 'Adjustments cleared.'),
      'ok', getSession().agentListening ? 3400 : 7000);
    } catch (err) {
      toast(err.message, 'error', 5000);
    }
    this.renderTrims();
  }

  syncTrims(data) {
    if (!this.canTrim()) return;
    const rec = data.saved && data.saved.trims;
    const fresh = Boolean(rec && rec.phase === this.view.cfg.phase && this.view.info
      && parseMs(rec.saved_at) >= this.view.info.mtime * 1000 - 1);
    const stamp = `${this.view.mediaKey}|${fresh ? rec.saved_at : ''}`;
    if (stamp === this.view.trimsSeen) return;
    this.view.trimsSeen = stamp;
    if (this.view.trimsDirty) return;   // Preserve unsaved adjustments while the user is editing.
    this.view.trims.clear();
    this.view.trimsSavedAt = fresh ? rec.saved_at : null;
    if (fresh) {
      (rec.trims || []).forEach((t) => this.view.trims.set(t.id, {
        start_delta: Number(t.start_delta) || 0,
        end_delta: Number(t.end_delta) || 0,
        beat: t.beat || '',
        quote: t.quote || '',
      }));
    }
    this.view.timeline.renderSegments();
    this.renderTrims();
  }
}
