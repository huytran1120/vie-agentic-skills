---
name: godot-audio
description: >
  Play and mix audio in Godot 4.7: AudioStreamPlayer (2D/3D variants), audio buses
  with volume/mute and effects, music vs SFX routing, db/linear volume, and precise
  sync-to-beat playback timing. Use when playing sounds or music in a Godot project,
  routing AudioStreamPlayer nodes to buses, adjusting bus volume via AudioServer, or
  syncing gameplay to the beat.
---

# Godot Audio (4.x)

Play SFX and music, route them through buses, control volume in decibels, and time
gameplay to the beat. Targets **Godot 4.7**.

## When to use

- Use when playing sound effects or music, routing audio to buses (Master/Music/SFX),
  adjusting volume/mute from code, adding bus effects (reverb, compressor), positional 3D
  audio, or syncing events to music.

**When *not* to use:** engine-agnostic audio *design* (adaptive music structure, mixing
philosophy, ducking patterns) → `audio-design`; importing/encoding assets outside Godot.

## Core workflow

1. **Pick the player node:**
   - `AudioStreamPlayer` — non-positional (music, UI, global SFX).
   - `AudioStreamPlayer2D` / `AudioStreamPlayer3D` — positional; volume/pan from distance.
2. **Assign an `AudioStream`** to `stream` (`.ogg` for music/loops, `.wav` for short SFX)
   and `play()`. Set `autoplay` for music that starts with the scene.
3. **Route to a bus.** Set the player's `bus` to a named bus (e.g. `"Music"`, `"SFX"`).
   Define buses in the Audio panel (bottom dock); each can have volume, mute, solo, and
   effects.
4. **Control volume in dB**, not linear (audio is logarithmic). `0 dB` = unchanged,
   `-80 dB` ≈ silent. Convert with `linear_to_db`/`db_to_linear`, or use the linear helpers
   (`volume_linear` on players, `AudioServer.set_bus_volume_linear()`), which convert for you.
5. **Drive volume/mute from code** with `AudioServer` by bus index.
6. **For rhythm**, compute precise playback time using output latency compensation.

## Patterns

### 1. One-shot SFX (fire-and-forget)

```gdscript
@onready var sfx: AudioStreamPlayer = $Sfx   # stream assigned in the editor

func play_jump() -> void:
    sfx.pitch_scale = randf_range(0.95, 1.05)   # slight variation avoids fatigue
    sfx.play()

# For overlapping copies, raise sfx.max_polyphony (default 1), use an
# AudioStreamPolyphonic stream, or spawn short-lived players and free on `finished`.
```

### 2. Set a bus's volume and mute via AudioServer

```gdscript
func set_music_volume(linear_0_to_1: float) -> void:
    var bus := AudioServer.get_bus_index("Music")
    # Convert a 0..1 slider to decibels; clamp avoids -inf at 0.
    AudioServer.set_bus_volume_db(bus, linear_to_db(maxf(linear_0_to_1, 0.0001)))

func toggle_sfx(muted: bool) -> void:
    AudioServer.set_bus_mute(AudioServer.get_bus_index("SFX"), muted)
```

### 3. Crossfade between two music tracks

```gdscript
@onready var a: AudioStreamPlayer = $MusicA
@onready var b: AudioStreamPlayer = $MusicB

func crossfade_to(stream: AudioStream, secs := 1.5) -> void:
    b.stream = stream
    b.volume_db = -40.0
    b.play()
    var tw := create_tween().set_parallel(true)
    tw.tween_property(a, "volume_db", -40.0, secs)   # fade out current
    tw.tween_property(b, "volume_db", 0.0, secs)     # fade in next
    tw.chain().tween_callback(a.stop)
    var tmp := a; a = b; b = tmp                      # swap roles
```

### 4. Beat-accurate timing (compensate for output latency)

```gdscript
@onready var music: AudioStreamPlayer = $Music

func get_playback_time() -> float:
    # Add time since the last audio mix, subtract output latency, for sub-frame accuracy.
    var t := music.get_playback_position() + AudioServer.get_time_since_last_mix()
    return t - AudioServer.get_output_latency()
```

## Pitfalls

- **Treating volume as linear.** `volume_db`/`set_bus_volume_db` are decibels. Setting
  `volume_db = 0.5` is nearly full volume, not half. Map sliders with `linear_to_db`.
- **`linear_to_db(0.0)` is `-inf`.** It is silent, but tweening or doing math from `-inf`
  produces NaN. Clamp the linear value to a small minimum (e.g. `0.0001`) before converting,
  or special-case 0 → mute. `set_bus_volume_linear(bus, 0.0)` stores `-inf` too.
- **Bus name typos fail quietly.** `get_bus_index("Muisc")` returns `-1`; calls then error
  or no-op. Match the exact bus name from the Audio panel.
- **Short SFX cut off** when the same player is retriggered → `max_polyphony` defaults to 1.
  Raise it (e.g. 4) so `play()` overlaps copies, or use an `AudioStreamPolyphonic` /
  separate players freed on `finished`.
- **Music doesn't loop** unless the import/stream loop is enabled (`.ogg` import has a
  Loop option; `AudioStreamWAV` has `loop_mode`).
- **Syncing to `get_playback_position()` alone is jittery** — it updates per audio mix,
  not per frame; add `get_time_since_last_mix()` and subtract `get_output_latency()`.
- **3D audio inaudible** → no `AudioListener3D`/`Camera3D` to hear it, or `max_distance`/
  attenuation too tight, or wrong bus muted.

## References

- For the bus layout (`.tres`), adding effects (reverb/compressor/EQ) and side-chain
  ducking, `AudioStreamPolyphonic`/`AudioStreamInteractive`, microphone capture, and
  procedural audio with `AudioStreamGenerator`, read `references/buses-and-effects.md`.

## Related skills

- `audio-design` — engine-agnostic adaptive music, mixing, and ducking practice.
- `godot-animation` — syncing animation/Tween to `get_playback_position()`.
- `godot-ui-control` — volume sliders wired to `AudioServer`.


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
