import { Review } from './review/view.mjs';
import { StyleView } from './style/view.mjs';
import { AWAIT_TAB, HASH_TAB, PHASE_LABEL, PHASE_TAB, POLL_MS, TAB_HASH, MUSIC_POLL_MS } from './constants.mjs';
import { fmtClock, isTypingTarget, parseMs } from './dom.mjs';
import { NUDGE, toast } from './feedback.mjs';
import { getSession, updateSession } from './api.mjs';

const App = {
  data: null,
  tab: null,
  lastPhase: undefined,
  lastMessage: null,
  connected: null,
  shownErrors: new Set(),
  musicAt: 0,
  musicBusy: false,

  init() {
    this.views = {
      cut: new Review(document.getElementById('view-cut'), {
        phase: 'cut',
        approveLabel: 'Approve cut',
        approvedLabel: 'Cut approved',
        emptyTitle: 'The cut is being prepared…',
        emptyText: 'The video appears automatically when ready. No reload is needed.',
        reloadedMsg: 'New cut loaded.',
        marksSavedMsg: 'Marks sent. The agent will adjust the cut.',
        approvedMsg: 'Cut approved. The agent can continue with styling.',
        approvedShort: 'Cut approved.',
        approvedBanner: (time) => `You approved this cut at ${time}. Next, choose a style.`,
        marksBanner: (time) => `Marks sent at ${time}. The revised cut appears when ready.`,
      }),
      style: new StyleView(document.getElementById('view-style')),
      final: new Review(document.getElementById('view-final'), {
        phase: 'final',
        approveLabel: 'Approve final video',
        approvedLabel: 'Final video approved',
        emptyTitle: 'The final video is not ready yet',
        emptyText: 'First approve the cut and choose a style. The final video appears here automatically when ready.',
        reloadedMsg: 'New final video loaded.',
        marksSavedMsg: 'Marks sent. The agent will adjust the video.',
        approvedMsg: 'Final video approved.',
        approvedShort: 'Final video approved.',
        approvedBanner: (time, rel) => `You approved the final video at ${time}. The file is at edit/${rel}.`,
        marksBanner: (time) => `Marks sent at ${time}. The revised version appears here when ready.`,
      }),
    };
    document.querySelectorAll('.tab').forEach((btn) => btn.addEventListener('click', () => this.setTab(btn.dataset.tab, true)));
    document.getElementById('help-btn').addEventListener('click', () => this.openHelp());
    document.addEventListener('keydown', (e) => this.onKey(e));
    document.addEventListener('keyup', (e) => {
      if ((e.code === 'Space' || e.key === ' ') && e.target && e.target.tagName === 'BUTTON' && this.activeReview()) e.preventDefault();
    });
    window.addEventListener('hashchange', () => { const t = HASH_TAB[location.hash]; if (t) this.setTab(t, true); });
    const fromHash = HASH_TAB[location.hash];
    this.setTab(fromHash || 'cut', Boolean(fromHash));
    this.poll();
  },

  activeReview() {
    const view = this.views[this.tab];
    return view instanceof Review ? view : null;
  },

  setTab(tab, byUser) {
    if (!this.views[tab]) return;
    const changed = tab !== this.tab;
    this.tab = tab;
    if (byUser) this.userPicked = true;
    document.querySelectorAll('.tab').forEach((btn) => btn.setAttribute('aria-selected', String(btn.dataset.tab === tab)));
    ['cut', 'style', 'final'].forEach((name) => {
      document.getElementById(`view-${name}`).hidden = name !== tab;
      const view = this.views[name];
      if (view instanceof Review) view.setActive(name === tab);
    });
    if (changed && location.hash !== TAB_HASH[tab]) history.replaceState(null, '', TAB_HASH[tab]);
    if (changed) window.scrollTo(0, 0);
  },

  openHelp() {
    const dialog = document.getElementById('help-dialog');
    if (!dialog.open) dialog.showModal();
  },

  onKey(e) {
    if (e.defaultPrevented || document.querySelector('dialog[open]')) return;
    const typing = isTypingTarget(e.target);
    if (e.key === '?' && !typing) { e.preventDefault(); this.openHelp(); return; }
    if (typing || e.metaKey || e.ctrlKey || e.altKey) return;
    const review = this.activeReview();
    if (review && review.handleKey(e)) e.preventDefault();
  },

  async poll() {
    try {
      const res = await fetch('/api/state', { cache: 'no-store' });
      if (!res.ok) throw new Error(String(res.status));
      const data = await res.json();
      this.setConnected(true);
      this.apply(data);
    } catch {
      this.setConnected(false);
    } finally {
      setTimeout(() => this.poll(), POLL_MS);
    }
  },

  setConnected(ok) {
    if (ok === this.connected) return;
    const was = this.connected;
    this.connected = ok;
    const line = document.getElementById('statusline');
    line.classList.toggle('is-offline', !ok);
    if (!ok) {
      document.getElementById('status-text').textContent = 'Preview disconnected. Check that it is still running. Retrying…';
      document.getElementById('status-badge').hidden = true;
      document.getElementById('status-meta').textContent = '';
    } else if (was === false) {
      this.lastMessage = null;
      toast('Preview reconnected.');
    }
  },

  apply(data) {
    this.data = data;
    updateSession(data);
    const state = data.state || null;
    const phase = state && state.phase ? state.phase : 'setup';

    // tab follows the phase when the agent moves on
    if (this.lastPhase === undefined) {
      if (!this.userPicked) this.setTab(PHASE_TAB[phase] || 'cut', false);
    } else if (phase !== this.lastPhase && PHASE_TAB[phase] && PHASE_TAB[phase] !== this.tab) {
      this.setTab(PHASE_TAB[phase], false);
      toast(`Current stage: ${PHASE_LABEL[phase] || phase}.`);
    }
    this.lastPhase = phase;

    this.views.cut.update(data);
    this.views.style.update(data);
    this.views.final.update(data);
    this.loadMusic();
    this.renderStatus(state, phase);

    Object.entries(data.errors || {}).forEach(([file, msg]) => {
      const key = `${file}:${msg}`;
      if (!this.shownErrors.has(key)) { this.shownErrors.add(key); toast(`Problem in ${file}: ${msg}`, 'error', 6000); }
    });
  },

  // moods of the personal soundtrack library (read-only route, needs the preview token)
  async loadMusic(force = false) {
    if (this.musicBusy || (!force && Date.now() - this.musicAt < MUSIC_POLL_MS) || !getSession().token) return;
    this.musicBusy = true;
    try {
      const res = await fetch('/api/music', { cache: 'no-store', headers: { 'X-Preview-Token': getSession().token } });
      const body = await res.json().catch(() => ({}));
      if (res.ok && body.ok) {
        this.musicAt = Date.now();
        this.views.style.setMusic(body);
      } else {
        this.musicAt = Date.now() - MUSIC_POLL_MS + 2000; // try again soon (the server may have restarted)
        if (!this.views.style.music) this.views.style.setMusic({ ok: false });
      }
    } catch {
      this.musicAt = Date.now() - MUSIC_POLL_MS + 2000;
    } finally {
      this.musicBusy = false;
    }
  },

  // saved_at of the approval, marks or style the person sent for what the agent is waiting on, or null
  receivedAt(state, awaiting) {
    const saved = (this.data && this.data.saved) || {};
    const since = parseMs(state && state.updated_at);
    if (awaiting === 'approval_cut' || awaiting === 'approval_final') {
      const phase = awaiting === 'approval_cut' ? 'cut' : 'final';
      const view = this.views[phase];
      const ap = saved.approval;
      if (view && view.approval.isApproved() && parseMs(ap.saved_at) >= since) return ap.saved_at;
      const mk = saved.marks;
      if (view && view.info && mk && mk.phase === phase && Array.isArray(mk.marks) && mk.marks.length
          && parseMs(mk.saved_at) >= view.info.mtime * 1000 - 1 && parseMs(mk.saved_at) >= since) return mk.saved_at;
    } else if (awaiting === 'style' && saved.style && parseMs(saved.style.saved_at) >= since) {
      return saved.style.saved_at;
    }
    return null;
  },

  renderStatus(state, phase) {
    const project = document.getElementById('project-name');
    const name = state && state.project ? state.project : '';
    if (project.textContent !== name) { project.textContent = name; document.title = name ? `${name} · Edit preview` : 'Edit preview'; }

    let awaiting = state ? state.awaiting : null;
    const received = this.receivedAt(state, awaiting);
    if (received) awaiting = null; // the person already acted: it is the agent's turn now
    document.querySelectorAll('.tab').forEach((btn) => btn.classList.toggle('is-awaiting', AWAIT_TAB[awaiting] === btn.dataset.tab));

    const line = document.getElementById('statusline');
    const text = document.getElementById('status-text');
    const badge = document.getElementById('status-badge');
    const meta = document.getElementById('status-meta');
    let message = state && state.message;
    if (received) {
      message = getSession().agentListening ? 'Received. The agent is working on it.' : `Received. ${NUDGE}`;
    }
    if (!message) {
      message = state ? {
        setup: 'The agent is preparing the edit.',
        cut: 'The agent is working on the cut.',
        style: 'Choose a video style and save.',
        final: 'The agent is composing the final video.',
      }[phase] || 'The agent is working.' : 'Waiting for the agent to begin editing.';
    }
    if (message !== this.lastMessage) {
      text.textContent = message;
      if (this.lastMessage !== null) { text.classList.remove('flash'); void text.offsetWidth; text.classList.add('flash'); }
      this.lastMessage = message;
    }
    badge.hidden = !awaiting;
    line.classList.toggle('is-awaiting', Boolean(awaiting));
    line.classList.toggle('is-working', !awaiting);
    const parts = [`Stage: ${PHASE_LABEL[phase] || phase}`];
    if (state && state.updated_at) { const clock = fmtClock(state.updated_at); if (clock) parts.push(`updated at ${clock}`); }
    meta.textContent = parts.join(' · ');
  },
};


export function init() { App.init(); }
