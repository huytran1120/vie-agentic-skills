---
name: survival-crafting
description: >
  Build a survival-crafting game: resource gathering, inventory, crafting and a tech tree,
  needs (hunger/thirst/temperature), and base building. Use for a survival or crafting/base-building game.
---

# Survival Crafting

A playbook for survival-crafting games — the gather → craft → build loop, survival needs, the
crafting/tech progression, and base building. This is a **compositional** skill: it orchestrates
inventory data, world content, persistence, and threats. It does not re-teach those primitives;
it defines the loop and the pressure systems (needs, scarcity, escalation) that make survival
tense rather than tedious.

## When to use

- Use when the player **gathers resources, crafts items/structures, manages survival needs, and
  builds a base** against escalating threats: survival sandbox, crafting/base-building game.
- Use when designing needs (hunger/thirst/temperature), a crafting tech tree, gathering loops,
  or base placement/building.

**When *not* to use:** crafting as a minor RPG feature → `rpg`. Permadeath grid dungeon →
`roguelike`. For inventory/items as data assets, use `godot-resources` /
`unity-scriptableobjects`; for world generation, `procedural-gen`.

## Core loop

**Gather raw resources → craft tools/items → build and upgrade a base → manage survival needs
→ explore farther for better resources → survive escalating threats → repeat at a higher tier.**
Each loop should unlock the *next* loop (better tools → reach new biomes → new resources →
better crafts). When that ladder breaks, the game becomes a grind.

## Must-have systems

1. **Resource nodes + gathering** — harvestable world objects; tool requirements/tiers; respawn.
2. **Inventory** — stacks, capacity (slots or weight), drop/transfer, hotbar.
3. **Crafting** — recipes (inputs → output), a crafting station/tech gate, a tech tree.
4. **Survival needs** — hunger, thirst, temperature, stamina, health, with decay + consequences.
5. **Base building** — placeable structures, a build grid/snapping, storage, crafting stations.
6. **World + day/night** — biomes/resources (often procedural); a time cycle driving threats.
7. **Threats** — hostile creatures/weather/events that escalate; combat or avoidance.
8. **Save/load** — world state, inventory, base, needs, progression; large-world persistence.

## Design knobs

| Knob | Effect | Notes |
|------|--------|-------|
| Needs decay rates | pressure cadence | Slow enough to explore, fast enough to matter. |
| Need-failure consequence | stakes | Damage over time, not instant death. |
| Resource scarcity / respawn | exploration push | Scarce near base → travel for more. |
| Tool tiers / gating | progression ladder | Better tool → new node types. |
| Recipe complexity / tech depth | long-term goals | Multi-step chains, not flat lists. |
| Inventory limit (slots/weight) | logistics tension | Forces base trips and storage. |
| Threat escalation curve | difficulty over time | Night/seasonal/event ramps. |
| Day length | rhythm | Day = gather, night = defend. |

## Patterns

### 1. Needs decay with graded consequences

```python
# Pseudocode in the per-frame/per-tick update. dt = seconds. Needs fall; failure bleeds HP.
def update_needs(p, dt):
    p.hunger = max(0, p.hunger - HUNGER_RATE * dt)
    p.thirst = max(0, p.thirst - THIRST_RATE * dt)
    p.temp   = approach(p.temp, ambient_temperature(p), TEMP_RATE * dt)

    # Consequences are graded, not binary: warnings, then attrition — never instant death.
    if p.hunger == 0 or p.thirst == 0:
        p.hp -= STARVE_DAMAGE * dt          # damage over time creates urgency with recovery room
    if p.temp < COLD_THRESHOLD or p.temp > HEAT_THRESHOLD:
        p.hp -= EXPOSURE_DAMAGE * dt
    if p.hunger > 0 and p.thirst > 0 and not exposed(p):
        p.hp = min(p.max_hp, p.hp + REGEN_RATE * dt)   # safe + fed => heal
```

### 2. Crafting: validate, then atomically consume inputs

```python
# Pseudocode. Recipes are data: inputs -> output, with an optional station/tech requirement.
recipe = {"id": "stone_axe",
          "inputs": {"wood": 3, "stone": 2}, "output": ("stone_axe", 1),
          "station": "workbench", "requires_tech": "basic_tools"}

def can_craft(recipe, inv, tech, station):
    if recipe.get("requires_tech") and recipe["requires_tech"] not in tech: return False
    if recipe.get("station") and recipe["station"] != station: return False
    return all(inv.count(item) >= n for item, n in recipe["inputs"].items())

def craft(recipe, inv, tech, station):
    if not can_craft(recipe, inv, tech, station): return False
    if not inv.can_add_after_removing(recipe["inputs"], *recipe["output"]):
        return notify("No room for the result")    # check space BEFORE consuming anything
    for item, n in recipe["inputs"].items(): inv.remove(item, n)   # consume all, then add
    inv.add(*recipe["output"])                                     # atomic: no partial craft
    return True
```

The space check must count the slots the inputs free up (crafting 3 wood into 1 plank can
succeed in a full bag). If space is short, refuse, or drop the result on the ground; never
consume the inputs and then fail the add.

### 3. Gathering gated by tool tier

```python
# Pseudocode. A node yields only if the held tool meets its required tier.
def harvest(node, tool):
    if tool.tier < node.required_tier:
        return notify("Need a better tool")        # e.g. stone node needs a pickaxe, not fists
    node.hp -= tool.power
    if node.hp <= 0:
        spawn_drops(node.drop_table)               # weighted drops (see roguelike loot pattern)
        node.start_respawn(node.respawn_time)      # node returns later; world isn't depleted forever
```

## Pitfalls / failure modes

- **Needs that kill instantly** → frustration and save-scumming. Make failure damage over time,
  with clear warnings and a recovery path (Pattern 1).
- **Grind without a ladder** → gathering that never unlocks new gathering. Each tier must open
  the next (better tool → new node → new resource → better craft).
- **Non-atomic crafting** → inputs consumed but output not granted on an edge case, most often
  a full inventory. Validate inputs and space first, then consume-and-add as one step
  (Pattern 2).
- **Inventory with no limits** → no logistics tension and no reason for a base/storage. Cap by
  slots or weight.
- **Permanently depleting the world** → players strip the map and quit. Respawn nodes or
  regenerate resources over time.
- **Per-frame decay unscaled by `dt`** → needs drain at different speeds on different hardware.
  Scale by `dt`.
- **No save / fragile save of a large world** → a crash wipes hours. Persist world+base+needs
  incrementally; version it (see `save-systems`).
- **Flat threat curve** → no late-game pressure. Escalate via night/season/event tiers.

## Composition (build it from these skills)

- **Items/recipes as data:** `godot-resources` / `unity-scriptableobjects` — items, recipes, tech tree, drop tables.
- **World:** `procedural-gen` for biomes/resource placement; `level-design` for authored areas.
- **Persistence:** `save-systems` for large-world state, base, inventory, needs, and versioning.
- **Threats:** `game-ai` for creatures; the engine physics skill for melee/collision.
- **Building/placement:** `godot-tilemap` / `unity-tilemap-2d` (2D) or `godot-3d-essentials` (3D) plus UI snapping.
- **UI:** `game-ui-ux` for inventory/crafting/HUD layout and scaling; `godot-ui-control` for the concrete inventory, crafting menu, needs HUD, and build mode.

## References

- For the full needs model and thresholds, the crafting tech-tree graph, gather/respawn tuning,
  base-building grids, and threat escalation, read `references/needs-and-crafting.md`.


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
