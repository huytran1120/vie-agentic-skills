---
name: dialogue-systems
description: >
  Build branching dialogue and narrative — a node/choice graph with conditions,
  variables, and localization hooks — and choose between authoring tools Ink and
  Yarn Spinner or a custom data-driven runner. Engine-neutral. Use when the user
  mentions dialogue system, branching dialogue, conversation tree, choices,
  Ink (.ink), Yarn Spinner (.yarn), or NPC dialogue.
---

# Dialogue systems

Model conversations as a **graph**: nodes hold lines, choices branch the flow,
conditions gate options, and variables remember what the player did. The first
real decision is *build vs. buy* — adopt a proven authoring tool (**Ink** or
**Yarn Spinner**) or write a small data-driven runner. This skill owns both Ink
and Yarn; the `visual-novel` and `rpg` genres consume it.

## When to use

- Use to design branching conversations, choice menus, or narrative state
  (flags, relationship values) that affect later dialogue.
- Use to decide between Ink, Yarn Spinner, and a custom JSON/resource format.
- Use to wire a dialogue script into your game loop (advance line, present
  choices, run commands, resolve variables).

**When *not* to use:** for engine UI (text boxes, portraits, choice buttons), use
`godot-ui-control` or the engine's UI skill. For persisting narrative variables
across sessions, use `save-systems`. For data-as-resources in Godot/Unity, see
`godot-resources` / `unity-scriptableobjects`.

## Core workflow

1. **Choose the authoring approach.**
   - **Ink** — prose-first, writer-friendly, weave/gather flow; great for
     dialogue-heavy or CYOA narrative. Integrate via ink runtime / inkle plugins.
   - **Yarn Spinner** — node-based, explicit `<<commands>>`, strong for
     game-driven dialogue with lots of engine hooks.
   - **Custom runner** — a JSON/resource graph + a small interpreter when you need
     full control or minimal dependencies. Don't build a *language*; build a graph.
2. **Define the node contract.** A node yields one of: a line (speaker + text),
   a set of choices, a command/side-effect, or an end/jump. The runner advances
   through nodes and hands lines/choices to the UI.
3. **Separate variables from flow.** Keep a variable store (booleans, numbers,
   strings) the dialogue reads/writes; gate choices with conditions over it.
4. **Localize from the start.** Author with **line IDs**, not raw strings, so the
   displayed text comes from a string table keyed by locale.
5. **Drive it from the game loop.** The runner is a state machine: `current` node
   → emit content → wait for input (continue or choice) → advance.
6. **Verify by walking branches.** Exercise each choice path; confirm conditions,
   variable writes, and that every branch reaches an end or a valid jump.

## Patterns

### 1. Engine-neutral dialogue graph (data, not code)

```json
{
  "start": "guard_intro",
  "nodes": {
    "guard_intro": {
      "speaker": "Guard", "line": "DLG_GUARD_001",
      "choices": [
        { "text": "DLG_OPT_BRIBE", "to": "bribe", "if": "gold >= 50",
          "set": { "gold": "gold - 50" } },
        { "text": "DLG_OPT_LEAVE", "to": "end" }
      ]
    },
    "bribe": {
      "speaker": "Guard", "line": "DLG_GUARD_BRIBED",
      "set": { "gate_open": true },
      "next": "end"
    },
    "end": { "end": true }
  }
}
```

`line`/`text` are **string-table IDs** (localization), not literal text. `if`
gates a choice; `set` mutates the variable store. The gold cost sits on the
*choice*, so it is paid once per pick even if the `bribe` node is revisited; the
idempotent `gate_open` write can live on the node. A string `set` value is an
expression, so a literal string needs inner quotes: `"mood": "'angry'"`. The full
interpreter that walks this graph is in `references/runner.md`.

### 2. Runner step (a state machine over the graph)

```gdscript
# Godot 4.7. The runner holds the current node and a variable store. Every line
# waits for the player: the UI calls choose() or the continue callback.
func goto(id: String) -> void:
    current = graph.nodes[id]
    apply_set(current.get("set", {}))
    if current.get("end", false):
        ui.close()
        return
    if current.has("line"):
        ui.show_line(current.get("speaker", ""), localize(current.line))
    if current.has("choices"):
        var shown = current.choices.filter(func(c): return eval_cond(c.get("if", "")))
        ui.show_choices(shown)            # only choices whose condition passes
    elif current.has("next"):
        var next_id: String = current.next
        ui.show_continue(func(): goto(next_id))   # advance when the player continues

func choose(choice: Dictionary) -> void:   # called when the player picks a choice
    apply_set(choice.get("set", {}))       # write on the transition (revisit-safe)
    goto(choice.to)
```

### 3. Ink — branching with knots, choices, and variables (inkle)

```ink
// Ink: '*' = once-only choice, '+' = sticky. [bracketed] text shows only in the
// choice, not the printed result. '->' diverts; '-> END' stops the flow.
VAR gold = 60
-> guard_intro                    // the story starts at the top: divert into a knot

=== guard_intro ===
The guard blocks the gate.
* {gold >= 50} [Offer 50 gold]   "Here, take it."
    ~ gold = gold - 50
    The guard pockets it and steps aside. -> END
* [Leave]   You turn back. -> END
```

Ink tracks how often each knot was seen, so `{visited_knot}` is a built-in
condition. Variables are global (`VAR`) or temporary (`~ temp`).

### 4. Yarn Spinner — nodes, options, and commands (Yarn Spinner 3.x)

```yarn
title: GuardIntro
---
<<declare $gold = 60>>
<<declare $gate_open = false>>
Guard: You can't pass.
-> Offer 50 gold <<if $gold >= 50>>
    <<set $gold = $gold - 50>>
    Guard: ...fine. Go on through.
    <<set $gate_open to true>>
-> Leave
    Guard: Good choice.
===
```

Yarn lines may start with `Speaker:`; options use `->`; `<<set>>`/`<<declare>>`
manage `$variables`; `<<if>>` gates an option; `<<jump NodeName>>` moves between
nodes. Interpolate values in text with `{$gold}`. Declare every variable before first
use: an undeclared one still compiles (Yarn infers its type and a zero/false/empty
start value) with only a warning, which hides typos. These constructs are unchanged from
Yarn Spinner 2.x.

## Pitfalls

- **Hardcoding display strings** instead of line IDs makes localization a
  rewrite. Author against a string table from day one.
- **Inventing a scripting language** for a simple branching tree. If you only
  need lines + choices + flags, a JSON/resource graph plus a 50-line runner beats
  a parser you must maintain. Use Ink/Yarn when writers need real flow control.
- **Variables coupled to the UI**: store narrative state separately so the same
  dialogue works in cutscenes, menus, and tests. Persist it via `save-systems`.
- **Unreachable or dead-end nodes**: a node with no `next`, choices, or end
  silently stalls. Validate that every node terminates or branches.
- **Mutating state in a line node the player can revisit** double-applies (`gold`
  drained twice). Apply `set` on the transition, or guard with a seen-flag.
- **Mixing Ink's `*` (once-only) and `+` (sticky)** by accident: looped menus
  need sticky `+` choices or the options vanish after one use.

## References

- `references/ink-and-yarn.md` — side-by-side syntax cheat sheet (choices,
  diverts/jumps, variables, conditions, includes) and integration notes.
- `references/runner.md` — a complete custom dialogue runner: graph schema,
  condition/expression evaluation, variable store, and localization lookup.

## Related skills

- `save-systems` — persist narrative variables and seen-flags.
- `godot-resources`, `unity-scriptableobjects` — store dialogue as engine data.
- `godot-ui-control` — render text boxes, portraits, and choice buttons.
- `visual-novel`, `rpg` — genres that compose this skill.


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
