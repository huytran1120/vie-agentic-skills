---
name: shader-programming
description: >
  Write game shaders from cross-engine fundamentals — the vertex→fragment
  pipeline, coordinate spaces, UV math, and common 2D/3D effects (tint, UV
  scroll, dissolve, outline, fresnel rim, vignette) in GLSL with HLSL
  equivalents. Use when the user mentions shaders, fragment/pixel shader, vertex
  shader, UV, GLSL, HLSL, or effects like dissolve, outline, or rim light.
---

# Shader programming (cross-engine)

Shaders are small programs that run **per vertex** and **per pixel** on the GPU.
The concepts — the pipeline, coordinate spaces, UVs, and how common effects are
built — port across engines; only the language dialect and built-in variable
names change. This skill teaches those portable fundamentals in GLSL with HLSL
equivalents; use `godot-shaders` (or Unity/Unreal material docs) for the exact
engine syntax and built-ins.

## When to use

- Use to understand or write vertex/fragment shaders and to reason about UVs,
  coordinate spaces, and the GPU pipeline.
- Use to build common effects: tint/recolor, scrolling textures, dissolve,
  outlines, fresnel/rim light, vignette, color grading.
- Use to translate a shader concept between GLSL and HLSL, or between engines.

**When *not* to use:** for an engine's exact shader language and built-ins, use
`godot-shaders` (Godot shading language) or the engine's material docs. For full
particle VFX systems, see `unreal-niagara`. For post-process *stacks*, defer to
the engine's renderer settings.

## Core workflow

1. **Know which stage you're in.** The **vertex** shader transforms each vertex
   into clip space and passes data (UVs, normals) onward; the **fragment/pixel**
   shader runs per rasterized pixel and outputs a color. Most game effects live
   in the fragment stage.
2. **Track coordinate spaces.** Positions move model → world → view → clip space;
   normals belong in world or view space. Mixing spaces is the most common bug.
3. **Drive effects with UVs and time.** UVs are `0..1` texture coordinates;
   offset, scale, or distort them, and animate with a `time` uniform.
4. **Work per pixel, branch-light.** Prefer `mix`, `step`, `smoothstep`, and
   `clamp` over `if` where possible; GPUs run pixels in lockstep, so a branch
   whose condition differs between neighbouring pixels runs both sides. A branch
   on a uniform (same for the whole draw) is cheap.
5. **Pass data via uniforms** (constant per draw) and **varyings** (interpolated
   vertex→fragment). Keep texture samples few; they dominate cost.
6. **Validate source before visual testing when the tools are already available.** For
   GLSL, run `glslangValidator path/to/shader.frag` with the matching stage suffix;
   for WGSL, run `naga path/to/shader.wgsl`. Check Godot `.gdshader` files by
   opening the project in Godot, which has no standalone validator for them.
7. **Verify visually and on target hardware.** Shaders that look right on desktop
   can break on mobile (precision, missing features). Test where it ships.

## Patterns

GLSL fragment snippets for desktop `#version 330` (each passes
`glslangValidator` with that header; close to Godot's `canvas_item`/`spatial`
shaders). For GLSL ES 3.00 — WebGL2, three.js `ShaderMaterial`, PixiJS filters —
add `precision highp float;` and set uniform defaults from code: ES rejects
`uniform float edge = 0.05;` with "cannot initialize this type of qualifier"
(Godot's shading language accepts it). See `references/effects.md` for the HLSL
equivalents and the full outline/fresnel/vignette shaders.

### 1. Fragment basics: sample, tint, and combine

```glsl
// Per-pixel: read the texture at this UV, multiply by a color (tint), keep alpha.
uniform sampler2D tex;
uniform vec4 tint;          // e.g. (1,0,0,1) reddens; multiply is non-destructive
in vec2 uv;                 // interpolated 0..1 texture coordinate (a "varying")
out vec4 frag;
void main() {
    vec4 c = texture(tex, uv);   // HLSL: tex.Sample(samp, uv)
    frag = c * tint;             // component-wise multiply tints without clipping
}
```

### 2. Scrolling UVs (animated texture) — frame-rate independent

```glsl
// Add time * speed to the UV to scroll. fract() wraps it into 0..1 so it tiles.
uniform sampler2D tex;
uniform float time;          // seconds, supplied by the engine
uniform vec2 scroll_speed;   // UV units per second, e.g. (0.1, 0.0)
in vec2 uv;
out vec4 frag;
void main() {
    vec2 scrolled = fract(uv + scroll_speed * time);  // HLSL: frac(...)
    frag = texture(tex, scrolled);
}
// Drive with a real time uniform, not a per-frame accumulator, so speed is stable.
```

### 3. Dissolve (threshold a noise map, glow the edge)

```glsl
// Hide pixels where noise < threshold; tint a thin band at the boundary.
uniform sampler2D tex;
uniform sampler2D noise_tex;     // grayscale noise, 0..1
uniform float amount;            // 0 = fully visible, 1 = fully dissolved
uniform float edge = 0.05;       // width of the glowing edge band
uniform vec4 edge_color;
in vec2 uv;
out vec4 frag;
void main() {
    vec4 c = texture(tex, uv);
    float n = texture(noise_tex, uv).r;
    float cut = amount * (1.0 + edge) - edge;  // edge band starts below 0 -> none at amount 0
    if (n <= cut) discard;                     // cut away dissolved pixels (all of them at 1)
    float e = smoothstep(cut, cut + edge, n);  // 0 at the edge -> 1 inside; keep edge > 0
    frag = mix(edge_color, c, e);              // HLSL: lerp(edge_color, c, e)
}
// WRONG: thresholding at `amount` directly — at amount 0 every pixel with
// n < edge is still tinted, so the "fully visible" sprite shows glowing specks.
```

### 4. Fresnel rim light (3D) — brighten glancing angles

```glsl
// Rim = 1 where the surface is edge-on to the camera (silhouette glow).
in vec3 world_normal;        // normalized, world space (from the vertex stage)
in vec3 view_dir;            // normalized, surface -> camera, world space
uniform float power = 3.0;
uniform vec3 rim_color;
out vec4 frag;
void main() {
    float f = pow(1.0 - clamp(dot(world_normal, view_dir), 0.0, 1.0), power);
    frag = vec4(rim_color * f, 1.0);   // add to lighting; f peaks at the silhouette
}
// Correctness: normal and view_dir MUST be in the same space and normalized.
```

## Pitfalls

- **Mixing coordinate spaces** (lighting a world-space normal against a
  view-space light) yields subtly wrong shading. Pick one space and convert
  everything into it.
- **Forgetting to normalize** interpolated normals/directions: interpolation
  shortens vectors, so `dot()` results drift. `normalize()` in the fragment stage.
- **UV assumptions across engines.** Some engines flip V (top-left vs bottom-left
  origin); a texture may appear upside-down. Know your engine's convention.
- **Heavy branching / dynamic loops** stall GPUs. Prefer `step`/`smoothstep`/
  `mix`; reserve `if`/`discard` for genuinely cheap early-outs.
- **`discard` defeats early-Z** and can hurt performance on tiled mobile GPUs;
  prefer alpha blending where you can.
- **Reversed `smoothstep` edges.** The GLSL spec leaves `smoothstep(e0, e1, x)`
  undefined when `e0 >= e1`, so `smoothstep(1.0, 0.5, d)` may work on one GPU
  and not another. Write `1.0 - smoothstep(0.5, 1.0, d)`.
- **Precision on mobile**: `highp` vs `mediump` matters; large UVs or time values
  in low precision shimmer. Use adequate precision for coordinates and time.
- **Assuming GLSL == HLSL.** `mix`↔`lerp`, `fract`↔`frac`, `texture()`↔`.Sample()`,
  `vec2`↔`float2`, `M * v`↔`mul(M, v)`, `mod`↔`fmod` (different for negatives).
  See the reference mapping.
- **A GLSL `ShaderMaterial` that renders nothing in three.js** under
  `WebGPURenderer`: that renderer only runs node materials (TSL), on its WebGPU
  and WebGL 2 backends alike. Keep `WebGLRenderer` for raw GLSL or port to TSL.

## References

- `references/effects.md` — full outline (2D sprite + 3D), vignette, and color
  grading shaders; the GLSL↔HLSL function/type mapping table; per-engine notes
  (Godot `canvas_item`/`spatial`, Unity ShaderLab/HLSL, Unreal material nodes).

## Related skills

- `godot-shaders` — Godot shading language syntax, built-ins, and screen-reading.
- `unreal-niagara` — GPU particle VFX (a different shader use).
- `procedural-gen` — the noise that drives dissolve and procedural texturing.


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
