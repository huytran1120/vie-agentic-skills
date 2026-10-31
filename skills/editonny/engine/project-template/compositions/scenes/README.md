# Custom scenes

Copy a built-in scene into this directory, give it a unique filename, and replace its template ID, composition ID, timeline registration, and DOM prefix together. Register it in `project.json`:

```json
{"scenes": [{"file": "compositions/scenes/example.html", "start": 2, "end": 7}]}
```

Every scene contains a `<template>`, one root with `data-composition-id`, `data-width`, `data-height`, and `data-duration`, and a paused GSAP timeline registered at `window.__timelines[id]`. Preserve the required HyperFrames attribute names. Two instances must use distinct IDs and DOM prefixes.

The build supplies `window.__scenes[id]` with `start`, `end`, `duration`, `width`, `height`, `safeArea`, `colors`, `backgroundCss`, `face`, `frame`, `words`, and `time`. Each word has `text`, `t`, and `end`. A framed layout has `frame.box`, `frame.freeArea`, and `frame.closedAt`; wait until it closes before drawing over the moving face. Scene time starts at zero. Never translate transcript words or user-provided text.

The 2D templates cover search, a gauge, diagrams, files, command entry, before/after comparisons, conversation, and notes. Edit their `PARAM` objects. Word anchors accept a string, seconds, or `{word, after, standard}` where `standard` is the standalone fallback time. `area: "aboveFace"` is supported by the small-card templates; inspect warnings if there is insufficient face clearance.

The 3D facade is `3d/three-scene.js`. It exports `initialize`, timing helpers, camera framing helpers, materials, `volumeText`, `mediaTexture`, and `loadModel`. Initialization takes `id`, `C`, `canvas`, `layer`, and `build(stage)`, which returns a deterministic `draw(time)` function. Never accumulate frame-to-frame state: seeking to the same time must produce the same frame. `window.__scene3d[id]` exposes readiness, warnings, revision, build time, and drawing diagnostics.

3D templates cover volume, exploded layers, a path, and a device screen. Runtime and licensed assets stay local. Review representative frames with `hf lint`, `hf check`, and a short render; structural checks alone do not prove every scene or format renders correctly.
