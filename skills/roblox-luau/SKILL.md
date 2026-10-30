---
name: roblox-luau
description: >
  Script a Roblox experience in Luau: get services, create and parent Instances,
  connect events, run server Scripts vs client LocalScripts, and communicate across
  the client/server boundary with RemoteEvents/RemoteFunctions (server-authoritative).
  Use when building or debugging Roblox Studio scripts — when the user mentions
  Roblox, Luau, services, RemoteEvent, Instance.new, PlayerAdded, or client vs
  server. For saving player data use roblox-datastores.
---

# Roblox Luau Scripting

Script a Roblox experience in **Luau**: services, `Instance`s, events, the
server/client split, and secure cross-boundary communication. Targets the current
Roblox engine and Studio.

## When to use

- Use when writing Roblox scripts: getting services, creating/parenting instances,
  connecting events, deciding server vs client, or wiring `RemoteEvent`/
  `RemoteFunction` communication.
- Use when the project has `Script`/`LocalScript`/`ModuleScript` objects, `.rbxl(x)`
  places, or a Rojo `*.project.json`, and code calls `game:GetService(...)`.

**When *not* to use:** persisting data across sessions → `roblox-datastores`.
Remote protocol architecture, exploit hardening, rate limits, high-frequency replication, and
multi-client abuse testing → `roblox-networking`. Generic Lua questions unrelated to the Roblox
API. Engine-agnostic input/save architecture → `input-systems` / `save-systems`.

## Core workflow

1. **Get services with `game:GetService("Name")`.** Common ones: `Players`,
   `Workspace`, `ReplicatedStorage` (shared client+server), `ServerScriptService`
   (server-only code), `ServerStorage`, `RunService`, `UserInputService` (client).
2. **Know where code runs.** A `Script` runs on the **server**; a `LocalScript`
   runs on a **client** (in `StarterPlayerScripts`, `StarterGui`, or the player's
   character). A `Script` whose `RunContext` is `Client` also runs on clients, from
   `ReplicatedStorage`; check `RunContext` before deciding where a `Script` runs. A
   `ModuleScript` is shared code you `require`.
3. **Create instances deliberately.** `local p = Instance.new("Part")`, set its
   properties, then set `p.Parent` **last** (parenting triggers replication).
4. **React with events.** `:Connect` to signals like `Players.PlayerAdded`,
   `part.Touched`, or `RunService.Heartbeat`. Disconnect when done to avoid leaks.
5. **Cross the client/server boundary with Remotes — and never trust the client.**
   Clients request via `RemoteEvent:FireServer(...)`; the server validates and
   applies. The server is authoritative for all game state.
6. **Test in Studio** with **Test** / **Test Here** / **Server & Clients**; use the
   Output window and the Client/Server toggle to confirm where code ran.
7. **Run static checks before Studio when the project already has the tools.** Put
   `std = "roblox"` in the root `selene.toml`, then run `selene .`.
   For a Rojo project, write the sourcemap once with
   `rojo sourcemap default.project.json --output sourcemap.json`, then run
   `luau-lsp analyze --sourcemap=sourcemap.json src`, passing the Roblox type definitions
   with `--definitions` (`luau-lsp analyze --help` lists the flags). Studio Script Sync
   projects may not have a sourcemap.

## Patterns

### 1. Server Script: react to players joining (leaderstats)

```lua
-- ServerScriptService/Leaderboard.server.luau  (a Script = runs on the server)
local Players = game:GetService("Players")

local function onPlayerAdded(player: Player)
    local stats = Instance.new("Folder")
    stats.Name = "leaderstats"          -- this name makes it show on the leaderboard

    local coins = Instance.new("IntValue")
    coins.Name = "Coins"
    coins.Value = 0
    coins.Parent = stats

    stats.Parent = player               -- parent LAST
end

Players.PlayerAdded:Connect(onPlayerAdded)
```

### 2. Create and configure an instance

```lua
local Workspace = game:GetService("Workspace")

local part = Instance.new("Part")
part.Size = Vector3.new(4, 1, 4)
part.Position = Vector3.new(0, 10, 0)
part.Anchored = true                    -- won't fall under gravity
part.BrickColor = BrickColor.new("Bright blue")
part.Parent = Workspace                 -- set Parent last so it replicates once, fully
```

### 3. Connect an event (and disconnect to avoid leaks)

```lua
local debounce = false
local connection
connection = part.Touched:Connect(function(hit: BasePart)
    local character = hit.Parent
    local humanoid = character and character:FindFirstChildOfClass("Humanoid")
    if not humanoid or debounce then return end
    debounce = true
    humanoid.Health -= 10
    task.wait(1)                        -- task.wait, NOT the deprecated wait()
    debounce = false
end)

-- Later, when the part is removed or the round ends:
-- connection:Disconnect()
```

### 4. Client → server with a RemoteEvent (validate on the server!)

```lua
-- ReplicatedStorage: create a RemoteEvent named "BuyItem" (in Studio or via code).
-- CLIENT (LocalScript): request a purchase. The client can lie — this is only a request.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local buyItem = ReplicatedStorage:WaitForChild("BuyItem")  -- wait: may not have replicated yet
buyButton.MouseButton1Click:Connect(function()
    buyItem:FireServer("sword")        -- send the item id only; never the price/result
end)
```

```lua
-- SERVER (Script): the ONLY place the transaction is decided.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local buyItem = ReplicatedStorage:WaitForChild("BuyItem")
local PRICES = { sword = 100, shield = 75 }

buyItem.OnServerEvent:Connect(function(player: Player, itemId)
    -- TRUST NOTHING from the client. Validate types and values.
    if type(itemId) ~= "string" then return end
    local price = PRICES[itemId]
    if not price then return end                         -- unknown item
    local coins = player.leaderstats.Coins
    if coins.Value < price then return end               -- can't afford
    coins.Value -= price                                 -- server applies the change
    grantItem(player, itemId)
end)
```

### 5. A per-frame loop with RunService

```lua
local RunService = game:GetService("RunService")
-- Heartbeat fires every frame AFTER physics; dt is seconds since the last step.
RunService.Heartbeat:Connect(function(dt)
    spinner.CFrame *= CFrame.Angles(0, math.rad(90) * dt, 0)  -- 90deg/sec, frame-independent
end)
```

### 6. Shared code in a ModuleScript

```lua
-- ReplicatedStorage/GameConfig (a ModuleScript) — usable by server and client.
local GameConfig = {}
GameConfig.MaxHealth = 100
function GameConfig.damageFor(weapon: string): number
    return ({ sword = 25, bow = 15 })[weapon] or 0
end
return GameConfig
```

```lua
local GameConfig = require(game:GetService("ReplicatedStorage"):WaitForChild("GameConfig"))
print(GameConfig.MaxHealth)
```

## Pitfalls

- **Trusting the client is an exploit** → clients can send any arguments to a
  `RemoteEvent`/`RemoteFunction`. Validate every argument's type and range on the
  server and keep the server authoritative over health, currency, and inventory.
- **`LocalScript` doesn't run where you put it** → LocalScripts run in
  `StarterPlayerScripts`, `StarterCharacterScripts`, `StarterGui`, or tools — not in
  `Workspace` or `ServerScriptService`. Server `Script`s belong in
  `ServerScriptService`/`Workspace`. A `Script` with `RunContext = Client` placed in a
  `Starter*` container runs twice (original and copy); keep those in `ReplicatedStorage`.
- **Deprecated globals** → use `task.wait`/`task.spawn`/`task.delay`, not the old
  `wait()`/`spawn()`/`delay()` (worse scheduling and throttling).
- **Parenting first, then setting properties** → set properties first and `Parent`
  last so the instance replicates once in its final state.
- **`nil` on the client right after join** → objects stream/replicate over time; use
  `parent:WaitForChild("Name")` instead of indexing directly on the client.
- **Connections never disconnected** → long-lived `:Connect` handlers leak and can
  fire on destroyed objects; store the connection and `:Disconnect()` (or use
  `Instance:GetAttributeChangedSignal`/`:Once` where appropriate).
- **Using a RemoteFunction where a RemoteEvent fits** → `RemoteFunction` blocks
  waiting for a return and a malicious/slow client can stall the server; prefer
  one-way `RemoteEvent`s unless you genuinely need a reply.
- **Assuming the old type checker** -> Luau's New Type Solver reached general release
  (out of Studio Beta) in Nov 2025. `nocheck`/non-strict places get it automatically;
  strict-mode places opt in with the `UseNewLuauTypeSolver` workspace property, and
  `LuauTypeCheckMode` sets a place's default checking mode. It runs only at edit time
  (no runtime cost), so triage type warnings against the solver the place actually has
  enabled, not older behavior.

## References

- For the full client/server model (replication, `RemoteFunction` vs `RemoteEvent`,
  `:WaitForChild` timing, `BindableEvent` for same-context messaging, attributes,
  `CollectionService` tags, and `:Once`/connection cleanup), read
  `references/client-server.md`.

## Related skills

- `roblox-datastores` — persist player data across sessions (server-only).
- `roblox-networking` — production remote contracts, server validation, rate limits, replication,
  streaming, prediction, and multi-client testing.
- `save-systems` — engine-agnostic persistence concepts.
- `game-ai` / `input-systems` — portable AI and input patterns to implement in Luau.


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
