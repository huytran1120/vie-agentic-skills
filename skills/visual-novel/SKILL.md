---
name: visual-novel
description: >
  Build a visual novel: a branching script, character and background display, a text box with choices,
  save/load, backlog, and skip/auto. Use for a VN, dating sim, or branching story game.
---

# Visual Novel

A playbook for visual novels — the branching script, the presentation (text box, characters,
backgrounds), choices, and the quality-of-life systems players expect (save anywhere, backlog,
skip, auto). This is a **compositional** skill: it drives a dialogue engine and a UI layer. It
does not re-teach the dialogue engine or UI nodes; it defines the script model and the player
conveniences that make a VN pleasant to read.

## When to use

- Use when the game is **mostly reading branching text** with character art and backgrounds:
  visual novel, dating sim, branching interactive fiction, story-choice game.
- Use when designing a choice/route structure, story flags, or VN conveniences (backlog,
  skip, auto-advance, save-anywhere).

**When *not* to use:** dialogue as one feature inside a larger game → `rpg` consuming
`dialogue-systems`. Card/board play → other genres. For the branching-script engine itself,
use `dialogue-systems` (Ink / Yarn Spinner).

**If the project is Ren'Py** (current stable 8.5.3): the engine already ships save-anywhere,
rollback, a history (backlog) screen, skip that stops at unseen text by default
(`preferences.skip_unseen = False`), auto-forward and a text-speed preference. Use and restyle
those through its screens and preferences; apply this skill's design guidance (routes, flags,
reactivity) rather than rebuilding the systems in Patterns 2–3.

## Core loop

**Read a line → advance → (at a branch) make a choice → the story branches on flags/choices →
read on → reach an ending.** The "game" is the *shape of the branching* and whether choices
feel consequential; everything else is presentation and convenience.

## Must-have systems

1. **Branching script** — ordered lines + choices + jumps, with conditions and variables (Ink/Yarn).
2. **Text box** — speaker name, body text, typewriter reveal, advance on click/key.
3. **Characters** — sprites with expressions/poses, positions, show/hide transitions.
4. **Backgrounds + transitions** — scene images, fades/dissolves.
5. **Choices** — present options, gate some on flags, record the pick.
6. **Story state** — flags/variables that branch the script and unlock content.
7. **Save/load (save-anywhere)** — full script position + state; multiple slots; quick save.
8. **VN conveniences** — backlog/history, skip (read text), auto-advance, text-speed setting.
9. **Audio** — music per scene, SFX, optional voice clips.

## Design knobs

| Knob | Effect | Notes |
|------|--------|-------|
| Text speed / instant | reading comfort | Always allow instant + a skip. |
| Auto-advance delay | hands-free reading | Tunable; pause on choices. |
| Skip scope | re-reading | Skip *read* text only by default. |
| Branch breadth/depth | replay value vs. cost | Branches multiply writing/art work. |
| Flag-gated content | reactivity | Lines/choices that check past decisions. |
| Route structure | story shape | Branch-and-merge vs. distinct routes (refs). |
| Choice visibility | fairness | Show locked choices vs. hide them. |
| Backlog length | convenience | Keep enough to re-read recent context. |

## Patterns

### 1. Script as data the engine walks

```python
# Pseudocode. Lines, choices, and jumps as data — usually authored in Ink/Yarn and stepped
# through by that runtime. The engine asks the script for "the next thing to show".
node = script.current()
if node.kind == "line":
    show_text(node.speaker, node.text)        # wait for advance input
elif node.kind == "choice":
    options = [o for o in node.options if condition_met(o.condition, flags)]  # gate by flags
    show_choices(options)                      # wait for selection
elif node.kind == "set":
    flags[node.var] = eval_expr(node.expr, flags)
script.advance(selected_option_or_none)
```

### 2. Typewriter reveal + advance (skippable)

```python
# Pseudocode. Lay out the whole line once, then reveal it; a press first completes the line.
def show_text(speaker, text):
    name_label.text = speaker
    body_label.text = text                     # full text set up front: wrapping is decided now
    shown = 0.0
    while shown < visible_length(body_label):  # count displayed characters, not markup tags
        if advance_pressed():                   # first press: reveal the whole line instantly
            break
        shown += chars_per_second * frame_dt()
        body_label.visible_characters = int(shown)
        wait_one_frame()
    show_all_characters(body_label)
    backlog.append((speaker, text))             # once, when the line is complete
    wait_for_advance()                          # second press: go to the next line
```

Reveal with the label's visible-character count, not by slicing the string: slicing cuts
markup tags in half and re-wraps the text every frame, so a word starts on one line and jumps
to the next. Godot 4.7: `RichTextLabel.visible_characters` (or `visible_ratio`) with
`visible_characters_behavior = TextServer.VC_CHARS_AFTER_SHAPING`; the default
`VC_CHARS_BEFORE_SHAPING` leaves hidden text out of line breaking, so words still jump. Unity 6.3:
`TMP_Text.maxVisibleCharacters` (TextMeshPro, part of the uGUI package).

### 3. Choice sets a flag that branches later content

```python
# Pseudocode. Choices write flags; later conditions read them — that is "reactivity".
def on_choice(option):
    if option.set: flags[option.set] = True     # e.g. flags["helped_npc"] = True
    script.jump(option.target)                   # follow the branch

# Elsewhere, a line/choice/ending checks the flag:
if flags.get("helped_npc"): play_route("good_ending") else: play_route("neutral_ending")
```

## Pitfalls / failure modes

- **Save that only stores a checkpoint** → VNs need **save-anywhere**. Persist the exact script
  position *and* all flags/variables (and seen-text data) so a load resumes the same line. Check
  what your runtime can restore: Ink saves the exact position, Yarn Spinner only the node
  (refs §4).
- **Typewriter text that jumps between lines or shows raw tags** → the reveal slices the string.
  Set the full text and raise the visible-character count (Pattern 2).
- **Presentation logic baked into the script** → unmaintainable. Keep *content* (text, choices)
  in the script and *how it looks* (sprites, transitions) in the engine layer.
- **No skip/auto/backlog** → readers feel trapped, especially on replays. These are expected
  baseline features, not extras.
- **Skipping unread text** → players miss content. Skip should fast-forward **read** text only.
- **Choices with no consequence** → branches that reconverge instantly feel fake. Set flags that
  visibly change later lines, choices, or endings.
- **Combinatorial branch explosion** → unshippable. Prefer branch-and-merge with a few flagged
  variations over fully distinct trees (refs).
- **Lost reading context** → no backlog to re-read the last lines. Keep a history buffer.
- **Hardcoded language** → no localization path. Keep text in data keyed for translation.

## Composition (build it from these skills)

- **Script engine:** `dialogue-systems` (Ink / Yarn Spinner) — branching, conditions, variables, localization hooks.
- **Presentation:** `game-ui-ux` for text-box/choice-menu layout, scaling, and safe areas; `godot-ui-control` for the concrete text box, choice menu, name plate, and backlog UI.
- **Persistence:** `save-systems` for save-anywhere slots, seen-text/skip data, and settings.
- **Audio:** `audio-design` for per-scene music, SFX, and voice playback.
- **Visuals:** the engine animation/`Tween` skill for sprite/background transitions; `shader-programming` for dissolves.
- **Process:** `prototype-fast` to test the branch structure in plain text before adding art.

## References

- For the branching data model, route structures (branch-and-merge vs. routes), flags/variables,
  save-anywhere + backlog/skip data, and the content/presentation split, read
  `references/script-and-flow.md`.


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
