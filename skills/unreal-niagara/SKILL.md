---
name: unreal-niagara
description: >
  Create and control VFX in Unreal Engine 5 with Niagara: systems and emitters, modules and
  the spawn/update stages, exposed User parameters, and spawning or driving effects from
  Blueprints or C++. Use when building particle effects, NS_/NE_ assets, spawning a Niagara
  system at runtime, setting User parameters, or when the user mentions Niagara, VFX, or a
  particle system in Unreal.
---

# Unreal Niagara VFX

Build and control real-time visual effects in UE5 with Niagara: understand the
System/Emitter/Module hierarchy, expose parameters you can drive from gameplay, and spawn
effects at runtime. Targets **UE 5.8**. (Niagara replaces the legacy Cascade system.)

## When to use

- Use when creating a Niagara System (`NS_`) and Emitters (`NE_`), wiring modules in the
  spawn/update stages, exposing **User** parameters to gameplay, or spawning/driving an effect
  (impact, muzzle flash, fire, magic) from Blueprint or C++.
- Use when the project has Niagara `NS_`/`NE_` assets or references `UNiagaraComponent`.

**When *not* to use:** material/shader authoring (the look of a surface, not particles) is a
separate topic; `shader-programming` covers cross-engine shader concepts. Audio for the effect
→ `audio-design`.

## Core workflow

1. **Understand the hierarchy.** A **Niagara System** (`NS_`) is the effect you place/spawn; it
   contains one or more **Emitters** (`NE_`, often emitter *templates*). Each emitter runs in
   stages: **Emitter Spawn/Update**, **Particle Spawn/Update**, optional **Event Handler**, and
   **Render**.
2. **Build behaviour from Modules**, which execute top-to-bottom in each stage (Spawn Rate,
   Add Velocity, Gravity Force, Color over Life, etc.). Order matters — a later module reads the
   values earlier ones wrote.
3. **Know the parameter namespaces:** `System`, `Emitter`, `Particle`, and **`User`**. Only
   **User-namespace** parameters are exposed to and settable from Blueprint/C++; the others are
   internal to the simulation.
4. **Spawn at runtime** with `UNiagaraFunctionLibrary::SpawnSystemAtLocation` (world position)
   or `SpawnSystemAttached` (follows a component/socket), which return a `UNiagaraComponent`.
5. **Drive the effect** by setting its User parameters on the returned component (color, spawn
   rate, a target position) and `Activate`/`Deactivate` it.
6. **Verify** in the Niagara editor preview and in-level; check bounds (especially GPU
   emitters), and confirm the effect culls/destroys correctly.

## Patterns

### 1. Spawn a one-shot effect at a world location (C++)

```cpp
#include "NiagaraFunctionLibrary.h"
#include "NiagaraComponent.h"

// ImpactSystem is a UPROPERTY(EditAnywhere) TObjectPtr<UNiagaraSystem>.
void AProjectile::SpawnImpact(const FVector& Location, const FRotator& Rotation)
{
    UNiagaraComponent* FX = UNiagaraFunctionLibrary::SpawnSystemAtLocation(
        GetWorld(), ImpactSystem, Location, Rotation);
    // FX auto-destroys when finished for a one-shot (system marked non-looping).
}
```

### 2. Spawn attached to a socket (muzzle flash that follows the gun)

```cpp
UNiagaraComponent* Muzzle = UNiagaraFunctionLibrary::SpawnSystemAttached(
    MuzzleSystem, WeaponMesh, FName("MuzzleSocket"),
    FVector::ZeroVector, FRotator::ZeroRotator,
    EAttachLocation::SnapToTarget, /*bAutoDestroy*/ true);
```

### 3. Drive an exposed User parameter at runtime

```cpp
// Only User-namespace parameters can be set from gameplay. Names match the User parameter.
if (UNiagaraComponent* Fire = UNiagaraFunctionLibrary::SpawnSystemAttached(
        FireSystem, RootComponent, NAME_None, FVector::ZeroVector, FRotator::ZeroRotator,
        EAttachLocation::KeepRelativeOffset, /*bAutoDestroy*/ false))
{
    Fire->SetVariableFloat(FName("SpawnRate"), 250.f);                 // User.SpawnRate
    Fire->SetVariableLinearColor(FName("FireColor"), FLinearColor::Red);
}
```

### 4. Blueprint equivalent (node flow)

```text
Spawn System at Location (System = NS_Impact, Location, Rotation)  -> returns Niagara Component
On the returned component:
  Set Niagara Variable (Float)  Name="SpawnRate"  Value=250
  Set Niagara Variable (LinearColor)  Name="FireColor"  Value=Red
```

## Pitfalls

- **Trying to set a System/Emitter/Particle parameter from gameplay** — it won't take. Expose
  it in the **User** namespace; only User parameters are settable via the component.
- **Using Cascade tutorials** — Cascade is deprecated and no longer developed. Niagara is the
  current system; the emitter/module workflow differs. For existing Cascade assets, the
  **Cascade To Niagara Converter** plugin gives a starting point to port from.
- **Crash on the spawned component** — `SpawnSystemAtLocation`/`SpawnSystemAttached` can return
  `nullptr` (no system asset, or the effect was culled before spawning by its scalability
  settings). Null-check the result before setting parameters. Both functions are marked unsafe
  during actor construction, so spawn from `BeginPlay` or later, not the Construction Script.
- **Effect disappears or doesn't cull right** — fixed/incorrect bounds, especially for **GPU
  Compute** emitters which need explicit Fixed Bounds. Set bounds on the emitter/system.
- **Looping effect never stops** — spawned with `bAutoDestroy = false` and never
  `Deactivate()`d; manage the returned component's lifetime, or mark the system non-looping for
  one-shots.
- **GPU sim can't drive gameplay** — GPU particle data isn't readily read back to the CPU;
  collision/events that gameplay must react to should use CPU emitters (or Niagara → gameplay
  via the data interface), not GPU.
- **Module order bugs** — a Force/Velocity module placed before the one that initializes the
  value reads zero. Mind the top-to-bottom stack order.

## References

- Primary docs: "Overview of Niagara Effects"
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-niagara-effects-for-unreal-engine`)
  and the `UNiagaraFunctionLibrary` / `UNiagaraComponent` API. Add the `Niagara` module to
  `*.Build.cs` for C++ access.

## Related skills

- `shader-programming` — material/shader concepts for particle materials.
- `unreal-cpp-gameplay` — spawning effects from gameplay code and module setup.
- `unreal-blueprints` — triggering effects from visual scripts.


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
