import { fmtClock, parseMs } from '../dom.mjs';
import { confirmBox, handoff, toast } from '../feedback.mjs';
import { getSession, postJson } from '../api.mjs';

export class Approval {
  constructor(view) { this.view = view; }

  isApproved() {
    const ap = this.view.data && this.view.data.saved && this.view.data.saved.approval;
    return Boolean(ap && ap.approved && ap.phase === this.view.cfg.phase && this.view.info
      && ap.file === this.view.rel && ap.file_sha256 === this.view.info.sha256
      && ap.dependencies_hash === this.view.info.dependencies_hash
      && parseMs(ap.saved_at) >= this.view.info.mtime * 1000 - 1);
  }

  async approve() {
    if (this.view.approving || !this.view.mediaKey) return;
    if (this.view.trimsDirty && this.view.trims.size) {
      const go = await confirmBox({
        title: 'Approve without sending adjustments?',
        text: 'You changed segment edges without sending adjustments. Approving now will not apply those changes.',
        ok: 'Approve anyway',
      });
      if (!go) return;
    }
    const savedMarks = this.view.data && this.view.data.saved && this.view.data.saved.marks;
    if (this.view.dirty && this.view.marks.length) {
      const go = await confirmBox({
        title: 'Approve without sending marks?',
        text: 'Your marks are unsaved. Approving now will not send those changes.',
        ok: 'Approve anyway',
      });
      if (!go) return;
    } else if (savedMarks && savedMarks.phase === this.view.cfg.phase && Array.isArray(savedMarks.marks) && savedMarks.marks.length
               && parseMs(savedMarks.saved_at) >= this.view.info.mtime * 1000 - 1) {
      const go = await confirmBox({
        title: 'Approve with pending marks?',
        text: 'You sent marks for this version and the agent has not returned a revision. Approval will prompt a check before continuing.',
        ok: 'Approve anyway',
      });
      if (!go) return;
    }
    this.view.approving = true;
    this.view.els.approve.disabled = true;
    try {
      const res = await postJson('/api/approve', {
        phase: this.view.cfg.phase, note: this.view.els.approveNote.value.trim(),
        file: this.view.rel, file_mtime: this.view.info.mtime, file_size: this.view.info.size,
        file_sha256: this.view.info.sha256, dependencies_hash: this.view.info.dependencies_hash,
      });
      if (this.view.data && this.view.data.saved) this.view.data.saved.approval = res.saved;
      this.view.els.approveNote.value = '';
      toast(handoff(this.view.cfg.approvedMsg, this.view.cfg.approvedShort), 'ok', getSession().agentListening ? 3400 : 7000);
    } catch (err) {
      toast(err.message, 'error', 5000);
    } finally {
      this.view.approving = false;
      this.renderBanner();
    }
  }

  renderBanner() {
    const { banner, approve, approveNote } = this.view.els;
    if (!this.view.info) return;
    const approved = this.isApproved();
    const savedMarks = this.view.data && this.view.data.saved && this.view.data.saved.marks;
    banner.className = 'banner';
    if (approved) {
      const ap = this.view.data.saved.approval;
      banner.hidden = false;
      banner.classList.add('is-approved');
      banner.textContent = this.view.cfg.approvedBanner(fmtClock(ap.saved_at), this.view.rel);
    } else if (!this.view.dirty && savedMarks && savedMarks.phase === this.view.cfg.phase && savedMarks.marks.length
               && parseMs(savedMarks.saved_at) >= this.view.info.mtime * 1000 - 1) {
      banner.hidden = false;
      banner.classList.add('is-info');
      banner.textContent = this.view.cfg.marksBanner(fmtClock(savedMarks.saved_at));
    } else {
      banner.hidden = true;
    }
    approve.textContent = approved ? this.view.cfg.approvedLabel : this.view.cfg.approveLabel;
    approve.classList.toggle('is-done', approved);
    approve.disabled = approved || this.view.approving;
    approveNote.hidden = approved;
  }
}
