import { THREE } from './three.mjs';
import { canvasTexture, shade } from './materials.mjs';
export function mediaTexture(el, { width = 1280, height = 720, focus = 0.4, fit = 'cover' } = {}) {
  const cv = document.createElement('canvas');
  cv.width = width;
  cv.height = height;
  const g = cv.getContext('2d', { willReadFrequently: true });
  g.fillStyle = '#000';
  g.fillRect(0, 0, width, height);
  const thumbnail = document.createElement('canvas');
  const gm = thumbnail.getContext('2d', { willReadFrequently: true });
  const tex = canvasTexture(cv);
  const font = () => {
    const sibling = el.nextElementSibling;
    if (sibling && sibling.classList && sibling.classList.contains('__render_frame__') && sibling.complete && sibling.naturalWidth > 0
      && sibling.style.visibility !== 'hidden') return sibling;
    if (el.tagName === 'VIDEO') return el.readyState >= 2 ? el : null;
    return el.complete && el.naturalWidth > 0 ? el : null;
  };
  return {
    texture: tex,
    update() {
      const f = font();
      if (!f) return false;
      const sw = f.videoWidth || f.naturalWidth, sh = f.videoHeight || f.naturalHeight;
      const kc = Math.max(width / sw, height / sh);
      if (fit === 'contain') {
        const km = 40 / Math.max(sw, sh);
        thumbnail.width = Math.max(2, Math.round(sw * km));
        thumbnail.height = Math.max(2, Math.round(sh * km));
        gm.drawImage(f, 0, 0, thumbnail.width, thumbnail.height);
        g.imageSmoothingEnabled = true;
        g.drawImage(thumbnail, (width - sw * kc) / 2, (height - sh * kc) / 2, sw * kc, sh * kc);
        g.fillStyle = 'rgba(0,0,0,0.45)';
        g.fillRect(0, 0, width, height);
        const ki = Math.min(width / sw, height / sh);
        g.drawImage(f, (width - sw * ki) / 2, (height - sh * ki) / 2, sw * ki, sh * ki);
      } else {
        g.drawImage(f, (width - sw * kc) / 2, (height - sh * kc) * focus, sw * kc, sh * kc);
      }
      tex.needsUpdate = true;
      return true;
    },
  };
}
export async function loadModel(url, { height = null, width = null } = {}) {
  const { GLTFLoader } = await import('../../../../assets/three/GLTFLoader.js');
  const gltf = await new GLTFLoader().loadAsync(url);
  const obj = gltf.scene;
  shade(obj);
  const box = new THREE.Box3().setFromObject(obj);
  const size = box.getSize(new THREE.Vector3());
  let k = 1;
  if (height) k = height / (size.y || 1);
  else if (width) k = width / (Math.max(size.x, size.z) || 1);
  obj.scale.setScalar(k);
  const c = box.getCenter(new THREE.Vector3());
  const category = new THREE.Group();
  obj.position.set(-c.x * k, -box.min.y * k, -c.z * k);
  category.add(obj);
  const mix = gltf.animations.length ? new THREE.AnimationMixer(obj) : null;
  if (mix) gltf.animations.forEach((a) => mix.clipAction(a).play());
  return { object: category, animations: gltf.animations, atTime: (t) => { if (mix) mix.setTime(t); } };
}
