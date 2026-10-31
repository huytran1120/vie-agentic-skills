import { THREE } from './three.mjs';
export function canvasTexture(cv) {
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
export function gridTexture(lineColor, steps = 24, px = 1024) {
  const cv = document.createElement('canvas');
  cv.width = cv.height = px;
  const g = cv.getContext('2d');
  g.strokeStyle = lineColor;
  g.globalAlpha = 0.75;
  g.lineWidth = Math.max(2, px / 420);
  for (let i = 0; i <= steps; i++) {
    const p = Math.round((i / steps) * (px - 2)) + 1;
    g.beginPath(); g.moveTo(p, 0); g.lineTo(p, px); g.stroke();
    g.beginPath(); g.moveTo(0, p); g.lineTo(px, p); g.stroke();
  }
  g.globalCompositeOperation = 'destination-in';
  const r = g.createRadialGradient(px / 2, px / 2, px * 0.12, px / 2, px / 2, px / 2);
  r.addColorStop(0, 'rgba(0,0,0,1)');
  r.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = r;
  g.fillRect(0, 0, px, px);
  return canvasTexture(cv);
}

let _spotTexture = null;
export function spotTexture() {
  if (_spotTexture) return _spotTexture;
  const px = 256;
  const cv = document.createElement('canvas');
  cv.width = cv.height = px;
  const g = cv.getContext('2d');
  const r = g.createRadialGradient(px / 2, px / 2, 0, px / 2, px / 2, px / 2);
  r.addColorStop(0, 'rgba(0,0,0,1)');
  r.addColorStop(0.45, 'rgba(0,0,0,0.55)');
  r.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = r;
  g.fillRect(0, 0, px, px);
  _spotTexture = new THREE.CanvasTexture(cv);
  return _spotTexture;
}
export function material(color, { roughness = 0.5, metal = 0, clearcoat = 0.25 } = {}) {
  return new THREE.MeshPhysicalMaterial({ color: new THREE.Color(color), roughness: roughness, metalness: metal, clearcoat: clearcoat, clearcoatRoughness: 0.35 });
}

export function shade(obj) {
  obj.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return obj;
}

function roundedRectangle(w, d, r) {
  r = Math.max(0.001, Math.min(r, w / 2 - 0.001, d / 2 - 0.001));
  const s = new THREE.Shape();
  const x = -w / 2, y = -d / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y);
  s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + d - r);
  s.quadraticCurveTo(x + w, y + d, x + w - r, y + d);
  s.lineTo(x + r, y + d);
  s.quadraticCurveTo(x, y + d, x, y + d - r);
  s.lineTo(x, y + r);
  s.quadraticCurveTo(x, y, x + r, y);
  return s;
}
export function plate({ width = 2, height = 0.2, depth = 1.4, radius = 0.12, bevel = 0.03, color = '#c7b7ef', sides = null,
  roughness = 0.5, metal = 0, clearcoat = 0.25 } = {}) {
  const ch = Math.max(0.001, Math.min(bevel, height / 2 - 0.001, width / 4, depth / 4));
  const shape = roundedRectangle(width - 2 * ch, depth - 2 * ch, Math.max(0.002, radius - ch));
  const geometry = new THREE.ExtrudeGeometry(shape, { depth: Math.max(0.001, height - 2 * ch), bevelEnabled: true, bevelThickness: ch,
    bevelSize: ch, bevelSegments: 3, curveSegments: 10 });
  geometry.rotateX(-Math.PI / 2);
  geometry.translate(0, ch, 0);
  geometry.computeVertexNormals();
  const lid = material(color, { roughness, metal, clearcoat });
  const side = sides ? material(sides, { roughness, metal, clearcoat }) : lid;
  return shade(new THREE.Mesh(geometry, [lid, side]));
}

export function box(op = {}) {
  return plate({ width: 1, height: 1, depth: 1, radius: 0.1, bevel: 0.05, ...op });
}

export function cylinder({ radius = 0.5, height = 1, color = '#c7b7ef', segments = 48, roughness = 0.5, metal = 0, clearcoat = 0.25 } = {}) {
  const geometry = new THREE.CylinderGeometry(radius, radius, height, segments, 1);
  geometry.translate(0, height / 2, 0);
  return shade(new THREE.Mesh(geometry, material(color, { roughness, metal, clearcoat })));
}
