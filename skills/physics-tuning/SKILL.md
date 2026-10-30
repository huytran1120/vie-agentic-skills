---
name: physics-tuning
description: >
  Tune game physics for stable, good-feeling motion — fixed vs variable
  timestep, render interpolation, mass/gravity/drag, continuous collision
  detection (CCD) to stop tunneling, fixing jitter, and collision layers/masks.
  Engine-neutral. Use when the user mentions physics feel, jitter, tunneling,
  fixed timestep, FixedUpdate, CCD, bouncing/unstable physics, or collision layers.
---

# Physics tuning

Most "bad physics" is not a bug in the engine — it's a mismatch between the
**fixed-timestep simulation** and the **variable-rate render loop**, or untuned
mass/drag/CCD/layer settings. This skill covers the engine-neutral knobs that
make physics stable and responsive; pair it with `godot-physics` or
`unity-physics` for the concrete APIs.

## When to use

- Use when motion jitters, objects pass through walls (tunneling), stacks
  explode, or movement feels floaty/sticky/laggy.
- Use to decide what goes in the fixed (physics) step vs the render frame, and
  how to interpolate between them.
- Use to tune gravity, mass, drag, restitution, solver iterations, sleeping, and
  collision layers/masks.

**When *not* to use:** for an engine's exact physics nodes/components and
collision callbacks, use `godot-physics` or `unity-physics`. For *movement
decisions* (when to jump, AI steering) use `input-systems` and `game-ai`. For
platformer jump-feel specifics like coyote time/jump buffering, that's input/
controller territory — see `input-systems` and the `platformer` genre.

## Core workflow

1. **Run physics on a fixed timestep.** Simulate at a constant rate (e.g. 50–60
   Hz). A fixed `dt` makes the simulation deterministic-ish and stable; a
   variable `dt` makes integration and collisions inconsistent.
2. **Put physics work in the physics callback**, not the render frame. Apply
   forces/velocities and read collisions in the fixed step (`FixedUpdate` /
   `_physics_process`), using that step's `dt`.
3. **Interpolate rendering between physics ticks.** The render frame rate ≠ the
   physics rate, so smoothly interpolate transforms toward the latest physics
   state, or enable the engine's Rigidbody interpolation, to remove visible
   stutter.
4. **Tune the body, not the scene.** Set mass for relative weight, drag for
   damping, gravity scale per object, and restitution/friction via materials.
5. **Stop tunneling with CCD** on small/fast bodies; cap maximum velocity.
6. **Stabilize stacks/joints** with more solver iterations, sane mass ratios, and
   sleeping for resting bodies.
7. **Verify by feel and stress test.** Play at low and high frame rates; throw
   fast objects at thin walls; stack and shove bodies. Report what you observed.

## Patterns

### 1. Fixed timestep for simulation, render interpolation for smoothness

```gdscript
# Physics callback: runs at the FIXED rate. Use its dt for all integration.
func _physics_process(dt):                  # Unity: void FixedUpdate()
    velocity += gravity * dt                # integrate with the FIXED dt
    move_and_slide()                        # engine resolves collisions this step
    _prev_pos = _curr_pos; _curr_pos = global_position   # record for interpolation

# Render frame: runs as fast as the display. Interpolate between physics states.
func _process(_frame_dt):                   # Unity: void Update()
    var alpha = Engine.get_physics_interpolation_fraction()  # 0..1 within the tick
    visual.global_position = _prev_pos.lerp(_curr_pos, alpha)
# RIGHT: integrate in the fixed step, render via interpolation.
# WRONG: applying forces in _process/Update with frame dt — speed and collisions
# then depend on frame rate and jitter under load.
```

Most engines offer this for you: Godot's project setting
`physics/common/physics_interpolation` (off by default; it interpolates every
node, 2D and 3D) and Unity's `Rigidbody.interpolation = Interpolate`. Prefer the
built-in before hand-rolling, and never do both on the same node.

### 2. Stop tunneling: CCD + a speed cap

```gdscript
# Fast, small bodies skip past thin colliders between ticks. Two fixes:
body.continuous_cd = true            # RigidBody3D bool (RigidBody2D: CCD_MODE_* enum)
# Unity: rb.collisionDetectionMode = CollisionDetectionMode.ContinuousSpeculative (cheap, covers
# dynamic bodies too) or ContinuousDynamic (fast vs fast); plain Continuous sweeps vs static only.
# Cap velocity so a single step can't move more than ~one collider thickness.
const MAX_SPEED := 40.0
if velocity.length() > MAX_SPEED:
    velocity = velocity.normalized() * MAX_SPEED
# Rule of thumb: max_distance_per_step (= speed / physics_hz) should be < the
# thinnest wall. Raise physics_hz or enable CCD when that fails.
```

### 3. Body tuning: mass, drag, gravity scale, material

```gdscript
# Mass is RELATIVE weight in collisions; it does NOT change fall speed (gravity
# accelerates all masses equally). Use drag and gravity_scale to shape feel.
body.mass = 2.0                      # heavier pushes lighter in collisions
body.linear_damp = 0.5               # air drag: higher = stops sooner (Unity 6: linearDamping, was drag)
body.gravity_scale = 1.5             # per-object gravity multiplier (Unity: Rigidbody2D.gravityScale)
# Bounce/slide come from the physics material, not code:
material.bounce = 0.2                # restitution 0..1 (Unity: PhysicsMaterial.bounciness)
material.friction = 0.8              # surface grip
body.physics_material_override = material
```

### 4. Collision layers and masks (who collides with whom)

```gdscript
# A body is ON its layer(s) and SCANS the layers in its mask. Both directions of a
# pair must be configured for them to interact.
player.collision_layer = LAYER_PLAYER
player.collision_mask  = LAYER_WORLD | LAYER_ENEMY     # player detects world+enemies
pickup.collision_layer = LAYER_PICKUP
pickup.collision_mask  = LAYER_PLAYER                  # pickup only reacts to player
# Unity equivalent: assign GameObject layers and edit the Physics collision matrix
# (or Physics.IgnoreLayerCollision). Keep a named layer constant table, not magic numbers.
```

## Pitfalls

- **Applying forces/movement in the render frame** (`Update`/`_process`) makes
  behavior frame-rate dependent — faster PCs run faster, and collisions get
  flaky. Do simulation in the fixed step.
- **Visible jitter** even with a fixed step usually means no render
  interpolation: the physics rate and display rate beat against each other.
  Enable interpolation.
- **Tunneling** through thin walls: discrete collision misses fast movers. Enable
  CCD, cap speed, thicken walls, or raise the physics rate.
- **Expecting heavier objects to fall faster.** Gravity is acceleration; mass
  affects collision response, not fall speed. Use `gravity_scale`/drag for feel.
- **Exploding stacks / jittery joints**: mass ratios too extreme, or too few
  solver iterations. Keep mass ratios modest and raise iteration counts.
- **Bodies that never rest** burn CPU and twitch. Enable sleeping and a sensible
  sleep threshold for resting objects.
- **One-directional layer setup**: A's mask includes B but B's mask excludes A.
  Detection/collision can need both sides; verify the full matrix.
- **Huge `dt` spikes** (load hitches, breakpoints) blow up integration. Clamp the
  max physics step / substep count so a stall doesn't launch everything (Godot
  `physics/common/max_physics_steps_per_frame`, Unity *Maximum Allowed Timestep*).
- **Teleports smear across the screen** with interpolation on: the renderer
  blends from the old position. Godot: call `reset_physics_interpolation()`
  *after* moving the node. Unity: move interpolated bodies through the
  Rigidbody; a direct `transform` write is ignored unless followed by
  `Physics.SyncTransforms()`.
- **Feel changes after raising the physics rate**: Godot (GodotPhysics and Jolt
  alike) damps by multiplying velocity by `1 - damp / ticks_per_second` each
  tick, an approximation that drifts as `damp` approaches the tick rate (at
  `damp >= ticks_per_second` the body stops in one tick). Small damping values
  barely change; re-tune large ones after changing `physics_ticks_per_second`.

## References

- `references/timestep-and-ccd.md` — the fixed-timestep accumulator loop,
  interpolation math, substepping, CCD modes, solver/iteration tuning, sleeping,
  and a stability checklist.

## Related skills

- `godot-physics`, `unity-physics` — concrete bodies, colliders, and callbacks.
- `input-systems` — responsive controls, jump buffering, coyote time.
- `game-ai` — agent movement that must agree with the physics step.
- `platformer`, `fps-shooter` — genres whose feel depends on this tuning.


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
