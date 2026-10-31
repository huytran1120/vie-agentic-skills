const session = { token: '', agentListening: false };
export const getSession = () => ({ ...session });
export function updateSession(data) {
  if (data.token) session.token = data.token;
  session.agentListening = Boolean(data.watcher && data.watcher.alive);
}

async function refreshToken() {
  try {
    const res = await fetch('/api/state', { cache: 'no-store' });
    const data = await res.json();
    session.token = data.token || '';
    session.agentListening = Boolean(data.watcher && data.watcher.alive);
  } catch { /* offline: the save below reports it */ }
}

export async function postJson(path, body, retried = false) {
  if (!session.token) await refreshToken();
  let res;
  try {
    res = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Preview-Token': session.token },
      body: JSON.stringify(body),
    });
  } catch {
    throw new Error('Preview disconnected. Is it still running?');
  }
  const data = await res.json().catch(() => ({}));
  if (res.status === 403 && !retried) { session.token = ''; return postJson(path, body, true); } // server restarted
  if (!res.ok || !data.ok) throw new Error(data.error ? `Could not save: ${data.error}` : `Could not save (error ${res.status}).`);
  return data;
}

