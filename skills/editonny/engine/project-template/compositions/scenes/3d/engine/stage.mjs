import { THREE, REVISION } from './three.mjs';
import { RoomEnvironment } from '../../../../assets/three/RoomEnvironment.js';
import { clamp } from './time.mjs';
import { frameCamera, orbit, sphereDistance, boxDistance, fittingDistance } from './camera.mjs';
import { gridTexture, spotTexture, plate, box, cylinder, material } from './materials.mjs';
import { volumeText } from './text.mjs';
import { createLabels } from './labels.mjs';
import { mediaTexture, loadModel } from './media.mjs';
function showFailure(layer, text) {
  if (!layer) return;
  const el = document.createElement('div');
  el.textContent = text;
  el.style.cssText = 'position:absolute;left:60px;right:60px;top:40%;padding:28px;border-radius:20px;background:#fff;color:#b00020;'
    + 'font:700 34px/1.25 Montserrat,sans-serif;box-shadow:0 0 0 6px #b00020;opacity:1';
  layer.appendChild(el);
}
export async function initialize(options) {
  const { id, C, canvas, layer } = options;
  const t0 = performance.now();
  const state = (window.__scene3d = window.__scene3d || {})[id] = { ready: false, warnings: [], revision: REVISION };
  const fail = (msg) => {
    state.error = msg;
    console.error(`[scene 3D ${id}] ${msg}`);
    showFailure(layer, `3D scene "${id}" failed to build: ${msg}`);
    return () => {};
  };
  const W = C.width || 1080, H = C.height || 1920;
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: options.background == null || !!options.cutout, preserveDrawingBuffer: true,
      powerPreference: 'high-performance' });
  } catch (e) {
    return fail(`WebGL failed in this browser (${e && e.message ? e.message : e}). See references/3d.md.`);
  }
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.shadowMap.enabled = options.shadows !== false;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const gl = renderer.getContext();
  const info = gl.getExtension('WEBGL_debug_renderer_info');
  state.plate = info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
  const scene = new THREE.Scene();
  if (options.background != null) scene.background = new THREE.Color(options.background);
  else renderer.setClearColor(0x000000, 0);
  const clipInset = options.cutout;
  if (clipInset) {
    const r = Math.round(36 * Math.min(W, H) / 1080);
    canvas.style.clipPath = `inset(${clipInset[1]}px ${W - clipInset[2]}px ${H - clipInset[3]}px ${clipInset[0]}px round ${r}px)`;
  }
  if (options.environment !== false) {
    const pm = new THREE.PMREMGenerator(renderer);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = options.environment === true || options.environment == null ? 0.55 : Number(options.environment);
    pm.dispose();
  }
  const camera = new THREE.PerspectiveCamera(options.fov || 30, W / H, 0.05, 400);
  const area = options.area || C.safeArea || [0, 0, W, H];
  frameCamera(camera, W, H, area);
  const root = options.root || document.baseURI;
  const solids = [];
  const textures = [];
  const stage = {
    THREE, renderer, scene, camera, W, H, C, area, bounds: options.bounds || area, colors: C.colors, scale: Math.min(W, H) / 1080,
    transparent: options.background == null,
    url: (path) => new URL(path, root).href,
    solid(obj, name) { solids.push({ obj, name: name || obj.name || 'object' }); return obj; },
    lights({ key = [4, 9, 6], intensity = 2.6, target = [0, 0.5, 0], area: size = 6, rim = 0.9, sky = 0.7 } = {}) {
      const hemi = new THREE.HemisphereLight('#ffffff', C.colors.base, sky);
      scene.add(hemi);
      const k = new THREE.DirectionalLight('#ffffff', intensity);
      k.position.set(...key);
      k.target.position.set(...target);
      k.castShadow = stage.renderer.shadowMap.enabled;
      k.shadow.mapSize.set(2048, 2048);
      Object.assign(k.shadow.camera, { left: -size, right: size, top: size, bottom: -size, near: 0.5, far: 60 });
      k.shadow.bias = -0.0004;
      k.shadow.normalBias = 0.02;
      k.shadow.radius = 4;
      scene.add(k, k.target);
      const r = new THREE.DirectionalLight('#ffffff', rim);
      r.position.set(-key[0] * 0.8, key[1] * 0.6, -Math.abs(key[2]) - 4);
      scene.add(r);
      return { hemi, key: k, rim: r };
    },
    floor({ size = 24, steps = 24, grid = options.background != null, shadow = 0.22, y = 0 } = {}) {
      const g = new THREE.Group();
      if (grid) {
        const map = gridTexture(C.colors.line, steps);
        map.anisotropy = renderer.capabilities.getMaxAnisotropy();
        const m = new THREE.MeshBasicMaterial({ map: map, transparent: true, depthWrite: false });
        const p = new THREE.Mesh(new THREE.PlaneGeometry(size, size), m);
        p.rotation.x = -Math.PI / 2;
        p.position.y = y + 0.0005;
        p.renderOrder = -2;
        g.add(p);
      }
      const s = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.ShadowMaterial({ opacity: shadow }));
      s.rotation.x = -Math.PI / 2;
      s.position.y = y + 0.001;
      s.receiveShadow = true;
      s.renderOrder = -1;
      g.add(s);
      scene.add(g);
      return g;
    },
    contactShadow({ width = 1, depth = 1, intensity = 0.45, y = 0 } = {}) {
      const m = new THREE.MeshBasicMaterial({ map: spotTexture(), transparent: true, opacity: intensity, depthWrite: false, color: '#000000' });
      const p = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), m);
      p.rotation.x = -Math.PI / 2;
      p.position.y = y + 0.002;
      p.renderOrder = -1;
      scene.add(p);
      return {
        mesh: p,
        place(x, z, heightAbove = 0, extraScale = 1, angleY = 0) {
          const k = 1 + heightAbove * 0.6;
          p.position.set(x, y + 0.002, z);
          p.rotation.set(-Math.PI / 2, 0, angleY);
          p.scale.set(width * 1.25 * k * extraScale, depth * 1.25 * k * extraScale, 1);
          m.opacity = intensity / (1 + heightAbove * 2.2);
        },
      };
    },
    plate, box, cylinder, material, volumeText,
    loadModel: (path, op) => loadModel(stage.url(path), op),
    mediaTexture(el, op) { const t = mediaTexture(el, op); textures.push(t); return t; },
    labels: (items) => createLabels(stage, layer, items),
    orbit: (pose) => orbit(camera, pose),
    sphereDistance: (radius, padding) => sphereDistance(camera, radius, H, area, padding),
    boxDistance: (width, height, padding) => boxDistance(camera, width, height, H, area, padding),
    fittingDistance: (box, pose, padding) => fittingDistance(camera, W, H, area, box, pose, padding),
  };
  try { await document.fonts.load(`800 ${Math.round(36 * stage.scale)}px Montserrat`); } catch { /* Use the available fallback font. */ }
  let update;
  try {
    update = await options.build(stage);
  } catch (e) {
    return fail(`failed to build objects: ${e && e.message ? e.message : e}`);
  }
  const DUR = C.duration || 5;
  const objectBounds = new THREE.Box3();
  const padding = camera.near + 0.03;
  const seen = new Set();
  for (let f = 0; f <= Math.ceil(DUR * 30); f++) {
    const t = Math.min(DUR, f / 30);
    update(t);
    for (const s of solids) {
      objectBounds.setFromObject(s.obj).expandByScalar(padding);
      if (objectBounds.containsPoint(camera.position) && !seen.has(s.name)) {
        seen.add(s.name);
        const msg = `camera enters "${s.name}" at ${t.toFixed(2)} s: move the camera away or change its path`;
        state.warnings.push(msg);
        console.error(`[scene 3D ${id}] ${msg}`);
      }
    }
  }
  const draw = (t) => {
    const tt = clamp(Number(t) || 0, 0, DUR);
    state.t = tt;
    update(tt);
    for (const tx of textures) tx.update();
    if (clipInset) {
      renderer.setScissorTest(false);
      renderer.setClearColor(0x000000, 0);
      renderer.clear();
      renderer.setScissorTest(true);
      renderer.setScissor(clipInset[0], H - clipInset[3], clipInset[2] - clipInset[0], clipInset[3] - clipInset[1]);
    }
    renderer.render(scene, camera);
  };
  state.ready = true;
  state.buildMs = Math.round(performance.now() - t0);
  state.draw = draw;
  return draw;
}
