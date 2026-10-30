---
name: godot-animation
description: >
  Animate in Godot 4.7 three ways: AnimationPlayer for keyframed clips (incl. Call
  Method tracks), AnimationTree with state machines and blend spaces for
  character animation, and Tween for short procedural/UI tweens via create_tween().
  Use when working with AnimationPlayer/AnimationTree nodes in a .tscn, blending
  character states, sprite-sheet animation, or code-driven Tweens.
---

# Godot Animation (4.x)

Choose and drive the right animation tool: `AnimationPlayer` (clips), `AnimationTree`
(blending/state machines), or `Tween` (short procedural moves). Targets **Godot 4.7**.

## When to use

- Use when playing keyframed animations, blending walk/run/idle states, animating a
  sprite sheet, or tweening UI/objects in code.

**When *not* to use:** the movement *logic* that decides which state to play →
`godot-2d-movement`; UI layout (vs. UI tweening) → `godot-ui-control`; shader-driven
effects → `godot-shaders`.

## Core workflow

1. **Pick the tool:**
   - `AnimationPlayer` — author keyframed clips (transforms, properties, method calls,
     audio, even other animations). The source of truth for clip data.
   - `AnimationTree` — blend and transition between those clips at runtime with a state
     machine and/or blend spaces. Needs an `AnimationPlayer` to pull clips from.
   - `Tween` — fire-and-forget procedural interpolation in code (`create_tween()`); ideal
     for UI pops, fades, and one-off moves.
2. **For 2D sprite sheets:** use `AnimatedSprite2D` + `SpriteFrames`, or keyframe the
   `frame` property in an `AnimationPlayer`.
3. **For characters:** build clips in `AnimationPlayer`, then add an `AnimationTree`
   (`active = true`), set its `anim_player`, and design an `AnimationNodeStateMachine` or
   `AnimationNodeBlendSpace2D` as the tree root.
4. **Drive transitions from code** via the playback object (`travel`) or by setting blend
   parameters.
5. **React to clip events** with the `animation_finished` signal and Call Method tracks.

## Patterns

### 1. AnimationPlayer: play a clip and await it

```gdscript
@onready var anim: AnimationPlayer = $AnimationPlayer

func attack() -> void:
    anim.play("attack")
    await anim.animation_finished     # resume after the clip ends
    anim.play("idle")
```

### 2. AnimationTree state machine: travel between states

```gdscript
@onready var tree: AnimationTree = $AnimationTree

func _ready() -> void:
    tree.active = true                # the tree drives animation; AnimationPlayer is the source

func set_state(state: StringName) -> void:
    # The playback object controls an AnimationNodeStateMachine root.
    var sm: AnimationNodeStateMachinePlayback = tree.get("parameters/playback")
    sm.travel(state)                  # transitions using the graph's connections

func _physics_process(_d: float) -> void:
    set_state(&"run" if velocity.length() > 5.0 else &"idle")
```

### 3. Blend space: blend run direction by a 2D parameter

```gdscript
# Root is an AnimationNodeBlendSpace2D named "Move" with idle/run points placed in it.
func update_locomotion(input_dir: Vector2) -> void:
    # Parameter path = "parameters/<node name>/blend_position".
    tree.set("parameters/Move/blend_position", input_dir)
```

### 4. Tween: fade and scale a UI element (code-driven)

```gdscript
func pop_in(node: Control) -> void:
    node.scale = Vector2.ZERO
    node.modulate.a = 0.0
    var tw := create_tween()                          # bound to this node's tree
    tw.set_parallel(true)                             # run the two tweens together
    tw.tween_property(node, "scale", Vector2.ONE, 0.2) \
      .set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
    tw.tween_property(node, "modulate:a", 1.0, 0.2)   # sub-property via ":"
```

## Pitfalls

- **`AnimationTree.active` left false** → nothing animates and `travel()` appears to do
  nothing. Set `active = true` and assign the `anim_player` path.
- **Wrong parameter path.** Blend/condition paths are `"parameters/<NodeName>/..."` and
  must match the node names in the tree exactly (e.g. `"parameters/playback"`,
  `"parameters/Move/blend_position"`). A typo silently no-ops.
- **AnimationPlayer and AnimationTree fighting.** When an `AnimationTree` is active, don't
  also call `AnimationPlayer.play()` for the same tracks — let the tree own playback.
- **3.x Tween node is gone.** There is no `Tween` node to add in 4.x; create tweens in
  code with `create_tween()` (which returns a `Tween`). They auto-start and free themselves.
- **Tween stalls when its node leaves the tree.** `node.create_tween()` pauses while that
  node is outside the tree and dies when it is freed. Use `get_tree().create_tween()` for a
  tween that must keep running while the node is out of the tree.
- **Scale/rotation tween on a child of a `Container` snaps back** → the container resets
  child transforms whenever it re-sorts. In 4.7+ set `offset_transform_enabled = true` and
  tween `offset_transform_scale` / `offset_transform_rotation` / `offset_transform_position`
  instead (visual only by default).
- **Reusing a finished tween.** A tween is one-shot; call `create_tween()` again for a new
  animation. Use `set_loops()` for repetition.
- **`yield`/`yield(anim, "...")` is gone.** Use `await anim.animation_finished`.
- **Sub-property tweens** use a colon: `"modulate:a"`, `"position:x"`. Tweening the whole
  property instead overwrites siblings.

## References

- For state machine transitions/conditions, root motion, one-shot/blend nodes, method &
  call tracks, `SpriteFrames`/`AnimatedSprite2D`, and Tween easing/chaining/callbacks,
  read `references/animation-tree-and-tween.md`.

## Related skills

- `godot-2d-movement` — supplies the velocity/state that selects animations.
- `godot-ui-control` — UI that Tweens animate.
- `godot-3d-essentials` — 3D character scenes driven by AnimationTree.
- `game-ai` — state machines that mirror animation states.


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
