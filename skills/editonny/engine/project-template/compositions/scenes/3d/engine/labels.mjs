import { THREE } from './three.mjs';
import { clamp } from './time.mjs';
export function createLabels(stage, layer, items) {
  const { W, H, scale: e, colors } = stage;
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('width', W);
  svg.setAttribute('height', H);
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.style.cssText = 'position:absolute;left:0;top:0;overflow:visible;pointer-events:none';
  layer.appendChild(svg);
  const list = items.map((it) => {
    const el = document.createElement('div');
    el.textContent = it.text;
    el.style.cssText = `position:absolute;left:0;top:0;opacity:0;white-space:nowrap;font-family:Montserrat,sans-serif;font-weight:800;`
      + `font-size:${Math.round((it.size || 36) * e)}px;line-height:1.05;padding:${Math.round(14 * e)}px ${Math.round(22 * e)}px;`
      + `border-radius:${Math.round(18 * e)}px;color:${it.color || colors.ink};background:${it.background || colors.paper};`
      + `box-shadow:0 0 0 ${Math.max(2, Math.round(3 * e))}px ${colors.base},0 ${Math.round(8 * e)}px 0 ${Math.round(-1 * e)}px ${colors.base}`;
    layer.appendChild(el);
    const line = document.createElementNS(ns, 'line');
    line.setAttribute('stroke', it.lineColor || colors.accent);
    line.setAttribute('stroke-width', String(Math.max(2, 4 * e)));
    line.setAttribute('stroke-linecap', 'round');
    line.setAttribute('opacity', '0');
    const dot = document.createElementNS(ns, 'circle');
    dot.setAttribute('r', String(Math.max(4, 10 * e)));
    dot.setAttribute('fill', it.lineColor || colors.accent);
    dot.setAttribute('stroke', colors.paper);
    dot.setAttribute('stroke-width', String(Math.max(2, 4 * e)));
    dot.setAttribute('opacity', '0');
    svg.appendChild(line);
    svg.appendChild(dot);
    return { el, line, dot, side: it.side || 'right', w: el.offsetWidth, h: el.offsetHeight };
  });
  const v = new THREE.Vector3();
  return {
    measure() { for (const r of list) { r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; } },
    update(states, op = {}) {
      const [sx0, sy0, sx1, sy1] = stage.bounds;
      const padding = (op.padding == null ? 70 : op.padding) * e;
      const visible = [];
      list.forEach((r, i) => {
        const s = states[i] || {};
        const o = clamp(s.opacity == null ? 1 : s.opacity);
        if (!s.point || o <= 0.001) { r.el.style.opacity = '0'; r.line.setAttribute('opacity', '0'); r.dot.setAttribute('opacity', '0'); return; }
        if (!r.w) { r.w = r.el.offsetWidth; r.h = r.el.offsetHeight; }
        if (s.point.isVector3) v.copy(s.point); else v.set(s.point[0], s.point[1], s.point[2]);
        v.project(stage.camera);
        if (v.z > 1 || v.z < -1) { r.el.style.opacity = '0'; r.line.setAttribute('opacity', '0'); r.dot.setAttribute('opacity', '0'); return; }
        const ax = (v.x * 0.5 + 0.5) * W, ay = (-v.y * 0.5 + 0.5) * H;
        const outside = Math.max(sx0 - ax, ax - sx1, sy0 - ay, ay - sy1, 0);
        const oo = o * (1 - clamp(outside / (40 * e)));
        if (oo <= 0.001) { r.el.style.opacity = '0'; r.line.setAttribute('opacity', '0'); r.dot.setAttribute('opacity', '0'); return; }
        visible.push({ r, o: oo, ax, ay, x: 0, y: 0 });
      });
      const dir = visible.filter((q) => q.r.side === 'right'), leftInset = visible.filter((q) => q.r.side === 'left');
      const rightColumn = op.column && dir.length ? Math.max(...dir.map((q) => q.ax)) + padding : null;
      const leftColumn = op.column && leftInset.length ? Math.min(...leftInset.map((q) => q.ax)) - padding : null;
      for (const q of visible) {
        const { r } = q;
        if (r.side === 'above') { q.x = q.ax - r.w / 2; q.y = q.ay - padding - r.h; } else if (r.side === 'bottom') { q.x = q.ax - r.w / 2; q.y = q.ay + padding; } else if (r.side === 'left') { q.x = (leftColumn != null ? leftColumn : q.ax - padding) - r.w; q.y = q.ay - r.h / 2; } else { q.x = rightColumn != null ? rightColumn : q.ax + padding; q.y = q.ay - r.h / 2; }
        q.x = clamp(q.x, sx0, sx1 - r.w);
        q.y = clamp(q.y, sy0, sy1 - r.h);
      }
      visible.sort((a, b) => a.y - b.y);
      const gap = 16 * e;
      for (let i = 1; i < visible.length; i++) {
        for (let j = 0; j < i; j++) {
          const A = visible[j], B = visible[i];
          const overlapsX = B.x < A.x + A.r.w && A.x < B.x + B.r.w;
          if (overlapsX && B.y < A.y + A.r.h + gap) B.y = A.y + A.r.h + gap;
        }
      }
      const excess = visible.length ? Math.max(0, Math.max(...visible.map((q) => q.y + q.r.h)) - sy1) : 0;
      for (const q of visible) {
        q.y = Math.max(sy0, q.y - excess);
        const { r } = q;
        r.el.style.transform = `translate(${q.x.toFixed(1)}px, ${q.y.toFixed(1)}px)`;
        r.el.style.opacity = q.o.toFixed(3);
        let lx = q.x, ly = q.y + r.h / 2;
        if (r.side === 'above') { lx = q.x + r.w / 2; ly = q.y + r.h; } else if (r.side === 'bottom') { lx = q.x + r.w / 2; ly = q.y; } else if (q.x + r.w / 2 < q.ax) { lx = q.x + r.w; }
        r.line.setAttribute('x1', q.ax.toFixed(1)); r.line.setAttribute('y1', q.ay.toFixed(1));
        r.line.setAttribute('x2', lx.toFixed(1)); r.line.setAttribute('y2', ly.toFixed(1));
        r.line.setAttribute('opacity', q.o.toFixed(3));
        r.dot.setAttribute('cx', q.ax.toFixed(1)); r.dot.setAttribute('cy', q.ay.toFixed(1));
        r.dot.setAttribute('opacity', q.o.toFixed(3));
      }
    },
  };
}
