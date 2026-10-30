---
name: godot-shaders
description: >
  Write Godot 4.7 shaders in the Godot Shading Language: canvas_item shaders for 2D
  and spatial shaders for 3D, with vertex/fragment functions, uniforms (source_color,
  hint_range), TIME/UV animation, and screen-reading via hint_screen_texture. Use
  when authoring .gdshader files, writing fragment/vertex code, making 2D/3D visual
  effects, or porting 3.x shaders (SCREEN_TEXTURE, hint_color) to 4.x.
---

# Godot Shaders (4.x)

Write `canvas_item` (2D) and `spatial` (3D) shaders in the Godot Shading Language, animate
with `TIME`/`UV`, expose `uniform`s, and read the screen. Targets **Godot 4.7**.

## When to use

- Use when writing `.gdshader` code or a `ShaderMaterial`: 2D effects (outline, dissolve,
  flash, water), 3D surface shaders (rim light, toon, scrolling UV), or screen-space
  post effects.

**When *not* to use:** the cross-engine *concepts* of shading (UVs, vertex/fragment
theory) → `shader-programming`; particles/VFX nodes → general 3D; non-shader visuals.

## Core workflow

1. **Pick the shader type** on the first line: `shader_type canvas_item;` for 2D
   (Sprite2D, TextureRect, anything `CanvasItem`) or `shader_type spatial;` for 3D
   materials. (`particles`, `sky`, `fog` also exist.)
2. **Attach via a `ShaderMaterial`.** Create a `ShaderMaterial`, assign your `.gdshader`,
   and put it on the node's `material`. Uniforms appear in the Inspector.
3. **Write `fragment()`** to set the output: `COLOR` (2D) or `ALBEDO`/`EMISSION`/`ALPHA`
   (3D). Optionally `vertex()` to move geometry and `light()` for custom lighting.
4. **Expose tunables as `uniform`s** with hints (`source_color`, `hint_range`) so they are
   editable and correctly color-managed.
5. **Animate with the built-in `TIME`** and sample textures with `texture(tex, UV)`.
6. **Set uniforms from code** with `material.set_shader_parameter("name", value)`.

## Patterns

### 1. 2D (canvas_item): tint + scrolling UV

```glsl
shader_type canvas_item;

uniform vec4 tint : source_color = vec4(1.0);     // source_color = sRGB-correct color
uniform float scroll_speed : hint_range(0.0, 2.0) = 0.3;

void fragment() {
    vec2 uv = UV;
    uv.x += TIME * scroll_speed;                  // scroll horizontally over time
    COLOR = texture(TEXTURE, uv) * tint;          // TEXTURE = the node's texture
}
```

### 2. 2D dissolve using a noise threshold

```glsl
shader_type canvas_item;

uniform sampler2D noise : repeat_enable;          // a NoiseTexture2D
uniform float amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    float n = texture(noise, UV).r;
    if (n < amount) {
        discard;                                  // cut the pixel away
    }
    COLOR = tex;
}
```

### 3. 3D (spatial): emissive rim light

```glsl
shader_type spatial;

uniform vec4 base_color : source_color = vec4(0.2, 0.5, 1.0, 1.0);
uniform vec3 rim_color : source_color = vec3(0.6, 0.8, 1.0);
uniform float rim_power : hint_range(0.5, 8.0) = 3.0;

void fragment() {
    ALBEDO = base_color.rgb;
    // VIEW and NORMAL are view-space built-ins; rim is strong at grazing angles.
    float rim = pow(1.0 - dot(NORMAL, VIEW), rim_power);
    EMISSION = rim_color * rim;
}
```

### 4. Screen-reading post effect (4.x hint, not SCREEN_TEXTURE)

```glsl
shader_type canvas_item;

// 4.x: declare the screen as a uniform with hint_screen_texture.
uniform sampler2D screen_tex : hint_screen_texture, filter_linear_mipmap;
uniform float blur : hint_range(0.0, 4.0) = 1.0;

void fragment() {
    vec2 px = SCREEN_PIXEL_SIZE * blur;
    vec4 c = texture(screen_tex, SCREEN_UV);
    c += texture(screen_tex, SCREEN_UV + vec2(px.x, 0.0));
    c += texture(screen_tex, SCREEN_UV - vec2(px.x, 0.0));
    COLOR = c / 3.0;
}
```

Set a uniform from GDScript:

```gdscript
$Sprite2D.material.set_shader_parameter("amount", 0.7)
```

## Pitfalls

- **3.x → 4.x renames.** `SCREEN_TEXTURE` is removed — declare
  `uniform sampler2D x : hint_screen_texture;` and sample with `SCREEN_UV`. Color hints
  `hint_color`/`hint_albedo`→`source_color`; `hint_white`/`hint_black`→
  `hint_default_white`/`hint_default_black`; `hint_range` stays. Depth/normal use `hint_depth_texture` / `hint_normal_roughness_texture`.
- **Wrong output variable.** In `canvas_item` write `COLOR`; in `spatial` write `ALBEDO`
  (and `EMISSION`, `ALPHA`, `ROUGHNESS`, `METALLIC`). Writing `COLOR` in a spatial shader
  does nothing.
- **Color uniforms without `source_color`** are treated as raw linear values and look
  wrong (washed/dark) because Godot won't sRGB-convert them.
- **Object drawn in the wrong order, casts no shadow, or skips SSAO (3D)** → the spatial
  shader reads or writes `ALPHA`, which moves the whole material to the transparent
  pipeline even if the value is always `1.0`. Don't touch `ALPHA` in opaque shaders; for
  hard cut-outs also set `ALPHA_SCISSOR_THRESHOLD` (alpha-scissor stays in the opaque pass).
- **Sampling outside [0,1] UV** without `repeat_enable` clamps. Add `: repeat_enable` to
  the sampler uniform for tiling/scroll.
- **Effect jumps once an hour** → `TIME` (seconds since start, affected by `time_scale`, not
  by pausing) wraps every `rendering/limits/time/time_rollover_secs` (3600 by default).
  Pick periods that divide the rollover, or feed your own time through a uniform.
- **`discard` is costly** on some hardware and breaks early-Z; prefer setting `ALPHA`/
  `COLOR.a` when you can.

## References

- For built-in variables per shader type, render modes, `varying`, custom `light()`,
  `vertex()` displacement, and the visual shader graph, read
  `references/shading-language.md`.

## Related skills

- `shader-programming` — engine-agnostic shader concepts (GLSL/HLSL).
- `godot-3d-essentials` — materials, environment, and where spatial shaders live.
- `godot-ui-control` — applying shaders to UI for effects.


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
