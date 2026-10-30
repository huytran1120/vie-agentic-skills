---
name: godot-3d-essentials
description: >
  Set up a Godot 4.7 3D scene: Node3D transforms, Camera3D, lighting
  (DirectionalLight3D/OmniLight3D), WorldEnvironment for sky/ambient/tonemap/post,
  MeshInstance3D materials, and GridMap for tile-based 3D levels. Use when building
  a 3D scene in a Godot project, placing cameras/lights, configuring environment and
  post-processing, or working with Node3D/.tscn 3D content and GridMap.
---

# Godot 3D Essentials (4.x)

Assemble a working 3D scene: transforms, camera, lights, environment/post, materials, and
`GridMap` blockouts. Targets **Godot 4.7**.

## When to use

- Use when starting or fixing a 3D scene: positioning a `Camera3D`, adding lights, setting
  up a `WorldEnvironment` (sky, ambient, tonemap, glow/SSAO), assigning materials, or
  building levels with `GridMap`.

**When *not* to use:** writing spatial shaders → `godot-shaders`; 3D physics bodies and
raycasts → `godot-physics`; character animation blending → `godot-animation`; full FPS
template → the `fps-shooter` genre skill.

## Core workflow

1. **Everything 3D is a `Node3D`** with a `Transform3D` (position, rotation basis, scale).
   Move with `global_position`, rotate with `rotate_y(angle)` or `look_at(target)`.
2. **Add a `Camera3D`.** Mark it `current` (or call `make_current()`); set `fov`, `near`,
   `far`. Parent it to a rig/pivot for orbit or follow cameras.
3. **Light the scene.** A `DirectionalLight3D` is the sun; `OmniLight3D`/`SpotLight3D` are
   local; `AreaLight3D` (4.7+) is a rectangular panel light that costs more than omni/spot.
   Enable shadows per light. Without lights and ambient, surfaces render black.
4. **Add a `WorldEnvironment`** with an `Environment` resource: background (sky/color),
   ambient light, tonemap, and post (glow, SSAO, fog, adjustments).
5. **Give meshes materials** (`StandardMaterial3D` or a `ShaderMaterial`) on
   `MeshInstance3D`.
6. **Block out levels with `GridMap`**, which places `MeshLibrary` items on a 3D grid
   (the 3D analog of a tilemap).

## Patterns

### 1. A follow camera (third-person, smoothed)

```gdscript
extends Camera3D

@export var target: Node3D
@export var offset := Vector3(0, 4, 8)
@export var smooth := 6.0

func _physics_process(delta: float) -> void:
    if target == null:
        return
    var desired := target.global_position + offset
    global_position = global_position.lerp(desired, smooth * delta)  # smooth follow
    look_at(target.global_position, Vector3.UP)                      # face the target
```

### 2. Sun + environment in code

```gdscript
func _ready() -> void:
    var sun := DirectionalLight3D.new()
    sun.rotation_degrees = Vector3(-45, -30, 0)
    sun.shadow_enabled = true
    add_child(sun)

    var we := WorldEnvironment.new()
    var env := Environment.new()
    env.background_mode = Environment.BG_SKY
    env.sky = Sky.new()
    env.sky.sky_material = ProceduralSkyMaterial.new()
    env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
    env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
    env.glow_enabled = true
    we.environment = env
    add_child(we)
```

### 3. Assign a StandardMaterial3D from code

```gdscript
func tint_mesh(mesh: MeshInstance3D, color: Color) -> void:
    var mat := StandardMaterial3D.new()
    mat.albedo_color = color
    mat.metallic = 0.0
    mat.roughness = 0.6
    mat.emission_enabled = true
    mat.emission = color * 0.3
    mesh.material_override = mat       # overrides the mesh's surface materials
```

### 4. Place tiles into a GridMap

```gdscript
@onready var grid: GridMap = $GridMap   # cell_size + mesh_library set in the editor

func build_floor(width: int, depth: int, item_id: int) -> void:
    for x in width:
        for z in depth:
            # set_cell_item(Vector3i cell, int item, orientation = 0)
            grid.set_cell_item(Vector3i(x, 0, z), item_id)
```

## Pitfalls

- **Scene renders black** → no lights and no ambient. Add a `DirectionalLight3D` and/or a
  `WorldEnvironment` with ambient/sky. New scenes have neither by default.
- **No camera / wrong camera.** If nothing shows, no `Camera3D` is `current`. Set
  `current = true` or `make_current()`; only one camera renders per viewport.
- **Confusing local vs global transforms.** `position`/`rotation` are relative to the
  parent; `global_position`/`global_transform` are world space. Mixing them under a rotated
  parent gives surprising results. `look_at` uses global coordinates.
- **Scaling physics/lights.** Non-uniform `scale` on a `Node3D` distorts child collisions
  and lights; prefer scaling the mesh asset or using uniform scale.
- **`look_at` does nothing and prints an error** → the target equals the node's position, the
  `up` vector is parallel to the look direction (e.g. looking straight down with
  `Vector3.UP`), or the node is not in the tree yet. Keep an offset, pass a different `up`, or
  use `look_at_from_position()` before the node enters the tree.
- **GridMap with no `MeshLibrary`** places nothing. Create a `MeshLibrary` (from scenes)
  and assign it; `set_cell_item(cell, -1)` clears a cell.
- **HDR/glow too strong** → check `tonemap_mode` and glow thresholds; raw emissive values
  bloom hard under filmic tonemapping.

## References

- For Transform3D math, camera projection modes, light/shadow params, the full
  Environment/post-processing options, `MeshLibrary` creation, and `ReflectionProbe`/
  `LightmapGI` lighting, read `references/scene-and-environment.md`.

## Related skills

- `godot-physics` — 3D bodies, areas, and raycasts.
- `godot-shaders` — spatial shaders for custom 3D surfaces.
- `godot-animation` — `AnimationTree` for 3D characters.
- `camera-systems` — third-person orbit / first-person look rigs, framing, and collision.
- `performance-optimization` — keep 3D scenes within frame budget (draw calls, lights, LOD).
- `fps-shooter` — composes 3D movement, input, and AI into a game.


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
