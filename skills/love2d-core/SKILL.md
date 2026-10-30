---
name: love2d-core
description: >
  Structure and debug a LÖVE (Love2D) game in Lua: the love.load/update/draw loop,
  delta-time movement, input, and screen states. Use when building a LÖVE 11.x game
  (main.lua, conf.lua, .love).
---

# LÖVE (Love2D) Core

Set up and debug the foundation of a LÖVE game in Lua: the callback loop, frame-rate-
independent movement, input, and screen states. Targets **LÖVE 11.5**.

## When to use

- Use when starting a LÖVE game, wiring up `main.lua`/`conf.lua`, or fixing the core loop,
  movement that runs at the wrong speed, input handling, or screen switching.
- Use when the workspace has `main.lua` calling `love.*`, a `conf.lua`, or a `.love` file.

**When *not* to use:** Lua *language* questions unrelated to LÖVE; physics bodies/joints
(LÖVE uses Box2D via `love.physics` — a separate concern); shader code (`love.graphics`
GLSL is its own topic). For cross-engine save/load patterns, use `save-systems`.

## Core workflow

1. **Confirm the entry points.** A LÖVE game runs `main.lua`; it should define
   `love.load()` (one-time setup), `love.update(dt)` (state), and `love.draw()` (rendering).
   Window/version setup goes in `conf.lua` (run *before* modules load).
2. **Pin the version.** Set `t.version = "11.5"` in `conf.lua` so LÖVE warns on mismatch.
3. **Drive all motion by `dt`** (delta time, in seconds) so speed is frame-rate independent.
4. **Handle input** two ways: polled (`love.keyboard.isDown` in `update`, for held keys) and
   event (`love.keypressed` callback, for discrete presses).
5. **Manage screens** (menu, game, pause) with a small state stack rather than a pile of
   `if` flags — see Patterns and `references/state-stack.md`.
6. **Run and observe.** Launch with `love .` from the project folder; verify the window,
   motion speed, and input on screen before assuming it works.

## Patterns

### 1. `main.lua` skeleton (the callback loop + input)

```lua
-- main.lua — LÖVE calls these callbacks for you. Colors are 0–1 in LÖVE 11.x.
function love.load()
    -- One-time setup. speed is in PIXELS PER SECOND, not per frame.
    player = { x = 100, y = 100, size = 40, speed = 220 }
    love.graphics.setBackgroundColor(0.1, 0.1, 0.12)
end

function love.update(dt)
    -- Polled input: good for continuous movement while a key is held.
    if love.keyboard.isDown("right") then player.x = player.x + player.speed * dt end
    if love.keyboard.isDown("left")  then player.x = player.x - player.speed * dt end
    if love.keyboard.isDown("down")  then player.y = player.y + player.speed * dt end
    if love.keyboard.isDown("up")    then player.y = player.y - player.speed * dt end
end

function love.draw()
    love.graphics.setColor(0.2, 0.8, 1.0)                 -- tint ON
    love.graphics.rectangle("fill", player.x, player.y, player.size, player.size)
    love.graphics.setColor(1, 1, 1)                       -- reset tint before text/images
    love.graphics.print("Arrow keys to move, Esc to quit", 10, 10)
end

function love.keypressed(key)
    -- Event input: fires once per physical press. Use for menus, jumps, toggles.
    if key == "escape" then love.event.quit() end
end
```

### 2. Frame-rate independence (the single most common bug)

```lua
-- RIGHT: scaled by dt → same real-world speed at 30 or 240 FPS.
player.x = player.x + player.speed * dt
-- WRONG: "pixels per frame" → moves twice as fast at double the frame rate.
player.x = player.x + player.speed
```

### 3. `conf.lua` (window + version; runs before `main.lua`)

```lua
-- conf.lua — must be its own file; love.conf will NOT run from main.lua.
function love.conf(t)
    t.version = "11.5"             -- the LÖVE version this game targets (string "X.Y")
    t.window.title  = "My LÖVE Game"
    t.window.width  = 800
    t.window.height = 600
    t.window.vsync  = 1            -- number since 11.0: 1 = on, 0 = off, -1 = adaptive
    t.window.resizable = false
    t.modules.physics = false      -- disable modules you don't use to trim startup/memory
end
```

### 4. Color is 0–1 in LÖVE 11.x (not 0–255)

```lua
-- LÖVE 11.x uses normalized floats. (Pre-11.0 code used 0–255 and will look wrong.)
love.graphics.setColor(1, 0, 0)                          -- opaque red
love.graphics.setColor(0.2, 0.8, 1.0, 0.5)               -- translucent cyan (alpha 0.5)
-- Need to convert old byte values? Use the helper instead of dividing by hand:
love.graphics.setColor(love.math.colorFromBytes(128, 234, 255))
```

### 5. Screen states (brief — full manager in references)

```lua
-- A screen is a table with optional :update(dt), :draw(), :keypressed(key).
-- Keep the active screen on a stack so pause/menu overlays are trivial to pop.
local Stack = require("state_stack")   -- see references/state-stack.md for the module

-- Call a method on the top screen only if it defines it (a menu may have no update).
local function forward(name, ...)
    local screen = Stack.current()
    if screen and screen[name] then screen[name](screen, ...) end
end

function love.load()          Stack.push(require("screens.menu")) end
function love.update(dt)      forward("update", dt) end
function love.draw()          forward("draw") end
function love.keypressed(key) forward("keypressed", key) end
```

## Pitfalls

- **Speed varies with FPS** → you forgot `* dt`. Every per-frame change to position, timers,
  or animation must be scaled by `dt`.
- **`love.conf` placed in `main.lua`** → it silently does nothing. It must live in `conf.lua`,
  which LÖVE runs *before* loading modules.
- **Colors washed out or invisible** → you used 0–255 values. 11.x does not rescale them;
  every channel above 1 draws at full intensity, so `setColor(128, 234, 255)` comes out
  plain white and an alpha of `128` is fully opaque. Use 0–1 floats or
  `love.math.colorFromBytes` (11.3+).
- **Everything tinted after one `setColor`** → color is global and persists across draws.
  Reset with `love.graphics.setColor(1, 1, 1)` before drawing text/images you want untinted.
- **Holding a key fires `love.keypressed` only once** → key repeat is off by default.
  Call `love.keyboard.setKeyRepeat(true)` (e.g. for text fields or menu scrolling); the
  repeats then arrive with the third argument `isrepeat` set, so a jump handler can
  ignore them. Releases go to `love.keyreleased(key)`.

## References

- For a complete push/pop screen-state manager (menu → game → pause, with delegated
  callbacks), read `references/state-stack.md`.

## Related skills

- `save-systems` — saving/loading game state (engine-agnostic).
- `input-systems` — rebindable, multi-device input architecture.
- `pygame-core` / `phaser-core` — the same loop concepts in other lightweight engines.


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
