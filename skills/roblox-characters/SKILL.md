---
name: roblox-characters
description: >
  Build respawn-safe Roblox character systems around Players, CharacterAdded/CharacterRemoving,
  Humanoid, HumanoidRootPart, Animator, R6/R15 rigs, movement, animations and markers, death,
  tools, accessories, ownership, and custom characters. Use when character scripts break after
  respawn, cache stale Humanoids, control movement or velocity, load AnimationTracks, handle death,
  equip Tools, modify avatars, or support custom player rigs.
---

# Roblox characters

Treat a `Player` as the durable identity and each `Character` as a replaceable session with its own
references, connections, animation tracks, and cleanup. Targets Roblox's rolling platform APIs.

## When to use

- Use for player-character lifecycle, Humanoid state/movement, rigs, animations, tools,
  accessories, custom characters, death, or respawn defects.
- Use whenever code stores a Character/Humanoid/root reference longer than one spawn.

**When not to use:** general physics queries and constraints belong to `roblox-physics`; remote
trust belongs to `roblox-networking`; camera logic belongs to `camera-systems`.

## Workflow

1. **Inspect the character contract.** Check avatar settings, `StarterCharacter`,
   `StarterCharacterScripts`, `CharacterAutoLoads`, R6/R15 support, existing Animate/controller
   scripts, tools, tags, collision groups, and server/client ownership.
2. **Separate scopes.** Player-scope state survives respawn; character-scope state does not. Put
   character connections/tracks/resources in one cleanup scope and destroy it on removal.
3. **Bind existing and future characters.** Connect `CharacterAdded`, then bind `player.Character`
   if present. Do not assume event subscription alone sees a character that already spawned.
4. **Resolve required components defensively.** Wait with a timeout where replication warrants it;
   validate `Humanoid`, root, `Animator`, and rig assumptions. Abort if that character is no longer
   current before applying delayed work.
5. **Choose movement ownership.** Use Humanoid movement for standard avatars; use
   `AssemblyLinearVelocity`, `BasePart:ApplyImpulse()`, or a `LinearVelocity`/`AlignPosition`
   constraint only for mechanics that need physical control. Keep gameplay
   authority and network ownership implications explicit.
6. **Own animation lifecycle.** Load via the rig's `Animator`; store tracks/connections; use named
   markers for gameplay timing only with server validation; stop/disconnect on character cleanup.
7. **Verify lifecycle stress.** Spawn, die, reset, rapid-respawn, swap rig if supported, equip/drop
   tools, leave during setup, and run with at least two players when character interactions matter.

## Pattern: replaceable character scope

```lua
local Players = game:GetService("Players")
local player = Players.LocalPlayer
local generation = 0
local connections: {RBXScriptConnection} = {}
local currentCharacter: Model? = nil

local function clearCharacter()
    generation += 1
    for _, connection in connections do connection:Disconnect() end
    table.clear(connections)
    currentCharacter = nil
end

local function bindCharacter(character: Model)
    -- Guard BEFORE teardown. A stale invocation (see the CharacterAdded/defer race below) must not
    -- clear a binding that is already current, or nothing ends up bound at all.
    if player.Character ~= character then return end
    clearCharacter()
    currentCharacter = character
    local thisGeneration = generation
    local humanoid = character:WaitForChild("Humanoid", 10)
    local root = character:WaitForChild("HumanoidRootPart", 10)
    -- Re-check after the yields: a respawn during WaitForChild bumps generation and makes this call stale.
    if not humanoid or not root or generation ~= thisGeneration then return end

    table.insert(connections, humanoid.Died:Connect(function()
        if generation ~= thisGeneration then return end
        setCharacterUiEnabled(false)
    end))
    attachCurrentCharacterSystems(character, humanoid, root)
end

player.CharacterRemoving:Connect(function(character)
    if currentCharacter == character then clearCharacter() end
end)
player.CharacterAdded:Connect(bindCharacter)
if player.Character then task.defer(bindCharacter, player.Character) end
```

Use the project's cleanup utility when one exists; do not introduce a new framework for three
connections. Server systems repeat this binding per `Player` and clear player-scope tables on
`PlayerRemoving`.

## Pattern: animation through Animator and markers

```lua
local animation = Instance.new("Animation")
animation.AnimationId = "rbxassetid://1234567890"
local track = animator:LoadAnimation(animation)
local markerConnection = track:GetMarkerReachedSignal("Commit"):Connect(function(parameter)
    playLocalSwingEffect(parameter) -- presentation; server still validates any hit
end)

track:Play(0.1)
-- On character teardown:
markerConnection:Disconnect()
track:Stop(0.1)
animation:Destroy()
```

For rigs without a `Humanoid`, use an `AnimationController` with an `Animator`. Do not use the
deprecated convenience path as a substitute for owning the actual Animator and track lifecycle.

## Movement and rig rules

- Do not hardcode R15 limb names if R6 is supported. Prefer attachments, tags, or a rig-type
  adapter; branch on `Humanoid.RigType` only where topology materially differs.
- `HumanoidRootPart` is the usual character assembly root, not a universal guarantee for every
  custom model. Define the custom rig contract and validate it at spawn.
- Prefer `Humanoid:Move()`/standard controls for ordinary avatar locomotion. Directly changing
  `AssemblyLinearVelocity` is an instantaneous physical action; use forces/constraints or impulses
  when continuous or instantaneous physics is the real intent.
- To rebind movement/jump or add actions like sprint, prefer the Input Action System
  (`InputContext`/`InputAction`/`InputBinding`, defined at edit time and cross-device)
  over hooking `UserInputService` directly. Default player and character control scripts
  run on this system when `Workspace.PlayerScriptsUseInputActionSystem` is enabled,
  exposing default `PlayerScripts` contexts; give your own `InputContext` a higher
  `Priority` (and `Sink`) to take precedence over the default bindings. See the
  `roblox-ui` input and navigation reference for the UI-focus side of this.
- Check whether the place opted into the Character Controller Library (beta; Avatar Settings ⟩
  Movement ⟩ Abilities) or a `ControllerManager` setup. Those replace `HumanoidStateType`-driven
  logic with abilities/controllers, so extend that system instead of layering Humanoid state
  changes on top of it.
- Never grant damage or movement authority because a client owns its character physics. Validate
  cross-player consequences on the server.
- Tools move between Backpack and Character during equip; listen to lifecycle/state rather than
  assuming one fixed parent. Modify accessories/appearance through current character APIs and
  preserve an up-to-date applied `HumanoidDescription` when editing avatar appearance.

## Common failures

| Symptom | Likely cause | Remedy |
|---|---|---|
| works once, breaks after reset | cached character/Humanoid/root | rebuild per `CharacterAdded`; clear on removal |
| callbacks fire twice after deaths | old character connections survived | character-scoped cleanup and generation/current checks |
| delayed load edits wrong rig | async work outlived spawn | compare current Character/generation after every yield |
| animation visible only locally or not at all | wrong Animator/context/asset ownership | inspect rig Animator, execution side, permissions, and replication |
| hit marker awards impossible hit | animation marker trusted as authority | use marker for timing/presentation; server validates combat state |
| R6/custom rig errors | R15 names assumed | define rig contract; attachments/adapter; test each supported rig |
| tool disappears from system | fixed Backpack/Character parent assumed | handle equip/unequip ancestry and character replacement |
| custom force fights Humanoid | two controllers own motion | choose one movement authority per state and restore cleanly |

## Resources

- Read `references/lifecycle-and-animation.md` for server binding, death vs removal, rig and
  animation verification, custom characters, and the lifecycle stress matrix.

## Related skills

- `roblox-physics` — forces, constraints, assemblies, collision, and network ownership.
- `roblox-networking` — server validation of character actions and stale requests.
- `input-systems` — action mapping and responsive movement intent.
- `camera-systems` — camera behavior following replaceable characters.

## Primary references

- `https://create.roblox.com/docs/characters`
- `https://create.roblox.com/docs/animation/using`
- `https://create.roblox.com/docs/characters/appearance`
- `https://create.roblox.com/docs/characters/character-controller-library`


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
