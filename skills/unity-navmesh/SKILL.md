---
name: unity-navmesh
description: >
  Add AI navigation in Unity 6.3 LTS: bake a NavMesh with the AI Navigation package (NavMeshSurface),
  move agents with NavMeshAgent.SetDestination, and handle dynamic obstacles. Use when setting
  up pathfinding, making an enemy chase the player, baking navigation, or when the user
  mentions NavMesh, NavMeshAgent, NavMeshSurface, NavMeshObstacle, or Unity pathfinding.
---

# Unity NavMesh (AI Navigation)

Give NPCs pathfinding in Unity 6.3 LTS: bake walkable surfaces and move agents around obstacles.
Targets **Unity 6.3 LTS (6000.3)** with the **AI Navigation package 2.0** (2.0.16 at last check).

> **Version trap (Unity 2022+/6):** the old built-in **Navigation window** (Object/Bake tabs,
> "Navigation Static" flag) is gone. The package's **Window → AI → Navigation** only holds the
> Agents and Areas tabs. Baking is now **component-based** via the **AI Navigation package**
> (`com.unity.ai.navigation`): add a **NavMeshSurface** to your level geometry and click
> **Bake**. The *runtime* `NavMeshAgent`/`NavMesh` API stays in built-in `UnityEngine.AI`.

## When to use

- Use when an agent needs to walk/chase/patrol to a target, when baking a navigable surface,
  adding dynamic blockers (`NavMeshObstacle`), or checking whether a destination is reachable.
- Use when the project has the AI Navigation package, a `NavMeshSurface` component, or scripts
  using `UnityEngine.AI.NavMeshAgent`.

**When *not* to use:** the *decision* logic of when/where to move (FSMs, behaviour trees,
steering) → `game-ai` (this skill is the Unity movement/pathing mechanism). Force-driven or
kinematic movement that isn't pathfinding → `unity-physics`.

## Core workflow

1. **Install the AI Navigation package** (Package Manager → `com.unity.ai.navigation`).
2. **Bake a surface:** select the static level geometry, **Add Component → Navigation → NavMesh
   Surface**, set the agent type/area settings, and click **Bake**. Re-bake whenever geometry,
   `NavMeshModifier`s, or agent settings change. Agent types (radius, height, step, slope)
   are defined in **Window → AI → Navigation → Agents**.
3. **Add a `NavMeshAgent`** to each moving NPC; its radius/height/speed must match the baked
   agent type, and it must spawn *on* the baked mesh.
4. **Drive it from script** with `SetDestination(targetPos)`; the agent steers and avoids other
   agents automatically. Detect arrival with `remainingDistance`/`pathPending`.
5. **Handle dynamic blockers** with `NavMeshObstacle` (carving) so closed doors/crates block
   paths without a full re-bake.
6. **Verify** with the AI Navigation overlay (the baked mesh is drawn in the Scene view) and by
   watching agents path around obstacles to the goal; check `NavMeshPath.status` for
   unreachable targets.

## Patterns

### 1. Chase/seek with a NavMeshAgent

```csharp
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Chaser : MonoBehaviour
{
    [SerializeField] private Transform target;
    private NavMeshAgent _agent;

    private void Awake() => _agent = GetComponent<NavMeshAgent>();

    private void Update()
    {
        if (target) _agent.SetDestination(target.position);   // re-path toward the target
    }

    // Arrived? pathPending guards the first frame before a path exists.
    private bool HasArrived() =>
        !_agent.pathPending && _agent.remainingDistance <= _agent.stoppingDistance;
}
```

### 2. Check reachability before committing

```csharp
using UnityEngine.AI;

public bool CanReach(NavMeshAgent agent, Vector3 destination)
{
    var path = new NavMeshPath();
    agent.CalculatePath(destination, path);
    return path.status == NavMeshPathStatus.PathComplete;   // vs Partial / Invalid
}
```

### 3. Bake at runtime (for procedurally built or streamed levels)

```csharp
using Unity.AI.Navigation;   // the package namespace (NavMeshSurface)

[SerializeField] private NavMeshSurface surface;

// After spawning level geometry, build the navmesh in code.
public void RebuildNav() => surface.BuildNavMesh();
```

### 4. Dynamic obstacle that carves the mesh

```csharp
// Add a NavMeshObstacle (Carve = true) to a door/crate. While present it cuts a hole in the
// navmesh so agents route around it; remove/disable it to reopen the path — no re-bake needed.
```

### 5. Connect separate mesh pieces with a NavMeshLink (jumps, doors, gaps)

```csharp
// Two baked surfaces that don't touch (a ledge and the floor below, two platforms across a
// gap) are separate islands — an agent can't path between them. Add Component > Navigation >
// NavMesh Link to bridge them: assign Start/End Transforms, set Width (0 = point-to-point),
// and toggle Bidirectional for one-way vs two-way. NavMeshLink lives in Unity.AI.Navigation.
// It replaces the deprecated built-in OffMeshLink (see pitfalls).
```

## Pitfalls

- **Looking for the Bake tab or the Navigation Static flag** — the old Navigation window was
  removed in AI Navigation 2.0. Bake from a `NavMeshSurface` component; the package's
  Window → AI → Navigation only edits agent types and areas.
- **Agent doesn't move / warps to origin** — it isn't on the baked mesh, or no surface was
  baked. Bake the surface and spawn the agent on it (`NavMesh.SamplePosition` to snap).
- **Agent ignores new geometry** — the navmesh is baked; runtime-spawned obstacles need a
  `NavMeshObstacle` (carving) or a `surface.BuildNavMesh()` re-bake.
- **`SetDestination` every frame is wasteful** — for a slow-moving target, re-path on a timer
  (e.g. every 0.2s) instead of each frame.
- **An NPC with a Rigidbody jitters or drifts off its path** — a `NavMeshAgent` and a
  non-kinematic `Rigidbody` both move the transform. Tick **Is Kinematic** while the agent
  is in control.
- **An agent with a `NavMeshObstacle` on the same GameObject spins or slides** — it tries to
  avoid itself (worse with carving). Keep only one of them enabled at a time, e.g. switch the
  agent off and the obstacle on when the NPC stops for good.
- **Teleporting an agent** — use `agent.Warp(position)` (returns false if it fails), not a
  plain Transform write.
- **Agent radius/height mismatch** — if the `NavMeshAgent`'s size differs from the baked agent
  type, it gets stuck in gaps or floats; keep them consistent.
- **Agents jitter against each other** — tune `avoidancePriority` and quality, or use an
  obstacle for truly static blockers rather than relying on agent avoidance.
- **Reaching for `OffMeshLink`** — the built-in `OffMeshLink` component is **deprecated** in
  AI Navigation 2.0 and can no longer be added from the Add Component menu. Use a
  **`NavMeshLink`** (from the package, `Unity.AI.Navigation`) instead — it adds Transform-based
  endpoints and a runtime `activated` property. Migrate any existing `OffMeshLink`s.
- **`CalculatePath` returns `PathPartial`** — the destination sits on a *different* baked
  island than the agent (a gap the mesh doesn't cross). Bridge the two with a `NavMeshLink`
  (pattern 5) or extend the geometry so one surface covers both; a partial path only reaches
  the near edge.

## References

- Primary docs: AI Navigation package manual
  (`https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/index.html`),
  the `NavMeshLink` page
  (`https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/NavMeshLink.html`)
  and its "What's new" note on the `OffMeshLink` deprecation
  (`https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/whats-new.html`), the
  "Navigation window" and "Use NavMesh Agent with other components" pages
  (`NavigationWindow.html`, `MixingComponents.html` in the same manual), plus
  `ScriptReference/AI.NavMeshAgent`, `ScriptReference/AI.NavMesh`.

## Related skills

- `game-ai` — engine-agnostic decision-making (FSM, behaviour trees, steering) that *uses* this.
- `unity-csharp-scripting` — the MonoBehaviour structure around the agent.
- `tower-defense` / `fps-shooter` — genres that compose pathfinding with gameplay.


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
