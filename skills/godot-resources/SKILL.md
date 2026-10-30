---
name: godot-resources
description: >
  Design data-driven Godot 4.7 games with custom Resource classes: define typed
  data with class_name + @export, save/load .tres/.res files, instance and duplicate
  resources, and load on demand with ResourceLoader (incl. threaded loading). Use
  when modeling items/stats/configs as data in a Godot project, creating .tres
  resources, or working with custom Resource subclasses and ResourceLoader/ResourceSaver.
---

# Godot Resources (4.x)

Model game data as reusable, Inspector-editable `Resource` objects instead of hard-coded
values, and load/save them as `.tres`/`.res`. Targets **Godot 4.7**.

## When to use

- Use when representing items, stats, enemy configs, dialogue lines, or level metadata as
  data; authoring `.tres` files in the Inspector; or loading/saving custom resources.

**When *not* to use:** nodes/scene structure → `godot-nodes-scenes`; saving the player's
*runtime progress* (engine-agnostic save format/slots) → `save-systems`; the C# variant of
this pattern → `godot-csharp`.

## Core workflow

1. **Subclass `Resource`** with `class_name` and `@export` fields. It now appears in the
   "New Resource" dialog and as an `@export` type, editable in the Inspector.
2. **Create instances as `.tres`** files in the FileSystem dock (text, diff-friendly) or
   `.res` (binary, smaller/faster). Edit their fields in the Inspector — no code needed.
3. **Reference resources from nodes** via `@export var data: ItemResource`, or arrays
   `@export var loot: Array[ItemResource]`.
4. **Load at runtime** with `preload` (constant path) or `load`/`ResourceLoader.load`
   (variable path). Use threaded loading for large assets.
5. **Duplicate before mutating** a shared resource at runtime, or every node using it
   changes too (resources are shared references).
6. **Save generated/edited resources** with `ResourceSaver.save`.

## Patterns

### 1. A custom data resource

```gdscript
# item.gd
extends Resource
class_name ItemResource

@export var id: StringName = &""
@export var display_name: String = "Item"
@export_multiline var description: String = ""
@export var icon: Texture2D
@export var max_stack: int = 99
@export var value: int = 0
```

Create `sword.tres` from this class in the FileSystem dock and fill it in the Inspector.

### 2. Consume resources from a node

```gdscript
extends Node
@export var starting_items: Array[ItemResource] = []   # drag .tres files in the Inspector

func _ready() -> void:
    for item in starting_items:
        print("Have: %s (x%d max)" % [item.display_name, item.max_stack])
```

### 3. Duplicate before mutating shared data

```gdscript
func give_unique_copy(template: ItemResource) -> ItemResource:
    # true = deep: copies nested arrays/dictionaries and *embedded* sub-resources, but
    # sub-resources saved in their own .tres stay shared. Use
    # template.duplicate_deep(Resource.DEEP_DUPLICATE_ALL) to copy those as well.
    var copy: ItemResource = template.duplicate(true)
    copy.value += 5                # mutating the copy won't touch the template .tres
    return copy
```

### 4. Save and load a resource at runtime

```gdscript
func save_config(cfg: Resource) -> void:
    ResourceSaver.save(cfg, "user://config.tres")   # user:// = writable app data dir

func load_config() -> Resource:
    if ResourceLoader.exists("user://config.tres"):
        return ResourceLoader.load("user://config.tres")
    return null
```

## Pitfalls

- **Resources are shared by reference.** A single `.tres` assigned to many nodes is the
  *same* object — mutating it changes all of them (and re-saving the file). Call
  `duplicate(true)` for per-instance state.
- **A deep copy still changes the original's sub-resource** → `duplicate(true)` only copies
  sub-resources embedded in the file; one saved as its own `.tres` (e.g. a shared
  `stats.tres` inside `goblin.tres`) is still the same object. Use
  `duplicate_deep(Resource.DEEP_DUPLICATE_ALL)` when those must be copied too.
- **`class_name` required to instance from the editor.** Without it the class won't appear
  in the "New Resource" dialog or as an `@export` type.
- **`res://` is read-only in exported games.** Write runtime data to `user://`, never
  `res://`. `ResourceSaver.save` to `res://` only works in the editor.
- **Storing nodes in a Resource doesn't serialize them.** Resources hold data, not live
  scene nodes. Reference scenes via `PackedScene`, not node instances.
- **Cyclic resource references** (A holds B holds A) can fail to save/load cleanly — keep
  data graphs acyclic or use IDs/lookups.
- **`preload` vs `load`.** `preload` needs a constant path and loads with the script;
  `load` accepts a variable path at runtime. Use `ResourceLoader.exists()` before `load`
  to avoid errors on missing files.
- **Don't put secrets in `.tres`** — they ship in plain text inside the export.

## References

- For threaded/background loading (`load_threaded_request`), `@tool` resources with custom
  setup, custom `ResourceFormatLoader`/`Saver`, resource-local-to-scene, and resource UIDs,
  read `references/resource-patterns.md`.

## Related skills

- `godot-gdscript` — `@export` annotations used to define resource fields.
- `godot-nodes-scenes` — instancing scenes vs. sharing resource data.
- `save-systems` — persisting runtime progress (separate from static data).
- `unity-scriptableobjects` — the equivalent data-asset pattern in Unity.


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
