---
name: godot-ui-control
description: >
  Build Godot 4.7 user interfaces with Control nodes: anchors and offsets for
  responsive layout, Container nodes (VBox/HBox/Grid/Margin) for automatic
  arrangement, Theme resources for consistent styling, and keyboard/gamepad focus
  navigation. Use when laying out a HUD, menu, or UI in a Godot project, working
  with Control/Container nodes, anchors, themes, or focus in a .tscn.
---

# Godot UI / Control nodes (4.x)

Lay out responsive UI with `Control` anchors and `Container` nodes, style it with a
`Theme`, and make it navigable by keyboard and gamepad. Targets **Godot 4.7**.

## When to use

- Use when building HUDs, menus, inventories, dialog boxes, or settings screens with
  `Control`-derived nodes; arranging UI that adapts to window size; theming; or wiring
  focus navigation for controller/keyboard.

**When *not* to use:** in-world 2D nodes (`Node2D`/sprites) → `godot-nodes-scenes`;
animating UI transitions → `godot-animation` (Tween); genre UIs like card hands →
`card-game`/`visual-novel`. For full input rebinding → `input-systems`.

## Core workflow

1. **Use `Control` nodes for UI**, not `Node2D`. Controls have a rect (position + size),
   anchors, and participate in focus/theming.
2. **Anchor for responsiveness.** Anchors are fractions (0–1) of the parent rect that the
   Control's edges stick to. Use the editor's **Layout** presets (Top-Left, Full Rect,
   Center, etc.) instead of hand-placing pixels.
3. **Let Containers position children.** Put children in a `VBoxContainer`,
   `HBoxContainer`, `GridContainer`, `MarginContainer`, etc. — the container sets their
   position/size; you control flow with `size_flags`. Don't set child anchors inside a
   container (it overrides them).
4. **Style with a `Theme`.** Assign a `Theme` resource on a top Control; children inherit
   it. Override per-node with theme overrides only when necessary.
5. **Wire focus** so gamepad/keyboard can move between buttons; set a default focused
   control and define neighbors or rely on auto-neighbor.
6. **Connect signals** (`pressed`, `toggled`, `text_submitted`, `value_changed`).

## Patterns

### 1. Responsive layout with anchors (code form)

```gdscript
extends Control

func _ready() -> void:
    # Stretch this panel to fill its parent (the editor's "Full Rect" preset).
    # Setting only anchors (or `anchors_preset`) keeps the current offsets, so the
    # control keeps its old rect; this call moves anchors AND resets offsets.
    set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    # Manual equivalent: anchor_left = 0; anchor_top = 0; anchor_right = 1;
    # anchor_bottom = 1, then set all four offset_* to 0.
```

### 2. A menu built from containers + button signals

```gdscript
extends VBoxContainer    # children stack vertically, auto-sized

func _ready() -> void:
    for child in get_children():
        if child is Button:
            child.pressed.connect(_on_button_pressed.bind(child.name))
    # Give the first button focus so a gamepad can navigate immediately.
    if get_child_count() > 0:
        (get_child(0) as Control).grab_focus()

func _on_button_pressed(which: StringName) -> void:
    match which:
        "PlayButton":  get_tree().change_scene_to_file("res://game.tscn")
        "QuitButton":  get_tree().quit()
```

### 3. Size flags: make one child expand to fill leftover space

```gdscript
# In a HBoxContainer: a label on the left, a spacer that eats remaining width.
func _ready() -> void:
    $Label.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
    $Spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL   # grows to fill
```

### 4. Theme override for one node (without a full Theme resource)

```gdscript
func _ready() -> void:
    # Per-node overrides: use add_theme_* (type-specific setters).
    $Title.add_theme_font_size_override("font_size", 32)
    $Title.add_theme_color_override("font_color", Color.GOLD)
    $Panel.add_theme_stylebox_override("panel", preload("res://ui/panel.stylebox.tres"))
```

## Pitfalls

- **Mixing manual position with Containers.** A child of a `Container` cannot set its own
  position/anchors — the container owns layout. To free-place, take the node out of the
  container or use a plain `Control`/`PanelContainer` wrapper. To nudge, rotate or scale a
  container child (e.g. a hover pop) in 4.7+, set `offset_transform_enabled = true` and use
  `offset_transform_position`/`_rotation`/`_scale`; the container leaves those alone.
- **Anchors vs offsets.** Anchors are fractions of the parent; offsets are pixel deltas
  from the anchored point. Set anchors via presets, then nudge with offsets. Setting only
  position while anchors are at 0 makes UI not scale with the window.
- **`Node2D` for UI.** Buttons/labels parented under a `Node2D` won't theme or take focus
  correctly. Keep UI under a `CanvasLayer`/`Control` subtree.
- **Focus lost on gamepad.** If nothing is focused, directional input does nothing. Call
  `grab_focus()` on an initial control and ensure `focus_mode` is `FOCUS_ALL` (`FOCUS_CLICK`
  is mouse-only, `FOCUS_NONE` never focuses).
- **Theme vs theme override.** A `Theme` resource styles a whole subtree; `add_theme_*`
  overrides one node. Overusing per-node overrides defeats centralized theming.
- **`rect_*` properties are renamed.** Godot 3's `rect_size`/`rect_position`/`rect_min_size`
  are now `size`/`position`/`custom_minimum_size` in 4.x.
- **`mouse_filter`** on a full-rect Control can swallow clicks meant for nodes beneath it;
  set `MOUSE_FILTER_IGNORE` on purely decorative panels.

## References

- For the anchor/offset math, every Container type, building/extending Theme and StyleBox
  resources, focus neighbor wiring, and `CanvasLayer` for HUDs, read
  `references/layout-and-theming.md`.

## Related skills

- `game-ui-ux` — cross-engine UI/UX: responsive scaling, safe areas, focus navigation, screen flow.
- `godot-animation` — Tween-based UI transitions and juicing.
- `godot-signals-groups` — connecting UI events to game logic.
- `input-systems` — rebindable input and multi-device focus.
- `card-game` / `visual-novel` — UI-heavy genre templates.


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
