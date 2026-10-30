---
name: godot-2d-movement
description: >
  Implement 2D kinematic character movement in Godot 4.7 with CharacterBody2D and
  move_and_slide(): platformer run/jump with gravity, top-down 8-direction motion,
  slope handling, and reading collisions. Use when coding a 2D player or enemy
  controller, a platformer or top-down character, or fixing move_and_slide()/
  is_on_floor() behavior in a .tscn with a CharacterBody2D.
---

# Godot 2D Movement (4.x)

Build responsive 2D character controllers with `CharacterBody2D` and the argument-less
`move_and_slide()`. Targets **Godot 4.7**.

## When to use

- Use when scripting a 2D player/enemy that moves and collides: platformer (gravity +
  jump) or top-down (free 8-direction), slope walking, or wall/floor detection.
- Use when `move_and_slide()` "does nothing", the character sinks through floors, or
  `is_on_floor()` is always false.

**When *not* to use:** dynamic rigid bodies, areas, raycasts, collision layers →
`godot-physics`; tile-based levels → `godot-tilemap`; full platformer game template →
the `platformer` genre skill; engine-agnostic feel tuning → `physics-tuning`.

## Core workflow

1. **Use `CharacterBody2D`** with a `CollisionShape2D` child. It is script-driven: it
   does not fall or react to forces on its own.
2. **Set the `velocity` property, then call `move_and_slide()`** (no arguments in 4.x).
   The method reads `velocity`, moves the body, slides along surfaces, and updates
   `velocity` to reflect what actually happened.
3. **Do it in `_physics_process(delta)`** — `move_and_slide()` uses the physics step's
   delta internally, so do not multiply `velocity` by `delta` yourself.
4. **Platformer:** add gravity to `velocity.y` each tick, jump by setting `velocity.y`
   negative when `is_on_floor()`.
5. **Top-down:** build a direction from input and scale by speed; set
   `motion_mode = MOTION_MODE_FLOATING` so there is no "floor/wall" distinction.
6. **Read results** with `is_on_floor()`, `is_on_wall()`, `get_wall_normal()`, and
   `get_slide_collision(i)` after the call.

## Patterns

### 1. Platformer controller (gravity, jump, slopes)

```gdscript
extends CharacterBody2D

@export var speed := 200.0
@export var jump_velocity := -400.0
@export var gravity := 1200.0          # pixels/sec^2 (tune to taste)

func _physics_process(delta: float) -> void:
    # Apply gravity while airborne.
    if not is_on_floor():
        velocity.y += gravity * delta

    # Jump only when grounded (Input action set in Project Settings > Input Map).
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    # Horizontal input: -1, 0, or 1.
    var dir := Input.get_axis("move_left", "move_right")
    if dir != 0.0:
        velocity.x = dir * speed
    else:
        velocity.x = move_toward(velocity.x, 0.0, speed)   # decelerate to a stop

    move_and_slide()   # 4.x: no arguments; uses and updates `velocity`
```

A fixed `gravity` export keeps tuning simple. To follow the project setting
(*Physics > 2D > Default Gravity*) and any `Area2D` gravity overrides instead, use
`velocity += get_gravity() * delta`, as the built-in CharacterBody2D script template does.

### 2. Top-down 8-direction movement

```gdscript
extends CharacterBody2D

@export var speed := 220.0

func _ready() -> void:
    motion_mode = CharacterBody2D.MOTION_MODE_FLOATING  # no floor/ceiling concept

func _physics_process(_delta: float) -> void:
    # get_vector returns a normalized-ish Vector2 from four input actions.
    var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = input * speed
    move_and_slide()
```

### 3. Reading slide collisions after moving

```gdscript
func _physics_process(delta: float) -> void:
    # ... set velocity ...
    move_and_slide()
    for i in get_slide_collision_count():
        var c := get_slide_collision(i)
        var other := c.get_collider()
        if other and other.is_in_group("enemies"):
            take_damage(1)        # touched an enemy while moving
```

### 4. Coyote time (forgiving jump just after leaving a ledge)

```gdscript
@export var coyote_time := 0.1
var _coyote := 0.0

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y += gravity * delta
        _coyote -= delta
    else:
        _coyote = coyote_time

    if Input.is_action_just_pressed("jump") and _coyote > 0.0:
        velocity.y = jump_velocity
        _coyote = 0.0
    # ... horizontal input + move_and_slide() ...
```

## Pitfalls

- **3.x signature is gone.** `move_and_slide(velocity)` (returning the new velocity) was
  removed. In 4.x set the `velocity` property and call `move_and_slide()` with no args.
  `move_and_slide(velocity, Vector2.UP)` will not parse.
- **Multiplying velocity by delta.** `move_and_slide()` already accounts for the physics
  delta. Setting `velocity = dir * speed * delta` makes the body crawl.
- **Movement in `_process`** instead of `_physics_process` causes frame-rate-dependent,
  jittery motion. Always move in `_physics_process`.
- **`is_on_floor()` always false** when `up_direction` is wrong (default `Vector2.UP`),
  there is no `CollisionShape2D`, or you never called `move_and_slide()` this frame.
- **Sinking through floors** usually means the collision shape is missing/zero-sized, the
  floor body is on a layer this body's mask doesn't include, or you moved the body via
  `position +=` instead of velocity + `move_and_slide()`.
- **Slope slipping while idle:** keep `floor_stop_on_slope = true` (default) and raise
  `floor_snap_length` (default 1 px) so the body sticks to downward slopes.

## References

- For one-way platforms, moving platforms, jump buffering, variable jump height, and
  `move_and_collide()` (manual collision response), read `references/controller-recipes.md`.

## Related skills

- `godot-physics` — collision layers/masks, areas, raycasts, rigid bodies.
- `godot-tilemap` — building the levels this character walks on.
- `godot-animation` — driving sprite/skeletal animation from movement state.
- `camera-systems` — follow camera, deadzone, and look-ahead that track this character.
- `platformer` / `input-systems` — full genre template and rebindable input.


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
