---
name: unreal-behavior-trees
description: >
  Build NPC AI in Unreal Engine 5 with Behavior Trees and Blackboards: composites
  (Selector/Sequence), tasks, decorators, services, and running the tree from an AIController.
  Use when creating enemy/NPC AI, BT_/BB_ assets, custom BTTask or BTService nodes, or when
  the user mentions Behavior Tree, Blackboard, AIController, BTTask, decorator, or service.
---

# Unreal Behavior Trees

Author NPC decision-making in UE5 with Behavior Trees driven by a Blackboard: structure the
tree with composites, gate branches with decorators, keep state current with services, and run
it from an AIController. Targets **UE 5.8**.

## When to use

- Use when building enemy/NPC AI: creating a `BT_`/`BB_` asset pair, structuring
  Selector/Sequence branches, adding decorators (conditions) and services (periodic updates),
  writing custom `BTTask`/`BTService` nodes, or wiring an AIController to run the tree.
- Use when the project has Behavior Tree (`BT_`) and Blackboard (`BB_`) assets and an
  `AAIController`.

**When *not* to use:** the *concept* of AI (FSM vs BT vs steering, cross-engine) →
`game-ai`. Pure navigation/pathing math is engine navmesh (BT's `MoveTo` uses it). Simple
one-off logic may be cheaper as a small state machine than a full tree.

**Behavior Tree or StateTree?** UE 5.8 ships both, and Behavior Trees are not deprecated.
StateTree is Epic's general-purpose hierarchical state machine: it combines BT-style
selection with explicit States and Transitions. If the project already uses StateTree
assets, or the AI is naturally a set of modes with clear transitions (patrol → alert →
combat), check with the user before adding a Behavior Tree next to it. Keep using Behavior
Trees where the project already has `BT_`/`BB_` assets.

## Core workflow

1. **Create the pair:** a Blackboard (`BB_`) holds typed keys (the AI's memory: `TargetActor`,
   `LastKnownLocation`, `bIsInvestigating`); a Behavior Tree (`BT_`) references that Blackboard.
2. **Possess and run.** An `AAIController` possesses the pawn and calls `RunBehaviorTree(BT)`,
   which also initializes the referenced Blackboard.
3. **Structure with composites.** **Selector** runs children left→right until one *succeeds*
   (priority/fallback: "attack, else chase, else patrol"). **Sequence** runs children until one
   *fails* (do-all: "move to cover → reload → peek"). **Simple Parallel** runs one main task
   alongside a secondary.
4. **Gate branches with Decorators** that read Blackboard keys (e.g. "Has Target?" guards the
   combat branch). Set **Observer Aborts** so the tree re-evaluates when the key changes.
5. **Keep the Blackboard current with Services** attached to a branch — they tick periodically
   (e.g. update `TargetActor` via a sight check) only while that branch is active.
6. **Do work in Tasks**, which return `Succeeded`, `Failed`, or `InProgress` (latent tasks like
   `MoveTo` finish later).
7. **Verify** with the Behavior Tree debugger during PIE — it highlights the running node and
   shows live Blackboard values, so you see exactly which branch executes.

## Patterns

### 1. AIController that runs the tree (C++)

```cpp
void AEnemyAIController::OnPossess(APawn* InPawn)
{
    Super::OnPossess(InPawn);
    if (BehaviorTree)                 // UPROPERTY(EditAnywhere) TObjectPtr<UBehaviorTree>
        RunBehaviorTree(BehaviorTree); // initializes & uses the Blackboard the BT references
}
```

### 2. A priority tree (node structure)

```text
ROOT
└── Selector (try combat, else investigate, else patrol)
    ├── Sequence            [Decorator: Blackboard 'TargetActor' Is Set, Observer Aborts: Both]
    │     ├── Task: MoveTo (TargetActor)          // latent: returns InProgress then Succeeded
    │     └── Task: Attack
    ├── Sequence            [Decorator: 'LastKnownLocation' Is Set]
    │     ├── Task: MoveTo (LastKnownLocation)
    │     └── Task: Wait (3s) + clear key
    └── Task: Patrol (BTTask_FindPatrolPoint -> MoveTo)
```

`Observer Aborts: Both` makes the combat branch interrupt patrol the instant `TargetActor` is
set, and bail out when it's cleared — this is what makes the AI feel reactive.

### 3. Updating the Blackboard from code (e.g. on seeing the player)

```cpp
void AEnemyAIController::SetTarget(AActor* Target)
{
    if (UBlackboardComponent* BB = GetBlackboardComponent())
        BB->SetValueAsObject(TEXT("TargetActor"), Target);   // key name must match the BB asset
}
// Clear with BB->ClearValue(TEXT("TargetActor")); to drop back to a lower-priority branch.
```

## Pitfalls

- **AI never starts** — the pawn isn't possessed (set the Pawn's *Auto Possess AI* to "Placed
  in World or Spawned" and assign the AIController), or `RunBehaviorTree` was never called.
- **`MoveTo` instantly fails** — no NavMesh in the level (add a Nav Mesh Bounds Volume), or the
  target is off the navmesh.
- **Branch doesn't react to changes** — the gating Decorator's **Observer Aborts** is set to
  None; set it to Self/Lower Priority/Both so the tree re-evaluates when the key changes.
- **A task hangs the tree** — a custom task returned `InProgress` and never calls
  `FinishLatentTask`. Always complete latent tasks.
- **AI behaves strangely only when several NPCs share a tree** — a custom task stores run state
  in member variables. Task nodes are shared by every AI using the asset unless instanced; keep
  per-AI state in node memory (see the reference).
- **Blackboard key typos** — `SetValueAsObject("Taget", ...)` silently does nothing; match the
  key name and type exactly, or use a cached `FBlackboardKeySelector`.
- **Sequence vs Selector confusion** — Sequence = AND (stops on first failure); Selector = OR
  (stops on first success). Swapping them inverts the behaviour.

## References

- For a **custom C++ `UBTTaskNode`** (instant and latent `ExecuteTask` returning `EBTNodeResult`,
  per-AI node memory, `AbortTask`, and a `FBlackboardKeySelector`), read
  `references/custom-bttask.md`.
- Primary docs: "Behavior Trees in Unreal Engine"
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-trees-in-unreal-engine`).

## Related skills

- `game-ai` — engine-agnostic AI design (FSM, BT, steering, pathfinding choices).
- `unreal-cpp-gameplay` — the AIController and pawn classes in C++.
- `fps-shooter` / `tower-defense` — genres that compose enemy AI.


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
