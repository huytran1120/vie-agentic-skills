---
name: godot-signals-groups
description: >
  Build event-driven, decoupled Godot 4.7 gameplay with signals and node groups:
  declare and emit custom signals, connect with Callables (incl. bind/one-shot),
  and broadcast to many nodes via groups and call_group. Use when wiring node
  communication in a Godot project, replacing tight references with signals,
  emitting/connecting events, or porting 3.x connect("sig", self, "method") code.
---

# Godot Signals & Groups (4.x)

Decouple nodes with the observer pattern (signals) and act on many nodes at once
(groups), instead of hard-coding references between scenes. Targets **Godot 4.7**.

## When to use

- Use when a node needs to tell others "something happened" (player died, item picked
  up, wave cleared) without holding direct references to them.
- Use when you need to address a whole category of nodes at once ("pause all enemies",
  "save every checkpoint").

**When *not* to use:** raw signal *syntax* basics → `godot-gdscript`; scene structure
and instancing → `godot-nodes-scenes`. For cross-scene global events, emit from an
autoload (see `godot-nodes-scenes`).

## Core workflow

1. **Decide the direction.** A child/sub-scene should *emit* a signal upward; the parent
   *connects* to it. This keeps the child reusable and ignorant of who listens.
2. **Declare typed signals** on the emitter; `emit()` them when the event occurs.
3. **Connect with a Callable** (`sig.connect(_on_sig)`), optionally in the editor's Node
   dock. Use `CONNECT_ONE_SHOT` for fire-once, `bind()` to pass extra context.
4. **Use groups for broadcast**: add nodes to a named group, then iterate
   `get_tree().get_nodes_in_group(...)` or `call_group(...)`.
5. **Disconnect when needed** (e.g. before freeing a long-lived listener) and check
   `is_connected()` to avoid duplicate connections.

## Patterns

### 1. Emit upward, connect from the parent

```gdscript
# coin.gd (reusable pickup — knows nothing about the player or HUD)
extends Area2D
signal collected(value: int)

func _on_body_entered(body: Node) -> void:
    if body.is_in_group("player"):
        collected.emit(10)
        queue_free()
```

```gdscript
# level.gd (the parent wires the coin to game state)
func _ready() -> void:
    for coin in get_tree().get_nodes_in_group("coins"):
        coin.collected.connect(_on_coin_collected)

func _on_coin_collected(value: int) -> void:
    GameState.add_score(value)
```

### 2. Connect flags: one-shot and bind extra arguments

```gdscript
func _ready() -> void:
    # Fire exactly once, then auto-disconnect.
    $Door.opened.connect(_on_door_opened, CONNECT_ONE_SHOT)
    # bind() appends arguments supplied at connect time (after the signal's own args).
    $RedButton.pressed.connect(_on_button.bind("red"))

func _on_button(color: String) -> void:
    print("Pressed the %s button" % color)
```

### 3. Groups: broadcast to many nodes

```gdscript
func pause_all_enemies() -> void:
    # Call a method on every node in the "enemies" group (no-op if missing).
    get_tree().call_group("enemies", "set_paused", true)

func count_enemies() -> int:
    return get_tree().get_nodes_in_group("enemies").size()
```

Add a node to a group from code or via the editor's Node > Groups tab:

```gdscript
func _ready() -> void:
    add_to_group("enemies")        # remove_from_group("enemies") to leave
```

### 4. Await a signal inline

```gdscript
func open_chest() -> void:
    $AnimationPlayer.play("open")
    await $AnimationPlayer.animation_finished   # pause until it emits
    spawn_loot()
```

## Pitfalls

- **3.x connect signature is gone.** `connect("died", self, "_on_died")` →
  `died.connect(_on_died)`. The target is implied by the Callable. The legacy
  `Object.connect("died", Callable(self, "_on_died"))` works but the method-name string
  form does not.
- **Duplicate connections fire handlers multiple times.** Connecting again in `_ready()`
  after re-adding a node stacks callbacks. Guard with
  `if not sig.is_connected(cb): sig.connect(cb)`.
- **Connecting to a freed node errors.** Godot removes a connection when the emitter or
  the Callable's owner is freed, but a lambda belongs to the script that created it — one
  that captures a node freed later keeps firing and errors. Connect listener methods, or
  disconnect stored lambdas yourself.
- **Groups are global to the SceneTree**, not per-scene. Two levels using the same group
  name share membership. Namespace group names if that matters.
- **`call_group` silently ignores nodes lacking the method.** Typos in the method name
  fail quietly — prefer a typed signal when the contract matters.
- **Signal args must match the handlers.** `emit()` does not validate arguments against
  the `signal` declaration; a handler with a different argument count fails with "Method
  expected N argument(s)" at emit time. Declare typed params and emit exactly those.

## References

- For connection flags, deferred connections, custom signal arguments, awaiting with
  timeouts, and signals vs. direct calls trade-offs, read `references/signal-patterns.md`.

## Related skills

- `godot-gdscript` — signal/`await` syntax fundamentals.
- `godot-nodes-scenes` — autoloads for global event buses.
- `game-ai` — state machines that often drive and consume these events.


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
