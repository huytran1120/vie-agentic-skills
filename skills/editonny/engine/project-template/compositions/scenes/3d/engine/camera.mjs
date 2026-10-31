import { THREE } from './three.mjs';
import { mix } from './time.mjs';
export function orbit(camera, pose) {
  const a = (pose.azim * Math.PI) / 180;
  const e = (pose.elev * Math.PI) / 180;
  const [x, y, z] = pose.target || [0, 0, 0];
  camera.position.set(x + pose.dist * Math.cos(e) * Math.sin(a), y + pose.dist * Math.sin(e), z + pose.dist * Math.cos(e) * Math.cos(a));
  camera.lookAt(x, y, z);
  camera.updateMatrixWorld();
}

export function mixPose(p0, p1, k) {
  const a0 = p0.target || [0, 0, 0];
  const a1 = p1.target || a0;
  return {
    target: [mix(a0[0], a1[0], k), mix(a0[1], a1[1], k), mix(a0[2], a1[2], k)],
    dist: mix(p0.dist, p1.dist == null ? p0.dist : p1.dist, k),
    azim: mix(p0.azim, p1.azim == null ? p0.azim : p1.azim, k),
    elev: mix(p0.elev, p1.elev == null ? p0.elev : p1.elev, k),
  };
}
export function frameCamera(camera, W, H, area) {
  if (!area) { camera.clearViewOffset(); return; }
  const cx = (area[0] + area[2]) / 2;
  const cy = (area[1] + area[3]) / 2;
  camera.setViewOffset(W, H, W / 2 - cx, H / 2 - cy, W, H);
}
export function sphereDistance(camera, radius, H, area, padding = 1.12) {
  const t = Math.tan((camera.fov * Math.PI) / 360);
  const ah = area[3] - area[1];
  const aw = area[2] - area[0];
  const k = t * Math.min(ah, aw) / H;
  return (radius * padding) / k;
}
export function boxDistance(camera, width, height, H, area, padding = 1.1) {
  const t = Math.tan((camera.fov * Math.PI) / 360);
  const ah = area[3] - area[1];
  const aw = area[2] - area[0];
  return Math.max((height / 2) * padding / (t * ah / H), (width / 2) * padding / (t * aw / H));
}
export function fittingDistance(camera, W, H, area, box, pose, padding = 1.08) {
  const corners = [];
  for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) corners.push(new THREE.Vector3(x, y, z));
  const cx = (area[0] + area[2]) / 2, cy = (area[1] + area[3]) / 2;
  const hw = (area[2] - area[0]) / 2 / padding, hh = (area[3] - area[1]) / 2 / padding;
  const v = new THREE.Vector3();
  const fits = (d) => {
    orbit(camera, { ...pose, dist: d });
    for (const c of corners) {
      v.copy(c).project(camera);
      if (v.z > 1 || v.z < -1) return false;
      if (Math.abs((v.x * 0.5 + 0.5) * W - cx) > hw || Math.abs((-v.y * 0.5 + 0.5) * H - cy) > hh) return false;
    }
    return true;
  };
  let lo = camera.near, hi = 1;
  while (!fits(hi) && hi < 1e4) hi *= 2;
  for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (fits(m)) hi = m; else lo = m; }
  return hi;
}
