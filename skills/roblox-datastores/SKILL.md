---
name: roblox-datastores
description: >
  Persist player data in Roblox with DataStoreService: GetDataStore, GetAsync/
  SetAsync/UpdateAsync/IncrementAsync wrapped in pcall, load-on-join and
  save-on-leave plus BindToClose, retries, and OrderedDataStore leaderboards. Use
  when saving or loading persistent data in a Roblox experience — when the user
  mentions DataStore, DataStoreService, GetAsync, SetAsync, UpdateAsync, save player
  data, or leaderboards. For general Luau scripting use roblox-luau.
---

# Roblox DataStores

Persist data across sessions in Roblox with `DataStoreService`: loading on join,
saving on leave and shutdown, safe updates, retries, and ordered stores for
leaderboards. Server-side only.

## When to use

- Use to save/load player progress (coins, inventory, levels), build persistent
  leaderboards, or fix data loss, overwrites, and throttling.
- Use when server code calls `DataStoreService`, `GetDataStore`, `GetAsync`,
  `SetAsync`, `UpdateAsync`, or `GetOrderedDataStore`.

**When *not* to use:** general scripting, services, remotes, the client/server
split → `roblox-luau`. High-frequency temporary state (matchmaking, per-round) →
memory stores (a different service). Engine-agnostic persistence theory →
`save-systems`.

## Core workflow

1. **Enable Studio access once.** In a published place, File → Experience Settings →
   Security → *Enable Studio Access to API Services* (use a separate test place; Studio
   hits the same live data as players). DataStores work only from server `Script`s,
   never `LocalScript`s.
2. **Get a store, then read/write by key.** `DataStoreService:GetDataStore("Name")`;
   key per player is usually `"Player_" .. player.UserId`.
3. **Wrap every call in `pcall`.** `GetAsync`/`SetAsync`/`UpdateAsync` are network
   calls that can fail; an unguarded failure errors the thread and risks data loss.
4. **Load on `PlayerAdded`, save on `PlayerRemoving`, and also `BindToClose`.** A
   leaving player and a shutting-down server both need a final save.
5. **Prefer `UpdateAsync` for read-modify-write** (multi-server safe) over `SetAsync`
   (blind overwrite). On a failed load, do **not** overwrite with defaults — abort
   the save so you don't wipe good data.
6. **Use `OrderedDataStore` for ranked data** (leaderboards) via `GetSortedAsync`.
   Test by joining, changing data, rejoining, and confirming it persisted.

## Patterns

### 1. Load on join (pcall-guarded)

```lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local store = DataStoreService:GetDataStore("PlayerData")

local DEFAULT = { Coins = 0, Level = 1 }

Players.PlayerAdded:Connect(function(player)
    local key = "Player_" .. player.UserId
    local ok, data = pcall(function()
        return store:GetAsync(key)
    end)

    if not ok then
        -- Load FAILED (network). Do not treat as a new player; flag so we never save
        -- over their real data with defaults.
        warn("Load failed for", player.Name, data)
        player:SetAttribute("DataLoaded", false)
        return
    end

    player:SetAttribute("DataLoaded", true)
    local profile = data or DEFAULT          -- nil == genuinely new player
    applyToLeaderstats(player, profile)
end)
```

### 2. Save with UpdateAsync (multi-server safe)

```lua
-- UpdateAsync reads the latest value, then writes what the callback returns.
-- The callback MUST NOT yield (no task.wait, no further Async calls inside it), and it
-- can run more than once if another server writes the key first, so keep it pure.
local function savePlayer(player)
    -- Save only after a confirmed load. `~= true` also covers a player who leaves while
    -- GetAsync is still in flight (attribute still nil), which `== false` would miss.
    if player:GetAttribute("DataLoaded") ~= true then return end
    local key = "Player_" .. player.UserId
    local newData = gatherDataFor(player)    -- a plain table of serializable values

    local ok, err = pcall(function()
        store:UpdateAsync(key, function(old)
            -- merge/decide here; return nil to cancel the write
            return newData
        end)
    end)
    if not ok then warn("Save failed for", player.Name, err) end
end
```

### 3. Save on leave AND on shutdown

```lua
Players.PlayerRemoving:Connect(savePlayer)

-- BindToClose runs when the server shuts down; save everyone still in.
-- The server waits at most 30 seconds for it, so save in parallel and yield until done.
game:BindToClose(function()
    local players = Players:GetPlayers()
    local remaining = #players
    if remaining == 0 then return end
    for _, player in players do
        task.spawn(function()
            savePlayer(player)
            remaining -= 1
        end)
    end
    while remaining > 0 do task.wait() end
end)
```

### 4. Retry with backoff (transient failures)

```lua
local function withRetry(fn, attempts)
    attempts = attempts or 3
    for i = 1, attempts do
        local ok, result = pcall(fn)
        if ok then return true, result end
        if i < attempts then task.wait(2 ^ i) end   -- 2s, 4s, ... backoff
    end
    return false
end

local ok, data = withRetry(function() return store:GetAsync(key) end)
```

Retry only operations that are safe to repeat. A failed write is not proof the write did
not happen: the server may simply have missed the response. Re-running an `UpdateAsync`
that writes the full saved state is harmless; re-running `IncrementAsync` can add twice.
When the outcome matters, confirm it with an uncached read (`DataStoreGetOptions` with
`UseCache = false`) before retrying.

### 5. Increment a counter

```lua
-- IncrementAsync is a convenience for integer read-modify-write (still wrap it).
local ok, newTotal = pcall(function()
    return store:IncrementAsync("Visits_" .. player.UserId, 1)
end)
```

### 6. Leaderboard with OrderedDataStore

```lua
local boards = DataStoreService:GetOrderedDataStore("Coins")

-- Write a player's score (call when it changes, not every frame).
pcall(function() boards:SetAsync("Player_" .. player.UserId, coins) end)

-- Read the top 10, descending.
local ok, pages = pcall(function()
    return boards:GetSortedAsync(false, 10)   -- ascending=false → highest first
end)
if ok then
    for rank, entry in ipairs(pages:GetCurrentPage()) do
        print(rank, entry.key, entry.value)   -- entry.value is the number
    end
end
```

## Pitfalls

- **Unhandled failure wipes progress** → always `pcall` Async calls; on a failed
  *load*, mark the session and refuse to *save* so defaults never overwrite real data.
- **`SetAsync` race between servers** → two servers writing the same key can clobber
  each other. Use `UpdateAsync` for read-modify-write so each write sees the latest.
- **Yielding inside the `UpdateAsync` callback** → the callback can't call
  `task.wait` or other Async functions; compute the new value beforehand and return it.
- **Side effects inside the `UpdateAsync` callback** → Roblox re-runs the callback when
  another server changed the key between read and write, so granting items, firing
  remotes, or incrementing counters there can happen twice. Act after the call returns.
- **Saving a player who left mid-load** → `PlayerRemoving` can fire while `GetAsync` is
  still yielding. Gate saves on "load succeeded", not on "load did not fail".
- **No `BindToClose` save** → players in the server at shutdown lose unsaved progress;
  add `game:BindToClose` and wait for saves to finish within its budget.
- **Throttling / "too many requests"** → respect per-key and per-minute limits; don't
  save on every value change. Batch and save on a timer / on leave. `GetAsync` is
  cached for about four seconds, so immediate re-reads may be stale. Studio Run mode
  uses its own lower static limits; Roblox recommends testing rate limits in Team Create.
- **Storing non-serializable values** → only JSON-serializable data persists: numbers,
  strings, booleans, and tables with string/number keys. `Instance`s, `Vector3`,
  `CFrame`, and functions do not — serialize them to plain tables first.
- **Testing without API access** → DataStore requests in Studio error (writes report
  `StudioAccessToApisNotAllowed`) until *Enable Studio Access to API Services* is on (and
  they don't work from a `LocalScript`).
- **`DataStoreKeyInfo` is nil for ordered stores** → `OrderedDataStore` doesn't
  support versioning/metadata; use a regular `DataStore` when you need those.

## References

- For session locking (preventing duplicate data across servers), versioning/
  metadata with `DataStoreSetOptions`, ordered-store pagination
  (`AdvanceToNextPageAsync`), the key error codes and request limits, and
  Right-to-be-Forgotten compliance, read `references/sessions-and-limits.md`.

## Related skills

- `roblox-luau` — services, instances, events, and the server/client model.
- `save-systems` — engine-agnostic serialization, slots, and migration.


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
