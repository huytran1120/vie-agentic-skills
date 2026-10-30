---
name: gamedev-godot-export
description: >
  Export and build a Godot 4.7 project for distribution: install export templates,
  define export presets (Windows/macOS/Linux/Web/Android), run headless command-line
  exports for CI, and handle web (HTML5) COOP/COEP and dedicated-server/headless
  builds. Use when exporting a Godot game, configuring export_presets.cfg, building
  for web/desktop/mobile, or automating builds from the command line.
---

# Godot Export & Builds (4.x)

Turn a project into runnable platform builds via export presets and the command line, and
handle the web/dedicated-server gotchas. Targets **Godot 4.7**.

## When to use

- Use when producing a shippable build: installing export templates, creating/editing
  export presets, exporting from the editor or headless CLI (CI), or troubleshooting web
  (HTML5) and dedicated-server exports.

**When *not* to use:** storefront publishing flows → `steam-publish`/`itch-publish`; the
networking code of a server → `godot-multiplayer` (this skill covers building it headless).

## Core workflow

1. **Install export templates** matching your engine version: Editor menu >
   *Manage Export Templates* (download), or install the `.tpz` offline. Versions must
   match the editor exactly. Since 4.7 the downloader can fetch templates for a single
   platform or architecture instead of the full set.
2. **Add export presets** in *Project > Export*: pick a platform (Windows Desktop, macOS,
   Linux, Web, Android, iOS), set the export path, icons, features, and resource
   include/exclude filters. Presets are saved to `export_presets.cfg`.
3. **Export from the editor** with *Export Project* (release) or *Export PCK/ZIP*.
4. **Or export headless from the CLI** for automation/CI using
   `--export-release "<preset name>" <output path>`.
5. **Per platform:** Web needs cross-origin isolation (COOP/COEP) only if the preset's
   *Thread Support* is on (off by default); Android needs the SDK/keystore; macOS/iOS need
   signing for distribution.
6. **Smoke-test the build** on the target before shipping — exported builds use `res://`
   read-only; write to `user://`.

## Patterns

### 1. Headless CLI export (CI-friendly)

```bash
# Preset name must match exactly what's in Project > Export (quote it).
# Run from the project directory (where project.godot lives).
godot --headless --export-release "Windows Desktop" build/windows/game.exe
godot --headless --export-release "Linux"           build/linux/game.x86_64
godot --headless --export-release "Web"             build/web/index.html

# Debug build (includes debug symbols / remote debug):
godot --headless --export-debug "Windows Desktop" build/windows/game_debug.exe

# Export only the data pack (no executable):
godot --headless --export-pack "Linux" build/game.pck

# Export only files changed since the given base pack(s):
godot --headless --export-patch "Linux" build/patch1.pck --patches build/game.pck
```

### 2. Run a project headless (dedicated server / tests)

```bash
# No window/GPU — for a server build or automated runs.
godot --headless --path . res://server_main.tscn
# Quit after N main-loop iterations (frames, NOT seconds) — handy for a headless smoke test:
godot --headless --path . --quit-after 600
```

### 3. Detect the build context at runtime

```gdscript
func _ready() -> void:
    if OS.has_feature("dedicated_server") or DisplayServer.get_name() == "headless":
        _start_server_only()          # skip rendering/UI on a headless server
    if OS.has_feature("web"):
        _apply_web_tweaks()
    # Custom feature tags (added per preset) are also queryable:
    # if OS.has_feature("demo"): limit_content()
```

### 4. Choose write paths that survive export

```gdscript
# res:// is READ-ONLY in exported games. Always write to user://.
func save_path() -> String:
    return "user://savegame.tres"     # resolves to the OS app-data dir

func _ready() -> void:
    print(OS.get_user_data_dir())     # where user:// actually lives
```

## Pitfalls

- **"No export template found".** Templates must match the exact editor version (incl.
  beta/rc). Re-download via *Manage Export Templates* after upgrading Godot.
- **Preset name mismatch in CLI.** `--export-release "Windows"` fails if the preset is
  named `"Windows Desktop"`. Names are case- and space-sensitive; quote them.
- **Web build shows a blank page / threads error.** Builds with the preset's *Thread
  Support* option enabled require the server to send
  `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` (cross-origin isolation for
  `SharedArrayBuffer`). Must be served over HTTP(S), not opened as a `file://`. itch.io has
  a "SharedArrayBuffer support" toggle for this. If the host cannot set headers (GitHub
  Pages), leave *Thread Support* off — the default since 4.3.
- **Writing to `res://` at runtime fails** in exports (read-only, packed). Use `user://`.
- **Missing resources in the build.** Non-resource files (e.g. external `.json`, `.txt`)
  are not auto-included — add them via the preset's *Resources > Filters to export
  non-resource files* (e.g. `*.json`).
- **Android export needs setup**: Android SDK/JDK paths in Editor Settings, a debug or
  release **keystore**, and the `INTERNET` permission for networked games.
- **macOS/iOS distribution requires signing/notarization**; unsigned macOS apps are
  blocked by Gatekeeper.
- **Debug vs release.** `--export-debug` enables remote debugging and debug checks; ship
  `--export-release`.

## References

- For the `export_presets.cfg` structure, all useful CLI flags, custom feature tags,
  PCK/expansion patching, encryption, and per-platform setup (Android keystore, macOS
  signing, web headers), read `references/presets-and-cli.md`.

## Related skills

- `godot-multiplayer` — the dedicated-server code you export headless.
- `steam-publish` / `itch-publish` — getting the build to players.
- `prototype-fast` / `game-jam` — quick web/desktop builds for sharing.


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
