---
name: roblox-physics
description: >
  Implement Roblox physical simulation and queries with assemblies, anchoring, constraints,
  collision groups, CanCollide/CanTouch/CanQuery, raycasts and overlap queries, mass, impulses,
  forces, velocity, moving assemblies, cleanup, and network ownership. Use for Roblox collisions,
  hit detection, RaycastParams, PhysicsService, projectiles, vehicles, knockback, constraints,
  deprecated BodyMovers, unstable motion, or client-owned physics exploits.
---

# Roblox physics

Choose deliberately between simulation, character control, hit detection, and visual-only motion;
they are different jobs. Targets Roblox's rolling platform APIs. Pair with `physics-tuning` for
engine-neutral stability and feel.

## When to use

- Use for BasePart assemblies, constraints, collision/query policy, ray/overlap queries, forces,
  impulses, moving physical objects, network ownership, or physics cleanup.
- Use when `Touched` is unreliable/security-sensitive, parts tunnel or jitter, a mechanism breaks
  when anchored, or old BodyMover patterns appear.

**When not to use:** ordinary Humanoid lifecycle/control belongs to `roblox-characters`; remote
validation belongs to `roblox-networking`; decorative UI/world motion may only need a tween.

## Decide the system first

| Goal | Mechanism |
|---|---|
| sustained physical interaction | unanchored assembly + modern constraints/forces |
| instantaneous physical change | `ApplyImpulse` / `ApplyAngularImpulse` |
| kinematic platform/path | controlled pivot/transform with an explicit passenger policy |
| character locomotion | Humanoid/custom character controller (`roblox-characters`) |
| authoritative hit test | server raycast/overlap with filters and gameplay validation |
| cosmetic trail/recoil | local visual motion; no gameplay authority |

## Workflow

1. **Inspect the mechanism.** In Studio, visualize assemblies, anchors, constraints, collision
   groups, massless parts, and network owners. Identify the assembly root and intended authority.
2. **Define interaction policy.** Write the collision-group matrix and separately decide
   `CanCollide`, `CanTouch`, and `CanQuery`. These flags are not interchangeable. Register groups
   in the Studio Collision Groups editor or with `Workspace:RegisterCollisionGroup()` and
   `Workspace:CollisionGroupSetCollidable()`; the `PhysicsService` collision-group methods are
   deprecated and forward to `Workspace`.
3. **Choose simulation or query.** Do not use `.Touched` as a universal hit detector. Use a ray for
   a path/line, an overlap query for a volume, and simulation contacts when physical response is
   actually required.
4. **Apply motion at assembly level.** Forces on a part affect its assembly. Use modern
   `LinearVelocity`, `AngularVelocity`, `VectorForce`, `AlignPosition`, and `AlignOrientation`
   constraints as appropriate; migrate deprecated BodyMovers when changing that system.
5. **Set ownership deliberately.** Server-own gameplay-critical loose assemblies when required;
   client ownership can improve responsiveness but never authorizes gameplay results.
6. **Bound cost and lifetime.** Reuse query parameters, cap query frequency/result count, remove
   temporary constraints/attachments, and disconnect event listeners.
7. **Verify under load and multiplayer.** Test anchored/unanchored transitions, mass extremes,
   collision matrix, fast motion, multiple clients, ownership changes, streaming, and cleanup.

## Pattern: filtered server raycast

```lua
local Workspace = game:GetService("Workspace")

local params = RaycastParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude
params.FilterDescendantsInstances = {shooterCharacter}
params.IgnoreWater = true
params.CollisionGroup = "WeaponQuery"

local direction = aimDirection.Unit * MAX_RANGE
local result = Workspace:Raycast(muzzlePosition, direction, params)
if result then
    local model = result.Instance:FindFirstAncestorOfClass("Model")
    local humanoid = model and model:FindFirstChildOfClass("Humanoid")
    if humanoid and serverCanDamage(shooter, model, result.Position) then
        humanoid:TakeDamage(serverWeaponDamage(shooter))
    end
end
```

The server must validate the origin/direction against server-known character/weapon state; do not
accept an arbitrary client origin and treat the raycast itself as validation.

## Pattern: overlap volume with explicit policy

```lua
local params = OverlapParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude
params.FilterDescendantsInstances = {sourceCharacter}
params.CollisionGroup = "DamageQuery"
params.MaxParts = 64

local seen: {[Model]: boolean} = {}
for _, part in Workspace:GetPartBoundsInBox(hitboxCFrame, hitboxSize, params) do
    local model = part:FindFirstAncestorOfClass("Model")
    if model and not seen[model] then
        seen[model] = true
        validateAndApplyHit(model)
    end
end
```

Bounds queries use bounding boxes and can include multiple parts from one target; deduplicate and
perform exact/gameplay checks as needed. For exact geometry use `WorldRoot:GetPartsInPart(part, overlapParams)`
only when its additional cost is justified. Note `OverlapParams.RespectCanCollide` decides whether a
query honours `CanCollide` or `CanQuery` — set it deliberately, or it silently overrides the flag
policy below. `OverlapParams.Tolerance` controls contact slop.

## Assemblies, force, and ownership

- Welded parts form one rigid assembly; force, impulse, velocity, mass, and ownership operate on
  that assembly. Anchoring a part changes simulation/ownership and can make an assembly effectively
  infinite mass.
- Apply an impulse for a one-time change; use a force or velocity constraint for sustained control.
  Setting `AssemblyLinearVelocity` is an immediate state change, not a continuous force model.
- Prefer attachments plus modern constraints over `BodyPosition`, `BodyVelocity`, `BodyGyro`, and
  other deprecated BodyMovers when authoring or revising a mechanism.
- Automatic ownership may move nearby unanchored assemblies to clients. Use
  `SetNetworkOwner(nil)` conservatively for critical objects, then measure responsiveness/server
  cost. Visualize network owners in Studio.
- A client owner can manipulate physical results and `.Touched` observations. The server validates
  consequential hits, positions, timing, and permissions independently.
- If `Workspace.AuthorityMode` is `Server`, the server owns simulation and clients predict parts
  near their own character with rollback (`RunService:SetPredictionMode()`, client-only, overrides
  per instance). Drive
  predicted forces and constraints from `RunService:BindToSimulation()` on both sides rather than
  from `Heartbeat` or client-only scripts; custom physics scripts need adapting when a place
  switches modes. See `roblox-networking`.

## Common failures

| Symptom | Likely cause | Remedy |
|---|---|---|
| welded mechanism will not move | one part anchored | inspect full assembly; anchor only intentional world roots |
| force behaves too strongly/weakly | assembly mass ignored | inspect `AssemblyMass`; tune force/impulse by intended acceleration |
| hit misses fast projectile | discrete touch sampling/tunneling | swept query — `WorldRoot:Blockcast()`, `Spherecast()`, or `Shapecast()` — plus `physics-tuning`; do not rely only on `.Touched` |
| ray hits shooter/effects | filters/collision group absent | reuse explicit params and query group |
| same target damaged many times | overlap returned multiple body parts | deduplicate by target model and enforce attack ID/cooldown |
| exploit fires impossible touch | client owns relevant physics | server query/context validation; deliberate ownership |
| invisible trigger blocks or cannot query | three flags conflated | set `CanCollide`, `CanTouch`, `CanQuery` independently |
| mechanism leaks attachments | temporary constraint lifecycle missing | own and destroy constraints, attachments, and connections together |

## Resources

- Read `references/queries-and-ownership.md` for collision/query matrices, assembly debugging,
  ownership security, migration choices, and the physics verification matrix.

## Related skills

- `physics-tuning` — timestep, jitter, tunneling, mass ratios, and stability methodology.
- `roblox-characters` — Humanoid/custom movement and respawn lifecycle.
- `roblox-networking` — authoritative validation of client-requested physical actions.
- `roblox-studio-workflow` — visualization, Output, and multi-client verification.

## Primary references

- `https://create.roblox.com/docs/physics/assemblies`
- `https://create.roblox.com/docs/physics/network-ownership`
- `https://create.roblox.com/docs/workspace/raycasting`


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
