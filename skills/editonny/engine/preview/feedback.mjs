import { getSession } from './api.mjs';
import { el } from './dom.mjs';

export const NUDGE = 'Send a message in the conversation (for example, "ready") so the agent can continue.';
export const handoff = (listening, saved) => (getSession().agentListening ? listening : `${saved} ${NUDGE}`);

export function toast(message, kind = 'ok', ms = 3400) {
  const wrap = document.getElementById('toasts');
  const node = el('div', { class: `toast${kind === 'error' ? ' is-error' : ''}`, role: kind === 'error' ? 'alert' : 'status', text: message });
  wrap.append(node);
  while (wrap.children.length > 3) wrap.firstElementChild.remove();
  setTimeout(() => {
    node.classList.add('is-leaving');
    setTimeout(() => node.remove(), 300);
  }, ms);
}

export function confirmBox({ title, text, ok }) {
  const dialog = document.getElementById('confirm-dialog');
  dialog.querySelector('[data-confirm-title]').textContent = title;
  dialog.querySelector('[data-confirm-text]').textContent = text;
  dialog.querySelector('[data-confirm-ok]').textContent = ok;
  dialog.returnValue = '';
  return new Promise((resolve) => {
    dialog.addEventListener('close', () => resolve(dialog.returnValue === 'ok'), { once: true });
    dialog.showModal();
    dialog.querySelector('[data-confirm-ok]').focus();
  });
}
