---
name: prototype-fast
description: >
  Build a playable prototype in about an hour to answer one question — is it fun? — with
  greybox primitives, a hard timebox, and explicit keep/kill criteria. Use when prototyping
  a mechanic, making a vertical slice or MVP, greyboxing/blockout, or judging throwaway vs keep.
---

# Prototype Fast

Get a mechanic into a player's hands fast to learn whether it's worth building. The output of
a prototype is a **decision** (keep / kill / refactor), not a product. Optimize for learning
speed, and decide up front whether the code is throwaway or load-bearing.

## When to use

- Use when validating a single mechanic or "what if", building a vertical slice / MVP,
  greyboxing a level or interaction, or de-risking an idea before committing real time.
- Use when the user says "just get something playable", "is this fun?", or "rough it in".

**When *not* to use:** a timed competition with a deadline and a submission (use `game-jam`);
shipping or updating a real release (use `steam-publish` / `itch-publish`); building the
production version of a validated feature (use the engine/genre skill directly).

## Core workflow

1. **Write the one question.** State the single thing the prototype must answer, e.g.
   *"Is grappling-while-falling satisfying to control?"* If you have two questions, build two
   prototypes. A prototype that tests everything tests nothing.
2. **Decide throwaway vs keep — before you write code.** Throwaway (a *spike*): hard-code,
   no architecture, delete after. Keep: still rough, but folder/names you can grow. Most
   prototypes should be throwaway; pretending otherwise is how prototypes rot into the
   shipping codebase.
3. **Set a hard timebox** (30-90 min for a mechanic; one sitting for a slice) and a visible
   timer. The constraint is the point — it forces you to test the *core* idea, not the trim.
4. **Greybox everything non-essential.** Primitives for art (boxes, circles, capsules),
   built-in fonts, one debug sound or none. Spend zero minutes on anything the question
   doesn't depend on.
5. **Instrument for the question.** Add on-screen debug text / gizmos that show the thing you
   are judging (speed, distance, timing window). You're measuring, not decorating.
6. **Playtest immediately and honestly.** Play it yourself, then hand it to one other person
   without explaining the controls. Watch where they struggle.
7. **Make the call against your kill criteria** (below). Keep → schedule the real build and
   *rewrite*, don't promote the spike. Kill → log the lesson and move on. Refactor → narrow
   the question and spike again.

## Patterns

### 1. The prototype brief (fill this in before coding)

```text
QUESTION:     The one thing this must prove (binary if possible).
CORE VERB:    The single action the player repeats.
THROWAWAY?:   yes -> hard-code freely, delete after.  no -> minimal structure to grow.
TIMEBOX:      e.g. 60 min. Stop when it rings, even if unfinished.
KEEP IF:      observable signal that means "fun / worth building" (see kill criteria).
KILL IF:      observable signal that means "stop".
```

### 2. Greybox the core loop, fake everything else (engine-agnostic pseudocode)

```text
# Only the CORE VERB is real. Visuals are primitives; systems are stubs.
on update(dt):
    read_input()
    apply_core_mechanic(dt)        # the ONLY thing you're testing — make this feel right
    draw_primitive(player)         # a box. not a sprite. not animated.
    draw_debug_hud(speed, timing)  # show the numbers you're judging
    # enemies, menus, save, audio, art -> stubbed or absent until the verb proves out
```

### 3. Kill criteria — make the keep/kill call observable, not emotional

```text
KEEP when, with placeholder art:
  - a fresh player does the core verb on purpose within ~30s, unprompted, and
  - you (or they) repeat the loop "one more time" without being asked.
KILL when:
  - the verb only feels good after you explain it, or
  - making it fun needs systems far beyond the prototype's scope, or
  - you're adding art/levels to avoid admitting the verb is flat.
REFACTOR when one variable is clearly off (too slow, window too tight) -> retune, retest.
```

### 4. Containment: keep a spike out of the shipping codebase

```text
prototypes/<idea-name>/      # separate folder or project, never imported by main game
  - hard-coded values, single file ok, magic numbers welcome
  - committed on a throwaway branch (or not at all)
Rule: a "keep" decision authorizes a REWRITE in the real project, not a copy-paste of the
spike. Prototype code carries prototype assumptions; shipping it ships the assumptions.
```

## Pitfalls

- **Polishing too early.** Art, menus, and audio make a flat mechanic look finished and
  delay the verdict. Greybox until the verb is proven.
- **No kill criteria.** Without a written "kill if", every prototype "has potential" and
  nothing gets cut. Decide the signal *before* you're attached to the code.
- **Building systems instead of the mechanic.** Inventory, save/load, and settings are not
  the question. Stub them.
- **The spike becomes the product.** Throwaway code promoted to production is technical debt
  with a fun origin story. Rewrite on a keep.
- **Prototyping in the real codebase.** It tangles experiments with shipping systems and
  makes the spike expensive to delete. Use a separate folder/project.
- **Testing only yourself.** You know the controls and the intent. One uncoached outside
  player reveals more in two minutes than an hour of self-play.

## References

- For working under a hard external deadline and submitting, read the `game-jam` skill.
- For the engine-specific core loop you'll greybox in, read that engine's skill
  (`godot-gdscript`, `phaser-core`, `love2d-core`, `unity-csharp-scripting`, …).

## Related skills

- `game-jam` — same scope discipline applied to a timed competition with a submission.
- Engine cores and genre skills — where a "keep" decision gets rebuilt properly.


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
