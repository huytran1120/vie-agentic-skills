import { THREE } from './three.mjs';
import { material, shade } from './materials.mjs';
function drawingContours(lines, fontCss, fontSizePx, lineHeight) {
  const cv = document.createElement('canvas');
  const g = cv.getContext('2d', { willReadFrequently: true });
  g.font = fontCss;
  const width = Math.max(...lines.map((l) => g.measureText(l).width));
  const pad = Math.ceil(fontSizePx * 0.3);
  const lh = Math.ceil(fontSizePx * lineHeight);
  const W = Math.ceil(width) + pad * 2;
  const H = lh * lines.length + pad * 2;
  cv.width = W;
  cv.height = H;
  g.font = fontCss;
  g.fillStyle = '#ffffff';
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  lines.forEach((l, i) => g.fillText(l, W / 2, pad + lh * (i + 0.5)));
  const px = g.getImageData(0, 0, W, H).data;
  const v = new Float32Array(W * H);
  for (let i = 0; i < W * H; i++) v[i] = px[i * 4 + 3] / 255;
  const iso = 0.5;
  const next = new Int32Array(2 * W * H).fill(-1);
  const pointX = new Float32Array(2 * W * H);
  const pointY = new Float32Array(2 * W * H);
  const idH = (x, y) => 2 * (y * W + x);
  const idV = (x, y) => 2 * (y * W + x) + 1;
  const point = (id) => {
    if (pointX[id] !== 0 || pointY[id] !== 0) return;
    const k = id >> 1;
    const x = k % W;
    const y = (k - x) / W;
    if ((id & 1) === 0) { const a = v[y * W + x], b = v[y * W + x + 1]; pointX[id] = x + (iso - a) / (b - a); pointY[id] = y; } else { const a = v[y * W + x], b = v[(y + 1) * W + x]; pointX[id] = x; pointY[id] = y + (iso - a) / (b - a); }
  };
  const link = (start, end) => { next[start] = end; point(start); point(end); };
  for (let y = 0; y < H - 1; y++) {
    for (let x = 0; x < W - 1; x++) {
      const a = v[y * W + x] > iso, b = v[y * W + x + 1] > iso, c = v[(y + 1) * W + x + 1] > iso, d = v[(y + 1) * W + x] > iso;
      const caseIndex = (a ? 8 : 0) | (b ? 4 : 0) | (c ? 2 : 0) | (d ? 1 : 0);
      if (caseIndex === 0 || caseIndex === 15) continue;
      const T = idH(x, y), B = idH(x, y + 1), L = idV(x, y), R = idV(x + 1, y);
      const middle = (v[y * W + x] + v[y * W + x + 1] + v[(y + 1) * W + x + 1] + v[(y + 1) * W + x]) / 4 > iso;
      switch (caseIndex) {
        case 1: link(L, B); break;
        case 2: link(B, R); break;
        case 3: link(L, R); break;
        case 4: link(R, T); break;
        case 5: if (middle) { link(L, T); link(R, B); } else { link(L, B); link(R, T); } break;
        case 6: link(B, T); break;
        case 7: link(L, T); break;
        case 8: link(T, L); break;
        case 9: link(T, B); break;
        case 10: if (middle) { link(T, R); link(B, L); } else { link(T, L); link(B, R); } break;
        case 11: link(T, R); break;
        case 12: link(R, L); break;
        case 13: link(R, B); break;
        case 14: link(B, L); break;
        default: break;
      }
    }
  }
  const returns = [];
  for (let id = 0; id < next.length; id++) {
    if (next[id] < 0) continue;
    const pts = [];
    let k = id;
    let store = 0;
    while (k >= 0 && store++ < 4000000) {
      pts.push([pointX[k], pointY[k]]);
      const n = next[k];
      next[k] = -1;
      k = n;
      if (k === id) break;
    }
    if (pts.length >= 3) returns.push(pts);
  }
  return { returns, W, H };
}

function simplify(pts, eps) {
  if (pts.length < 8) return pts;
  let far = 0, dmax = -1;
  for (let i = 1; i < pts.length; i++) {
    const d = (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2;
    if (d > dmax) { dmax = d; far = i; }
  }
  const rdp = (arr) => {
    const out = [arr[0]];
    const stack = [[0, arr.length - 1]];
    const keep = new Uint8Array(arr.length);
    keep[0] = keep[arr.length - 1] = 1;
    while (stack.length) {
      const [i0, i1] = stack.pop();
      const [x0, y0] = arr[i0], [x1, y1] = arr[i1];
      const dx = x1 - x0, dy = y1 - y0, n = Math.hypot(dx, dy) || 1e-9;
      let im = -1, dm = eps;
      for (let i = i0 + 1; i < i1; i++) {
        const d = Math.abs(dy * arr[i][0] - dx * arr[i][1] + x1 * y0 - y1 * x0) / n;
        if (d > dm) { dm = d; im = i; }
      }
      if (im >= 0) { keep[im] = 1; stack.push([i0, im], [im, i1]); }
    }
    for (let i = 1; i < arr.length; i++) if (keep[i]) out.push(arr[i]);
    return out;
  };
  const a = rdp(pts.slice(0, far + 1));
  const b = rdp(pts.slice(far).concat([pts[0]]));
  return a.concat(b.slice(1, -1));
}

const areaOf = (p) => { let s = 0; for (let i = 0, j = p.length - 1; i < p.length; j = i++) s += (p[j][0] + p[i][0]) * (p[j][1] - p[i][1]); return s / 2; };
const inside = (pt, p) => {
  let c = false;
  for (let i = 0, j = p.length - 1; i < p.length; j = i++) {
    if ((p[i][1] > pt[1]) !== (p[j][1] > pt[1]) && pt[0] < ((p[j][0] - p[i][0]) * (pt[1] - p[i][1])) / (p[j][1] - p[i][1]) + p[i][0]) c = !c;
  }
  return c;
};

export async function volumeText(text, { font = 'Montserrat', weight = 900, fontSizePx = 260, height = 1, thickness = 0.3, bevel = 0.02,
  lineHeight = 1.05, color = '#665080', sides = null, roughness = 0.4, metal = 0, clearcoat = 0.5 } = {}) {
  const css = `${weight} ${fontSizePx}px ${font}`;
  try { await document.fonts.load(css, text); } catch { /* Use the available fallback font. */ }
  if (document.fonts && !document.fonts.check(css, text)) console.warn(`[scene 3D] font ${font} did not load; text will use a fallback`);
  const lines = String(text).split('\n');
  const { returns } = drawingContours(lines, css, fontSizePx, lineHeight);
  const scale = height / fontSizePx;
  const polygons = returns.map((p) => simplify(p, 0.35)).filter((p) => p.length >= 3 && Math.abs(areaOf(p)) > 4);
  if (!polygons.length) throw new Error(`could not draw text "${text}"`);
  let larger = polygons[0];
  for (const p of polygons) if (Math.abs(areaOf(p)) > Math.abs(areaOf(larger))) larger = p;
  const outsideSign = Math.sign(areaOf(larger));
  const outside = polygons.filter((p) => Math.sign(areaOf(p)) === outsideSign);
  const holes = polygons.filter((p) => Math.sign(areaOf(p)) !== outsideSign);
  const turn = (p) => p.map(([x, y]) => new THREE.Vector2(x * scale, -y * scale));
  const shapes = outside.map((p) => ({ p, s: new THREE.Shape(turn(p)), a: Math.abs(areaOf(p)) }));
  for (const f of holes) {
    const owner = shapes.filter((o) => inside(f[0], o.p)).sort((a, b) => a.a - b.a)[0];
    if (owner) owner.s.holes.push(new THREE.Path(turn(f)));
  }
  const ch = Math.max(0.001, bevel * height);
  const geometry = new THREE.ExtrudeGeometry(shapes.map((o) => o.s), { depth: Math.max(0.001, thickness * height - 2 * ch), bevelEnabled: true,
    bevelThickness: ch, bevelSize: ch, bevelSegments: 2, curveSegments: 1 });
  geometry.computeBoundingBox();
  const bb = geometry.boundingBox;
  geometry.translate(-(bb.min.x + bb.max.x) / 2, -bb.min.y, -(bb.min.z + bb.max.z) / 2);
  geometry.computeVertexNormals();
  const front = material(color, { roughness, metal, clearcoat });
  const side = sides ? material(sides, { roughness, metal, clearcoat }) : front;
  return shade(new THREE.Mesh(geometry, [front, side]));
}
