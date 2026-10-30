---
name: unreal-cpp-gameplay
description: >
  Write Unreal Engine 5 C++ gameplay code: the UCLASS/UPROPERTY/UFUNCTION reflection macros,
  the Gameplay Framework (GameMode, Pawn, Character, PlayerController, Actor components), and
  the module Build.cs. Use when writing or debugging UE C++, deriving from AActor/ACharacter/
  AGameModeBase, exposing properties to the editor or Blueprints, or when the user mentions
  Unreal C++, UCLASS, GENERATED_BODY, GameMode, ACharacter, or .Build.cs.
---

# Unreal C++ Gameplay

Write correct UE5 gameplay C++: the reflection macros that connect C++ to the editor and
Blueprints, the Gameplay Framework class roles, and module dependencies. Targets **UE 5.8**.

## When to use

- Use when creating C++ gameplay classes (`AActor`, `APawn`, `ACharacter`, `AGameModeBase`,
  `UActorComponent`), exposing properties/functions with `UPROPERTY`/`UFUNCTION`, setting up a
  GameMode's default classes, or adding a module dependency in `*.Build.cs`.
- Use when the project has a `Source/` tree with `*.h`/`*.cpp` using `UCLASS`, and `*.Build.cs`.

**When *not* to use:** designer-facing visual logic → `unreal-blueprints`. Player input
binding details → `unreal-enhanced-input`. AI logic → `unreal-behavior-trees`. This skill owns
the C++ class/reflection foundation those build on.

## Core workflow

1. **Name with the right prefix.** `A` = Actor-derived, `U` = `UObject`/component-derived,
   `F` = plain struct, `E` = enum, `I` = interface. The prefix must match the base class.
2. **Declare the class with reflection macros.** `UCLASS()` above the class, `GENERATED_BODY()`
   as the first line in the body, and `#include "ClassName.generated.h"` as the **last**
   include in the header.
3. **Expose data with `UPROPERTY`** (editor/Blueprint visibility *and* garbage-collection
   tracking) and behaviour with `UFUNCTION` (`BlueprintCallable`, etc.).
4. **Create components in the constructor** with `CreateDefaultSubobject<T>(TEXT("Name"))` and
   set the `RootComponent`.
5. **Know the framework roles:** `AGameModeBase` sets the rules + default classes; `APawn`/
   `ACharacter` is the controllable body; `APlayerController` is the player's will;
   `UActorComponent` is reusable behaviour.
6. **Add module dependencies** to `*.Build.cs` (e.g. `EnhancedInput`) or unresolved-symbol
   link errors follow.
7. **Verify** by compiling (Live Coding `Ctrl+Alt+F11` from the editor, or a full build from
   the IDE with the editor closed) and checking the class/properties appear in the editor. For
   automation tests, run headless with
   `UnrealEditor-Cmd <Project>.uproject -ExecCmds="Automation RunTest MyGame;Quit"`
   (`RunTest` takes a test name, a dotted prefix, or `Group:<name>`).

## Patterns

### 1. Minimal Actor class (header + source)

```cpp
// Pickup.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Pickup.generated.h"          // MUST be the last include

UCLASS()
class MYGAME_API APickup : public AActor   // MYGAME_API = your module's export macro
{
    GENERATED_BODY()
public:
    APickup();

    // EditAnywhere = tweak per-instance & on the CDO; BlueprintReadWrite = BP get/set.
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pickup")
    int32 ScoreValue = 10;

    // UPROPERTY on a UObject* pointer is what keeps it from being garbage-collected.
    UPROPERTY(VisibleAnywhere)
    TObjectPtr<UStaticMeshComponent> Mesh;   // UE5: TObjectPtr instead of raw UStaticMeshComponent*

    UFUNCTION(BlueprintCallable, Category = "Pickup")
    void Collect();

protected:
    virtual void BeginPlay() override;
};
```

```cpp
// Pickup.cpp
#include "Pickup.h"
#include "Components/StaticMeshComponent.h"

APickup::APickup()
{
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = Mesh;                     // the mesh is this actor's root
}

void APickup::BeginPlay() { Super::BeginPlay(); }   // always call Super
void APickup::Collect()   { Destroy(); }
```

### 2. GameMode wiring its default classes

```cpp
// MyGameMode.cpp — set in the constructor so the engine spawns your classes.
AMyGameMode::AMyGameMode()
{
    DefaultPawnClass      = AMyCharacter::StaticClass();
    PlayerControllerClass = AMyPlayerController::StaticClass();
}
```

### 3. Module dependency in Build.cs

```csharp
// MyGame.Build.cs
PublicDependencyModuleNames.AddRange(new string[]
{
    "Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput"
});
```

## Pitfalls

- **`generated.h` not last / missing** — compile errors like "Cannot find generated header" or
  "Expected an include". It must be the final include in the header.
- **Forgetting `GENERATED_BODY()`** — UHT (Unreal Header Tool) errors; it must be the first
  thing inside the class body.
- **Raw `UObject*` without `UPROPERTY`** — the garbage collector doesn't see it and may destroy
  it out from under you. Track every UObject pointer with `UPROPERTY` (use `TObjectPtr` in UE5).
- **Header/UPROPERTY edits with Live Coding** — function-body edits are reliable. Structural
  changes (new functions, new `UPROPERTY`s) rely on Object Reinstancing, which is on by default
  but less stable; code that caches pointers to reinstanced objects must refresh them. If the
  editor or Blueprints misbehave after such a change, close the editor and build from the IDE.
- **Wrong class prefix** — naming an Actor `UFoo` (or a component `AFoo`) breaks UHT; match the
  prefix to the base type.
- **Unresolved external symbol at link** — the module providing the API isn't in `Build.cs`
  `PublicDependencyModuleNames`.
- **Not calling `Super::`** in overridden `BeginPlay`/`Tick`/etc. skips engine setup.

## References

- For `UActorComponent` creation/attachment, the `UPROPERTY` garbage-collection ownership rules
  (`TObjectPtr`, `TArray<TObjectPtr<>>`, `TWeakObjectPtr`, holding UObjects from plain C++
  classes), and a replication primer, read
  `references/components-and-gc.md`.
- Primary docs: "Unreal Engine CPP Quick Start" and "Gameplay Framework"
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine`).

## Related skills

- `unreal-blueprints` — exposing C++ to designers; BP/C++ interop.
- `unreal-enhanced-input` — binding input in a C++ Pawn/Character.
- `unreal-behavior-trees` — C++ AI tasks driven from a behaviour tree.


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
