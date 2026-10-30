---
name: unreal-packaging
description: >
  Package and ship an Unreal Engine 5 project: the Platforms menu Package Project flow, build
  configurations (Development vs Shipping), cooking content, packaging settings and the Game
  Default Map, and command-line builds with RunUAT BuildCookRun. Use when packaging a build,
  making a shipping build, cooking content, configuring packaging settings, or when the user
  mentions package Unreal, cook content, shipping build, or BuildCookRun.
---

# Unreal Packaging & Cooking

Turn a UE5 project into a runnable, distributable build: choose the right build configuration,
cook content, set the launch map, and package — from the editor or the command line. Targets
**UE 5.8**.

## When to use

- Use when producing a build (test or release), choosing Development vs Shipping, cooking
  content, configuring Packaging / Maps & Modes settings, or automating builds with
  `RunUAT BuildCookRun` for CI.
- Use when the project has a `*.uproject` and `Config/Default*.ini`, and the goal is a packaged
  player rather than running in-editor.

**When *not* to use:** storefront submission/release process → `steam-publish` / `itch-publish`.
Editor-time gameplay/iteration is not packaging.

## Core workflow

1. **Set the launch map.** Project Settings → **Maps & Modes** → **Game Default Map** is what a
   packaged build loads first. Wrong/empty here is the most common "packaged game is black"
   cause.
2. **Pick the build configuration:** **Development** (default; optimized but keeps logging/
   stats/console for testing) vs **Shipping** (all optimizations, debugging tools stripped — for
   release). `DebugGame`/`Debug` are for debugging engine/game code and aren't for distribution;
   `DebugGame` isn't available for Blueprint-only projects.
3. **Understand cook vs package.** **Cooking** converts assets to the target platform's format.
   **Staging/packaging** copies the compiled executable + cooked content into a standalone,
   distributable folder, with content in container files (`.pak`, plus `.utoc`/`.ucas` when
   **Use Io Store** is on, which is the default). Packaging runs a cook as part of it.
4. **Package from the editor:** the **Platforms** menu → choose the platform (e.g. Windows) →
   set the Binary Configuration → **Package Project** → pick an output folder.
5. **Or build from the command line** with the Unreal Automation Tool (`RunUAT BuildCookRun`)
   for repeatable/CI builds. The **Project Launcher** (Platforms → Project Launcher) saves the
   same build/cook/stage/deploy choices as reusable launch profiles.
6. **Tune Packaging settings** (Project Settings → **Packaging**): which maps/directories to
   cook, full-rebuild, compression, and whether to build all maps.
7. **Validate assets before packaging when UnrealEditor-Cmd is available.** Run
   `UnrealEditor-Cmd <Project>.uproject -run=DataValidation` (`UnrealEditor-Cmd.exe` on
   Windows) and fix every reported validation error before cooking.
8. **Verify** by *running the packaged build*, not just by a successful cook — launch the
   executable and confirm it loads the right map and runs.

## Patterns

### 1. Editor packaging (the menu path)

```text
Platforms (toolbar)
  -> Windows
     -> Binary Configuration -> Development | Shipping
     -> Content Management -> Package Project
  -> choose/confirm the staging output folder
```

### 2. Command-line build with UAT (CI-friendly)

```bash
# Cook + build + stage + pak + archive a Shipping Windows build.
RunUAT BuildCookRun \
  -project="C:/Path/MyGame.uproject" \
  -noP4 -platform=Win64 -clientconfig=Shipping \
  -cook -allmaps -build -stage -pak -archive \
  -archivedirectory="C:/Builds/MyGame"
```

`RunUAT` lives in `Engine/Build/BatchFiles/` (`RunUAT.bat` on Windows, `RunUAT.sh` on
macOS/Linux). Drop `-allmaps` and pass `-map=Map1+Map2` to cook a subset. UE 5.8 adds
experimental Windows on Arm game builds: `-clientarchitecture=arm64` (or `arm64+x64` for both
executables side by side); the editor itself is not supported on Arm64 in 5.8.

### 3. Cook only (no packaging), e.g. to refresh content

```bash
RunUAT BuildCookRun -project="C:/Path/MyGame.uproject" -noP4 \
  -platform=Win64 -clientconfig=Development -cook -skipstage
```

## Pitfalls

- **Packaged build loads a black/empty level** — Game Default Map isn't set (or that map wasn't
  cooked). Set it in Maps & Modes and ensure it's included in the cook.
- **Shipping a Development build** — Development keeps logging/console/stats and is slower; ship
  **Shipping**. Conversely, Shipping strips `UE_LOG`/console, so debugging a Shipping-only issue
  needs Development or `Test`. A Shipping build has no console `quit`, so the game needs its own
  exit option.
- **A referenced map/asset is missing at runtime** — it wasn't cooked. Add it to the Packaging
  settings' maps/directories to cook, or cook all maps.
- **Build fails on the platform** — the platform SDK/toolchain isn't installed or is too old.
  For UE 5.8 on Windows that means Visual Studio 2022 17.14+ (2026 recommended), MSVC 14.38+
  and Windows SDK 10.0.22621.0+; macOS needs Xcode 15.2+. Check the release notes' Platform SDK
  table for other targets. Console packaging also requires a source build of the engine, not
  the Launcher build.
- **`Saved/Cooked/<Platform>` has no `.uasset`/`.uexp` files** — in UE 5.8 Zen Server is the
  cooked output store by default (unless the project turned it off in Packaging settings). The
  folder only holds a small `ue.projectstore` marker and the data lives in the Zen data
  directory. Staging still writes `.pak`/`.utoc`/`.ucas` to the staging folder; ship that
  folder, not `Saved/Cooked`. For team and CI machines Epic recommends
  `LimitProcessLifetime=false` under `[Zen.AutoLaunch]` in `DefaultEngine.ini` so `zenserver`
  is not started and stopped on every step; make sure your build automation tolerates that
  long-running process.
- **Expecting Blueprint Nativization** — it was **removed in UE5**; don't rely on it for
  performance. Profile and move hot logic to C++ (`unreal-cpp-gameplay`) instead.
- **First cook is very slow** — shaders and all assets cook from scratch; subsequent cooks are
  incremental. Don't mistake a slow first cook for a hang.

## References

- Primary docs: "Packaging Your Project"
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project`), the
  Build Configurations / `BuildCookRun` references, "Zenserver as Cooked Output Store"
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/using-zen-storage-server-as-cooked-output-store-for-unreal-engine`)
  and the Platform SDK table in the UE 5.8 release notes
  (`https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes`).

## Related skills

- `steam-publish` / `itch-publish` — distributing the packaged build to a storefront.
- `unreal-cpp-gameplay` — moving hot logic to C++ now that BP nativization is gone.


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
