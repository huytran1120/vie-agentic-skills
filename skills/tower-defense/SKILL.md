---
name: tower-defense
description: >
  Build a tower defense: enemies pathing along lanes, wave spawning, towers that auto-target and fire,
  an economy, and lives. Use for a tower-defense/wave-defense game, or balancing waves and economy.
---

# Tower Defense

A playbook for tower defense — enemy pathing, wave spawning, tower targeting, and the
economy that ties them together. This is a **compositional** skill: it orchestrates pathing,
AI, and UI into a TD loop. It does not re-teach pathfinding; it defines the systems and the
balance levers (DPS vs. HP vs. income) that decide whether a TD is tense or trivial.

## When to use

- Use when building a game where the player **places towers** that automatically attack
  **waves of enemies** following a path, spends earned currency to expand/upgrade, and loses
  if too many enemies leak through.
- Use when designing wave composition/pacing, tower targeting priorities, or the gold economy.

**When _not_ to use:** the player directly controls a shooter → `fps-shooter`. Free-form base
building with needs → `survival-crafting`. For the pathfinding algorithm itself, use `game-ai`.

## Core loop

**Prepare (place/upgrade towers with current gold) → start the wave → enemies path toward the
goal while towers auto-fire → earn gold from kills → survive the wave → repeat against a
harder one.** The tension is a planning puzzle: is my current DPS enough for what's coming,
and can I afford the answer?

## Must-have systems

1. **Enemy path** — waypoint lanes, or grid + pathfinding for maze TD (refs).
2. **Wave spawner** — timed, scripted sequences of enemy types with per-wave scaling.
3. **Towers** — range, fire rate, damage, projectile/hitscan, splash; placement validity.
4. **Targeting** — per-tower priority (first/last/closest/strongest/weakest) (refs).
5. **Economy** — gold from kills + wave bonuses; tower/upgrade costs; sell refund.
6. **Lives / leak** — enemies reaching the goal cost lives; 0 = game over.
7. **Wave/prep UI** — lives, gold, next-wave preview, start-next-wave control.

## Design knobs

| Knob                      | Effect                  | Notes                                    |
| ------------------------- | ----------------------- | ---------------------------------------- |
| Enemy HP growth/wave      | upgrade pressure        | Geometric ~1.1–1.2× (refs).              |
| Income vs. HP curves      | difficulty              | Player should _almost_ afford each wave. |
| Tower DPS / range / cost  | tower identity          | Cheap+wide vs. expensive+tall.           |
| Targeting priority        | optimal placement       | Changes play more than raw stats.        |
| Enemy variety             | counters one-build wins | Fast / armored / flying / swarm / boss.  |
| Leak penalty              | stakes                  | Cost lives _and_ lost bounty.            |
| Upgrade vs. build economy | strategy depth          | Diminishing upgrade returns.             |
| Wave pacing               | tension curve           | Spike → breather → spike, not monotonic. |

## Patterns

### 1. Wave spawner (timed, data-driven)

```python
# Pseudocode. A wave is data: a list of (enemy_type, count, spacing). Spawn over time.
wave = [ ("grunt", 10, 0.5), ("runner", 5, 0.3), ("tank", 2, 1.0) ]

def run_wave(wave):
    for enemy_type, count, spacing in wave:
        for _ in range(count):
            spawn_enemy(enemy_type, at=path[0])   # enter at the path start
            wait(spacing)                          # seconds between spawns (use a timer/coroutine)
    # wave clears when all spawned enemies are dead or have leaked
```

### 2. Tower targeting (filter to range, then pick by priority)

```python
# Pseudocode. "First" (furthest along path) is the standard default for stopping leaks.
def acquire_target(tower, enemies, mode="first"):
    in_range = [e for e in enemies if distance(tower.pos, e.pos) <= tower.range]
    if not in_range: return None
    if mode == "first":    return max(in_range, key=lambda e: e.progress)   # furthest along path (stop leaks)
    if mode == "last":     return min(in_range, key=lambda e: e.progress)   # least progress (guard the entrance)
    if mode == "closest":  return min(in_range, key=lambda e: distance(tower.pos, e.pos))
    if mode == "strongest":return max(in_range, key=lambda e: e.hp)         # burn down tanks first
    if mode == "weakest":  return min(in_range, key=lambda e: e.hp)         # secure kills / last-hit bounty
    return in_range[0]
```

### 3. "Can this lane hold?" sanity check (DPS vs. HP)

```python
# Pseudocode. One tower's damage to one enemy crossing its range.
tower_dps     = tower.damage * tower.fire_rate
time_in_range = tower.range_coverage_length / enemy.speed
damage_dealt  = tower_dps * time_in_range
# Lane holds if summed damage_dealt from covering towers >= enemy.hp (per enemy). See refs.
```

## Pitfalls / failure modes

- **Enemy HP scales slower than player income/DPS** → game trivializes after a few waves.
  Tune the HP curve against the income curve (refs).
- **One dominant tower/strategy** → no decisions. Add enemy types that hard-counter builds
  (armored vs. rapid-fire, flying vs. ground-only) and diminishing upgrade returns.
- **Maze TD that can fully block the goal** → enemies get stuck/softlock. Forbid placements
  that sever the path for the spawn or for any enemy already walking; recompute paths when
  towers change (refs §1).
- **Fast enemies slow down at corners or skip waypoints** → per-step movement stops at each
  waypoint or overshoots it. Carry the leftover distance to the next waypoint (refs §1).
- **No next-wave telegraph** → specials feel random and unfair. Preview upcoming composition.
- **Per-frame movement unscaled by `dt`** → speed varies with frame rate. Scale steering by `dt`.
- **Leaks only cost lives, not gold** → leaking is sometimes optimal. Make leaks lose bounty too.
- **Monotonic difficulty ramp** → exhausting. Pace spikes and breathers.

## Composition (build it from these skills)

- **Pathing:** `game-ai` for A\*/flow-field/steering; for fixed lanes, simple waypoint following.
- **Enemy movement:** `godot-2d-movement` (or engine equivalent) to move along the path; `unity-navmesh` for nav-based pathing.
- **Map:** `godot-tilemap` / `unity-tilemap-2d` for the grid/lanes; `level-design` for map layouts.
- **Data:** `godot-resources` / `unity-scriptableobjects` to define towers, enemies, and waves as assets.
- **UI:** `game-ui-ux` for HUD layout, scaling, and the build menu; `godot-ui-control` for the concrete widgets (lives, gold, wave preview).
- **Polish:** `audio-design` for fire/hit/leak sound cues.

## References

- For path representations (waypoints / A\* / flow fields), targeting modes, DPS and economy
  math, enemy scaling, and wave pacing, read `references/balancing.md`.


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
