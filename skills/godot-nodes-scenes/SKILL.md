---
name: godot-nodes-scenes
description: >
  Structure a Godot 4.7 project with the scene tree and node composition: build
  reusable scenes, instance PackedScenes at runtime, navigate the tree safely,
  and register autoload singletons. Use when designing .tscn scenes, deciding how
  to split nodes, spawning instances with instantiate(), wiring autoloads, or
  fixing "node not found"/freed-node errors in a Godot project.
---

# Godot Nodes & Scenes (4.x)

Compose games from nodes and scenes, instance them at runtime, and access the tree
without crashing on freed or missing nodes. Targets **Godot 4.7**.

## When to use

- Use when structuring `.tscn` scenes, choosing how to break a feature into nodes,
  instancing a `PackedScene` (bullets, enemies, UI), or setting up autoload singletons.
- Use when debugging `get_node()` / `$Path` returning `null`, or "Attempt to call on a
  previously freed instance".

**When _not_ to use:** GDScript language/syntax → `godot-gdscript`; signal-based
decoupling → `godot-signals-groups`; physics bodies/collisions → `godot-physics`.

## Core workflow

1. **Model with composition.** A scene is a tree of nodes saved as `.tscn`. Build small,
   single-purpose scenes (Player, Bullet, Enemy) and compose larger scenes from them.
   Favor adding child nodes over deep inheritance.
2. **Make a scene reusable** by giving its root a script and exposing `@export` config.
   Save it; it becomes a `PackedScene` you can instance many times.
3. **Instance at runtime** with `preload`/`load` → `scene.instantiate()` →
   `add_child(instance)`. Set position/state _after_ adding (or before, both work).
4. **Access nodes safely.** Use `@onready var x = $Path` for fixed children; use unique
   names (`%Name`) for nodes deep in the tree; never assume a node still exists.
5. **Use autoloads for global state/services** (game state, audio, scene switching) —
   registered in Project Settings > Globals (Autoload), accessible by name everywhere.
6. **Free nodes with `queue_free()`** and guard later access with `is_instance_valid()`.
7. **Check references before you finish.** After creating, moving or renaming scenes,
   resources or scripts, run `python scripts/check_godot_project.py <project-dir>` (no
   Godot install needed; `--json` for machine-readable output). Fix every `ERROR` (missing
   or wrong-case `res://` paths, undeclared `ExtResource`/`SubResource` ids, bad `parent=`
   paths, missing main scene or autoload) and re-run until it exits 0. Warnings such as a
   stale `path=` that Godot still finds by uid are safe but worth fixing. Run the script
   path relative to this skill directory, or resolve the installed skill path first. It
   needs Python 3.10+ and nothing else, and it does not replace opening the project in Godot.

## Patterns

### 1. Instance a scene at runtime

```gdscript
extends Node2D

const BULLET := preload("res://bullet.tscn")   # preload: loaded at compile time

func shoot(at: Vector2, dir: Vector2) -> void:
    var bullet := BULLET.instantiate()         # create an instance of the scene
    bullet.global_position = at
    bullet.direction = dir                      # set exported/public state
    add_child(bullet)                           # now it's in the tree and runs
```

### 2. Safe node access: $, get_node_or_null, and unique names

```gdscript
@onready var label: Label = $UI/Label            # $ is sugar for get_node("UI/Label")
@onready var health_bar: ProgressBar = %HealthBar # % = scene-unique name (rename-proof)

func update() -> void:
    var optional := get_node_or_null("Maybe/Missing")  # returns null instead of erroring
    if optional:
        optional.queue_free()
```

### 3. An autoload singleton (global game state)

```gdscript
# game_state.gd — add in Project Settings > Globals > Autoload as "GameState".
extends Node

var score := 0
signal score_changed(value: int)

func add_score(points: int) -> void:
    score += points
    score_changed.emit(score)         # any scene can: GameState.score_changed.connect(...)
```

### 4. Change the running scene

```gdscript
func go_to_level_2() -> void:
    # Swaps the current scene for another. Frees the old scene tree.
    get_tree().change_scene_to_file("res://levels/level_2.tscn")
    # Or, with a preloaded PackedScene:
    # get_tree().change_scene_to_packed(LEVEL_2)
```

## Pitfalls

- **`$Path` / `get_node()` return `null` or error** when the path is wrong or the node
  isn't in the tree yet. Use `@onready`, verify the path matches the scene, or use
  `get_node_or_null()` for optional nodes.
- **Renaming a node breaks `$Path`.** Use **unique names** (`%Name`, set via right-click
  > Access as Unique Name) so deep references survive renames and reparenting.
- **`free()` mid-frame can crash** other code still using the node. Prefer
  `queue_free()` (deletes at end of frame) and check `is_instance_valid(node)`.
- **Setting child state before `add_child()`** is fine, but `_ready()` on the child only
  runs _after_ it enters the tree — don't expect its `@onready` vars before that.
- **Autoload order matters**: autoloads are added before the main scene, in list order.
  An autoload can't depend on the main scene existing yet.
- **`instance()` was renamed** to `instantiate()` in Godot 4. `preload` runs at parse
  time (path must be constant); `load` runs at runtime (path can be a variable).
- **`change_scene_to_file()` is deferred, and the old scene leaves the tree at once.** The
  outgoing scene is removed from the tree immediately (its `get_tree()` now returns `null`,
  and `get_tree().current_scene` is `null`), then at the end of the frame it is freed and the
  new scene is added. Code after the call must not touch `get_tree()` from the old scene. To
  act on the new scene, do it from the new scene's `_ready()`, or from an autoload with
  `await get_tree().scene_changed` (Godot 4.5+). `change_scene_to_node(node)` (4.6+) swaps
  in a node you have already instanced and configured.

## References

- For scene inheritance, `owner`/ownership when saving scenes from code, groups vs
  unique names, and node-path edge cases, read `references/tree-and-instancing.md`.
- `scripts/check_godot_project.py` — read-only reference checker for a Godot 4.x project;
  `--help` lists every check and the exit codes.

## Related skills

- `godot-gdscript` — language, lifecycle, and `@onready`.
- `godot-signals-groups` — decouple instanced scenes from their spawner.
- `godot-resources` — share data between instances without duplicating it.
- `save-systems` — persist scene/game state across runs.


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
