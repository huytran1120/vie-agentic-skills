---
name: threejs-gltf-loading
description: >
  Load glTF/GLB models in three.js with GLTFLoader and play their skinned
  animations with AnimationMixer, including DRACO/Meshopt-compressed meshes and
  KTX2 textures. Use when importing 3D models into three.js — when the user
  mentions glTF, GLB, GLTFLoader, AnimationMixer, animation clips, DRACOLoader, or
  "load a 3D model". For scene/camera/renderer setup use threejs-scene-setup; for
  materials and lights use threejs-materials-lighting.
---

# three.js glTF Loading

Load `.gltf`/`.glb` models and play their animations in three.js, including
compressed geometry (DRACO/Meshopt) and textures (KTX2). Patterns target
**r186**; preserve an existing project's pinned release unless migration is requested.

## When to use

- Use to import a 3D model, add it to the scene, inspect its node hierarchy, and
  play baked/skinned animation clips with an `AnimationMixer`.
- Use when files are `.gltf`/`.glb`, or code imports `GLTFLoader` /
  `DRACOLoader` / `KTX2Loader` from `three/addons/loaders/...`.

**When *not* to use:** creating the renderer/camera/loop → `threejs-scene-setup`.
Tuning surface look, lights, or shadows on the loaded model →
`threejs-materials-lighting`. Authoring/exporting the model itself (Blender) is out
of scope; prefer glTF over OBJ/FBX for runtime.

## Core workflow

1. **Why glTF.** It's a transmission format: binary vertex data, PBR materials, and
   animations are ready to render with minimal parsing. Prefer it over OBJ (no scene
   graph, no animation) and FBX (heavy) for the web.
2. **Load with `GLTFLoader`.** `loader.load(url, onLoad, onProgress, onError)`. The
   result `gltf` has `gltf.scene` (the `Object3D` root), `gltf.animations`
   (`AnimationClip[]`), `gltf.cameras`, and `gltf.asset`.
3. **Add `gltf.scene` to your scene** and frame it. Inspect the hierarchy with
   `traverse` / `getObjectByName` to find the parts you'll control.
4. **Play animations with an `AnimationMixer`.** One mixer per animated root;
   `mixer.clipAction(clip).play()`; advance with `mixer.update(delta)` every frame.
5. **Decode compressed assets.** Attach a `DRACOLoader`, a `KTX2Loader`, and/or
   the Meshopt decoder so DRACO meshes, KTX2 textures, and meshopt-compressed
   buffers load. Since r185 the DRACO and KTX2 loaders find their bundled
   decoder files on their own.
6. **Validate changed glTF files when the project already has the tool.** Run
   `gltf-transform validate path/to/model.glb` for each changed `.gltf` or `.glb`;
   fix reported errors before loading.
7. **Verify what loaded** — log the scene graph and `gltf.animations`, and confirm
   the model is visible (right scale, lit) and the clip actually plays.

## Patterns

### 1. Load a model and frame it

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load(
  'assets/robot.glb',
  (gltf) => {
    const root = gltf.scene;
    scene.add(root);
    // Inspect: gltf.animations is an array of AnimationClip.
    console.log('clips:', gltf.animations.map((c) => c.name));
  },
  (event) => {
    // total is 0 when the server sends no Content-Length (e.g. compressed responses)
    if (event.total) console.log(`${(event.loaded / event.total) * 100}% loaded`);
  },
  (error) => console.error('glTF load failed:', error)
);
```

### 2. Play a skinned animation with AnimationMixer

```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

let mixer;                                  // declare outside so the loop can see it
const timer = new THREE.Timer();            // THREE.Clock is deprecated since r183

new GLTFLoader().load('assets/character.glb', (gltf) => {
  scene.add(gltf.scene);
  mixer = new THREE.AnimationMixer(gltf.scene);          // one mixer per animated root
  const clip = THREE.AnimationClip.findByName(gltf.animations, 'Run')
            ?? gltf.animations[0];
  mixer.clipAction(clip).play();
});

renderer.setAnimationLoop((time) => {
  timer.update(time);
  const dt = timer.getDelta();
  if (mixer) mixer.update(dt);              // advance the animation by real seconds
  renderer.render(scene, camera);
});
```

### 3. Cross-fade between two clips

```js
const actions = {};
mixer = new THREE.AnimationMixer(gltf.scene);
for (const clip of gltf.animations) {
  actions[clip.name] = mixer.clipAction(clip);
}
let current = actions['Idle'];
current.play();

function transitionTo(name, duration = 0.3) {
  const next = actions[name];
  if (!next || next === current) return;
  next.reset().play();                      // rewind and clear any old fade
  current.crossFadeTo(next, duration, false); // fade the old one out, new one in
  current = next;
}
```

### 4. DRACO-compressed geometry

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader, DRACO_GLTF_CONFIG } from 'three/addons/loaders/DRACOLoader.js';

// r185+: DRACOLoader finds the decoder that ships next to it in
// three/examples/jsm/libs/draco/, so no path is required. DRACO_GLTF_CONFIG
// (also r185+) selects the smaller glTF-only WASM build in libs/draco/gltf/.
const draco = new DRACOLoader().setDecoderPath(DRACO_GLTF_CONFIG);

const loader = new GLTFLoader();
loader.setDRACOLoader(draco);              // share one DRACOLoader across loads
loader.load('assets/city-draco.glb', (gltf) => scene.add(gltf.scene));
```

On releases before r185, or when your host does not serve those files, pass a
folder instead: `draco.setDecoderPath('/decoders/draco/')` with the files copied
from the same `three` version.

### 5. Find and animate a named part

```js
const timer = new THREE.Timer();

new GLTFLoader().load('assets/car.glb', (gltf) => {
  scene.add(gltf.scene);
  const wheels = [];
  gltf.scene.traverse((node) => {
    if (node.name.startsWith('Wheel')) wheels.push(node);
  });
  renderer.setAnimationLoop((time) => {
    timer.update(time);
    const dt = timer.getDelta();
    for (const w of wheels) w.rotation.x += dt * 4;
    renderer.render(scene, camera);
  });
});
```

## Pitfalls

- **Model loads but is invisible** → it has lit (PBR) materials and the scene has no
  light or environment. Add a light or `scene.environment` (see
  `threejs-materials-lighting`), and check scale — glTF is in metres, so a 0.01-scaled
  asset is tiny.
- **`load` is async** → `gltf` only exists inside the callback; declare `mixer`/refs
  outside and assign them in the callback, or use `await loader.loadAsync(url)`.
- **Animation never moves** → you didn't call `mixer.update(delta)` each frame, or you
  passed milliseconds instead of seconds (use `timer.getDelta()` after
  `timer.update(time)`), or you forgot
  `action.play()`.
- **DRACO/KTX2 model fails, or the network tab shows a 404 for `draco_*`/`basis_*`
  files** → the decoder/transcoder files are not being served, or come from a
  different three.js version. Since r185 the loaders default to the copies inside
  `three/examples/jsm/libs/`; if your bundler or host doesn't serve those, copy the
  folders from the installed `three` and point `setDecoderPath`/`setTranscoderPath`
  at them.
- **`setKTX2Loader must be called before loading KTX2 textures`** or
  **`setMeshoptDecoder must be called before loading compressed files`** → the
  asset uses `KHR_texture_basisu` or meshopt compression (`EXT_`/`KHR_meshopt_compression`);
  attach the missing decoder (see the reference).
- **Multiple mixers fighting** → use **one** `AnimationMixer` per animated root and
  create all actions from it; don't make a new mixer per clip.
- **Baked-in transforms surprise you** → exporters sometimes bake scale/rotation onto
  child nodes. Dump the hierarchy (names + position/rotation/scale) before relying on
  a node's local transform; re-export from the source if the rig is unusable.
- **Origins are off** → re-parent a part under a fresh `Object3D` to give it a clean
  pivot rather than fighting baked offsets.

## References

- For the full decode/transcode setup (DRACO + Meshopt + KTX2 together), `loadAsync`
  + a `LoadingManager` progress bar, reusing models with `SkeletonUtils.clone`, and
  exporter guidance (apply transforms, one clean root), read
  `references/loaders-and-animation.md`.

## Related skills

- `threejs-scene-setup` — the renderer, camera, and loop this model renders into.
- `threejs-materials-lighting` — lighting/environment so PBR models look right.
- `fps-shooter` — a 3D genre that composes three.js skills.


## VAS installation notes

Imported from gamedev-skills/awesome-gamedev-agent-skills at
`19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9`, Apache-2.0.
Copyright 2026 Abhishek Barali and the awesome-gamedev-agent-skills contributors.
The complete upstream LICENSE and NOTICE accompany this standalone skill.
Third-party notices, including the Go-Fonts license where provided, remain intact.
Only documented VAS naming, router-path adaptations and these notes differ;
supporting files and executable modes are preserved.

Use Copy Agent Prompt in the VAS catalog or `./vas install <canonical-id> --target <agent>`.
VAS uses its existing agent-folder mapping and CLI-compatible receipt. Installing
a skill only copies/links its payload; it never runs bundled Python/Luau/Go code,
installs engines, SDKs, packages, plugins or MCP servers, connects accounts,
generates assets through paid services, uploads builds or publishes a game.
Review code and request permission before installation, execution, downloads,
external services, private-data submission, purchases or publishing.

Respect the existing project's pinned engine/dependency versions. Baselines in
the upstream runbooks are snapshots, not claims about the newest release.
Actual use may need the matching engine, Go/.NET/Luau/Node toolchain, SDK,
hardware or platform account. create-game-assets' optional image helpers need
Pillow>=10,<14; no Pillow or other runtime dependency is installed automatically.
Generated Ebitengine projects fetch their own Go modules only with approval;
the bundled Go-Fonts notice does not change the license of this runbook.
Storefront publishing, signing credentials and paid asset generation are separate,
explicitly authorized actions. Missing prerequisites or failed commands are errors,
not evidence that a game works or has shipped.

Collection names performance-optimization and godot-export mean VAS canonical IDs
gamedev-performance-optimization and gamedev-godot-export respectively, not the
unrelated existing application-performance or Blender-export skills.
Other source skill names retain their canonical IDs and installed folder names.
Cross-skill composition recommendations do not imply that other independent
skills or external tools have been installed. Each specialized skill includes
its own complete local references, helpers and assets. For automatic selection
across the collection, the separately installable router includes all 77 original
specialized payloads as read-only companions under bundled/skills/, with
RUNBOOK.md filenames rather than additional auto-discovered SKILL.md files.
Read only the selected companion and its references on demand; never execute
its helpers automatically. Bundled companions are references, not extra catalog
records or separately registered agent skills. External engines, documentation,
SDKs, services and generated project's dependencies remain separate prerequisites.
