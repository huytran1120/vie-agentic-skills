export const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

export function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value === undefined || value === null || value === false) continue;
    if (key === 'class') node.className = value;
    else if (key === 'text') node.textContent = value;
    else if (key === 'html') node.innerHTML = value;
    else if (key.startsWith('on')) node.addEventListener(key.slice(2), value);
    else if (key === 'style') Object.assign(node.style, value);
    else node.setAttribute(key, value === true ? '' : value);
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

export function fmtTime(seconds) {
  if (seconds === null || seconds === undefined || !isFinite(seconds)) return '--:--';
  const s = Math.max(0, seconds);
  let m = Math.floor(s / 60);
  let rest = Math.round((s - m * 60) * 100) / 100;
  if (rest >= 60) { m += 1; rest -= 60; }
  return `${String(m).padStart(2, '0')}:${rest.toFixed(2).padStart(5, '0')}`;
}

export function fmtRuler(seconds, step) {
  const m = Math.floor(seconds / 60);
  const s = seconds - m * 60;
  const secText = step < 1 ? s.toFixed(1).padStart(4, '0') : String(Math.round(s)).padStart(2, '0');
  return `${m}:${secText}`;
}

export function fmtClock(value) {
  const d = typeof value === 'number' ? new Date(value) : new Date(Date.parse(value));
  if (isNaN(d)) return '';
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

export function fmtSeconds(sec) {
  return `${(Math.round(sec * 10) / 10).toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} s`;
}

export function firstWords(text, n) {
  if (!text) return '';
  const words = String(text).trim().split(/\s+/);
  const cut = words.slice(0, n).join(' ');
  return words.length > n ? `${cut.replace(/[.,;:!?]+$/, '')}…` : cut;
}

export const encodePath = (rel) => String(rel).split('/').map(encodeURIComponent).join('/');
export const versionOf = (info) => (info ? `${Math.round(info.mtime * 1000)}-${info.size}` : '0');
export const mediaUrl = (rel, info) => `/media/${encodePath(rel)}?v=${versionOf(info)}`;
export const parseMs = (iso) => { const t = Date.parse(iso || ''); return isNaN(t) ? 0 : t; };

// edit_data "motion": a list of animations or {"enabled": bool, "items": [...]}. undefined = not decided yet.
export function motionOn(m) {
  if (Array.isArray(m)) return m.some((it) => it && typeof it === 'object' && it.enabled !== false) || undefined;
  if (m && typeof m === 'object') {
    if (m.enabled === false) return false;
    return (Array.isArray(m.items) && m.items.some((it) => it && typeof it === 'object' && it.enabled !== false)) || undefined;
  }
  return undefined;
}

export function normalizeHex(value) {
  const m = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(String(value || '').trim());
  if (!m) return null;
  let hex = m[1];
  if (hex.length === 3) hex = hex.split('').map((c) => c + c).join('');
  return `#${hex.toUpperCase()}`;
}

export const store = {
  get(key) { try { const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : null; } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode */ } },
  del(key) { try { localStorage.removeItem(key); } catch { /* ignore */ } },
  dropOthers(prefix, keep) {
    try {
      Object.keys(localStorage).forEach((k) => { if (k.startsWith(prefix) && k !== keep) localStorage.removeItem(k); });
    } catch { /* ignore */ }
  },
};

export const isTypingTarget = (target) => {
  if (!target || !target.tagName) return false;
  const tag = target.tagName;
  if (tag === 'TEXTAREA' || tag === 'SELECT' || target.isContentEditable) return true;
  return tag === 'INPUT' && !['checkbox', 'radio', 'button', 'submit', 'range', 'color'].includes(target.type);
};
