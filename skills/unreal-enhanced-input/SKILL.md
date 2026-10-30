---
name: unreal-enhanced-input
description: >
  Set up player input in Unreal Engine 5 with Enhanced Input: Input Actions, Input Mapping
  Contexts, modifiers and triggers, adding the mapping context, and binding actions by
  ETriggerEvent. Use when wiring movement/look/jump input, creating IA_/IMC_ assets, binding
  in C++ or Blueprints, or when the user mentions Enhanced Input, Input Mapping Context,
  Input Action, IA_/IMC_, or ETriggerEvent.
---

# Unreal Enhanced Input

Wire player input the modern UE5 way with the **Enhanced Input** system: data-driven Input
Actions and Mapping Contexts instead of the legacy Project Settings axis/action mappings.
Targets **UE 5.8** (Enhanced Input is the default; legacy input is deprecated).

## When to use

- Use when adding movement/look/jump/fire input, creating Input Action (`IA_`) and Input
  Mapping Context (`IMC_`) assets, applying modifiers/triggers, adding a mapping context to a
  player, or binding actions in C++ or Blueprints.
- Use when the project has `IA_*`/`IMC_*` assets or references `EnhancedInput`.

**When *not* to use:** engine-agnostic input *architecture* (rebinding strategy, buffering,
multi-device design) → `input-systems`. The Pawn/Character C++ those bindings live in →
`unreal-cpp-gameplay`.

## Core workflow

1. **Enable the module/plugin.** Enhanced Input is on by default in UE5; for C++ binding add
   `"EnhancedInput"` to `PublicDependencyModuleNames` in `*.Build.cs`.
2. **Create Input Actions (`IA_`).** Each has a **Value Type**: `Digital (bool)` for buttons,
   `Axis1D (float)` for triggers, `Axis2D (Vector2D)` for movement/look.
3. **Create an Input Mapping Context (`IMC_`)** that maps keys/buttons to those actions. Use
   **Modifiers** to shape raw input (Negate, Swizzle Input Axis Values, Dead Zone) — e.g. WASD
   into one Axis2D needs Negate on A/S and a Swizzle on W/S. Use **Triggers** (Pressed, Hold,
   Tap) to decide *when* an action fires. The **Combo** trigger is deprecated in UE 5.8; don't
   build new input on it.
4. **Add the mapping context to the player** via the `EnhancedInputLocalPlayerSubsystem`
   (`AddMappingContext(IMC, Priority)`), usually in `BeginPlay`/possession.
5. **Bind actions** to handlers by `ETriggerEvent` (`Triggered`, `Started`, `Completed`, …) on
   the `EnhancedInputComponent`, and read the `FInputActionValue` in the handler.
6. **Verify** in PIE; the Enhanced Input debugging console commands
   (`showdebug enhancedinput`) show which actions trigger and their values.

## Patterns

### 1. Add the mapping context (C++ Character)

```cpp
void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();
    if (APlayerController* PC = Cast<APlayerController>(GetController()))
        if (ULocalPlayer* LP = PC->GetLocalPlayer())
            if (auto* Subsystem = LP->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
                Subsystem->AddMappingContext(DefaultMappingContext, /*Priority*/ 0);
}
// DefaultMappingContext is a UPROPERTY(EditAnywhere) TObjectPtr<UInputMappingContext>.
```

### 2. Bind actions and read values

```cpp
void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    // The component is an Enhanced Input component when the plugin is active.
    // (Don't name the parameter InputComponent: that shadows AActor::InputComponent.)
    if (UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        EIC->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AMyCharacter::Move);
        EIC->BindAction(LookAction, ETriggerEvent::Triggered, this, &AMyCharacter::Look);
        EIC->BindAction(JumpAction, ETriggerEvent::Started,   this, &ACharacter::Jump);
        EIC->BindAction(JumpAction, ETriggerEvent::Completed, this, &ACharacter::StopJumping);
    }
}

void AMyCharacter::Move(const FInputActionValue& Value)
{
    const FVector2D Axis = Value.Get<FVector2D>();          // Axis2D action
    AddMovementInput(GetActorForwardVector(), Axis.Y);
    AddMovementInput(GetActorRightVector(),   Axis.X);
}
```

### 3. Blueprint equivalent (node flow)

```text
Event BeginPlay
  -> Get Controller -> Cast To PlayerController -> Get Local Player
  -> Get EnhancedInputLocalPlayerSubsystem -> Add Mapping Context (IMC_Default, Priority 0)

// IA_Move is exposed as its own event node in the Character's Event Graph:
EnhancedInputAction IA_Move (Triggered)
  -> Action Value (Vector2D) -> Add Movement Input (Forward * Y, Right * X)
```

## Pitfalls

- **No input at all** — the mapping context was never added (`AddMappingContext`), or the
  player has no Local Player yet. Add it after possession/`BeginPlay`.
- **Input works in single player but not on a client, or stops after respawn** — `BeginPlay`
  ran before the controller possessed the pawn, so `GetController()` was null. Add the context
  in an override of `PawnClientRestart()`, which runs on the owning client after possession
  (Epic's Input Overview does this), or in the PlayerController.
- **Link/compile error binding in C++** — `"EnhancedInput"` isn't in `Build.cs`
  `PublicDependencyModuleNames`.
- **WASD only moves on two keys / wrong axis** — Axis2D needs **Modifiers**: Negate on the
  negative keys (A, S) and a Swizzle Input Axis Values on the vertical (W/S) so both axes map
  correctly. Raw bindings without modifiers misbehave.
- **`Get<FVector2D>()` returns zero** — value-type mismatch: the Input Action is Digital/Axis1D,
  not Axis2D. Match the `Get<T>()` to the action's Value Type.
- **Action fires every frame unexpectedly** — `Triggered` repeats while held for a Down trigger;
  use `Started`/`Completed` for one-shots (jump press/release), or a Pressed/Tap trigger.
- **Two contexts fight** — multiple mapping contexts stack by Priority; a higher-priority
  context can consume a key. Manage with priorities and `RemoveMappingContext`.

## References

- For a complete first-/third-person C++ Character with Enhanced Input (header + source,
  including look/jump and a control-rebind note), read `references/cpp-setup.md`.
- Primary docs: "Enhanced Input in Unreal Engine"
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine`)
  and "Input Overview"
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/input-overview-in-unreal-engine`).

## Related skills

- `input-systems` — engine-agnostic input architecture and rebinding strategy.
- `unreal-cpp-gameplay` — the Character/Pawn class and module setup.
- `fps-shooter` — composes input with a 3D controller and shooting.


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
