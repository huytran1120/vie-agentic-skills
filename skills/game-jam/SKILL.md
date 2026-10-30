---
name: game-jam
description: >
  Plan and ship a game under a jam deadline: lock scope to the clock, schedule the hours,
  cut features, and submit on time. Use for a game jam (Ludum Dare, GMTK Jam, Global Game
  Jam), a 48-hour or weekend build, or scoping and submitting a jam entry.
---

# Game Jam

Turn a theme and a fixed deadline into a finished, submitted game. This is a planning and
scope-control playbook, not engine code: the win condition is *something submitted and
playable*, not *the game you imagined*.

## When to use

- Use when entering a timed jam (Ludum Dare, GMTK Jam, Global Game Jam, a weekend jam),
  scoping a 48-hour build, or deciding what to cut to hit a deadline.
- Use when the user asks "what can I actually build in a weekend" or "how do I submit to
  this jam".

**When *not* to use:** building the *core loop* in engine code (use the engine skill —
`godot-2d-movement`, `phaser-core`, etc. — or a genre skill like `platformer`); throwaway
experiments with no deadline (use `prototype-fast`); shipping a commercial release (use
`steam-publish` / `itch-publish`).

## Core workflow

1. **Read the rules before the theme drops.** Confirm the jam's *length*, *theme reveal
   time*, *submission deadline (with timezone)*, whether teams/pre-made assets/engines are
   allowed, its *generative AI* policy, which platforms the build must run on (often Windows
   or browser), *where* you submit (an itch.io jam page, or the jam's own site), whether
   uploads lock once the deadline passes, and whether ratings require you to rate other
   entries. Missing one of these disqualifies an otherwise-finished game.
2. **Prep the boring parts in advance** (allowed by most jams): empty project that builds
   and exports, input + a title/end screen stub, an export pipeline you've run once, and a
   font/SFX source you're licensed to use. Day-one time is too precious to spend here.
3. **Theme → one sentence.** Brainstorm 10 ideas in 15 minutes, then commit to **one**
   expressible as: *"You [verb] to [goal] while [constraint]."* If you can't say it in one
   sentence, it's too big.
4. **Scope to the clock, not the idea.** Use the budget table below. Pick **one** core
   mechanic and **one** "hook". Everything else is a stretch goal.
5. **Build the vertical slice first.** Get a 30-second playable loop (start → play → lose/win
   → restart) running early. A complete tiny loop beats a half-built big one.
6. **Reserve the last ~20% of the clock for shipping**, not features. Export, test the build
   on a clean path, capture screenshots, write the page. Builds always break at hour 47.
7. **Submit early, update if time remains.** Upload a working build *well before* the
   deadline; you can usually replace the file until submissions close. After that, many jams
   lock uploads for the whole rating period or allow only declared bug fixes, so the build
   you have at the deadline is the one people rate. A submitted mediocre game scores; an
   unsubmitted great one does not.

## Patterns

### 1. Scope budget by jam length (plan backwards from the deadline)

```text
              | 48-hour jam            | 72-96 hour jam        | 1-week jam
--------------|------------------------|-----------------------|------------------------
Core mechanic | 1, proven by hour 6    | 1-2                   | 2-3 interacting
Levels/content| 1 hand-made or gen'd   | 3-5                   | 8-12 + progression
Art           | placeholder/1 palette  | cohesive 1-artist set | themed set + UI
Audio         | 3-5 SFX + 1 loop       | SFX + 1-2 tracks      | adaptive music
SHIP BUFFER   | last 8-10 h            | last 12-16 h          | last full day
```

### 2. The 48-hour timeline (concrete blocks)

```text
H0-2    Ideate -> lock ONE-sentence concept -> name the core mechanic + win/lose.
H2-8    Core loop in code with primitives (boxes/circles). Make it playable, no art.
H8-12   Sleep. (Tired code is tomorrow's bug list.)
H12-24  Content: 1 level/encounter, tune difficulty, add the "hook" feature.
H24-30  Sleep + playtest with one other person; cut anything not landing.
H30-38  Art + audio pass. Juice: screenshake, hit-stop, tween, particles, SFX.
H38-44  Bug-fix freeze: no new features. Fix only crashes + soft-locks.
H44-48  EXPORT, test the build clean, screenshots, write page, SUBMIT (by ~H46).
```

### 3. Feature triage — decide fast, decide out loud

```text
For every feature ask, in order:
  1. Does the core loop work WITHOUT it?   -> if yes, it's a stretch goal, not MVP.
  2. Can a player tell it's missing?       -> if no, cut it.
  3. Is it < 30 min of work?               -> if no, defer past the ship buffer.
Default answer under deadline pressure is CUT. You can always add in a post-jam version.
```

### 4. Pre-submission build check (run on a clean copy, not your dev folder)

```text
[ ] Build runs from an extracted zip on a path with NO engine/IDE installed.
[ ] Controls are shown on-screen or on the page (jurors won't read your mind).
[ ] No dev console errors; no soft-lock; restart works.
[ ] Web build (if any) is set to the platform's playable-in-browser mode.
[ ] Page has: 1-line pitch, controls, screenshots, credits + asset licenses.
[ ] File uploaded and the submission is actually attached to the JAM, not just the page.
```

### 5. Format rules of the big recurring jams (re-check the current event page)

```text
Ludum Dare   Two categories. COMPO: solo, 48 h, all art/music/sound made during the
             event, source code must be shared. JAM: 72 h, solo or team, any base code;
             third-party or old assets are fine but opt out of Graphics/Audio voting.
             One extra "submission hour" for packaging; after it, only declared bug
             fixes and ports, no new features. Entries live on ldjam.com and link to
             builds you host elsewhere (for example on itch.io). Rating others raises
             your entry's visibility ("Coolness").
GMTK Jam     Hosted on itch.io, solo or team, runs about four days. Must be playable
             on Windows or in a browser with keyboard/mouse. Generative AI art and
             audio get the entry disqualified. Uploads lock during the rating period;
             linking to a "fixed" build elsewhere is also grounds for disqualification.
Global Game  Run at local sites; each site picks its own 48 h window inside a 7-day
Jam          period, and the submission deadline is local time. Submit on
             globalgamejam.org with source code and all original assets before the jam
             ends; GGJ projects are released open source under a Creative Commons
             license, so plan any commercial follow-up with that in mind.
```

## Pitfalls

- **Scope creep is the #1 jam killer.** If the core loop isn't playable by the first third
  of the clock, cut features now, not later.
- **No ship buffer.** Exporting, zipping, and writing the page reliably takes 1-3 hours and
  always surfaces a build bug. Treat the deadline as ~2 hours earlier than it is.
- **Submitting to the page but not the jam.** On itch.io a jam entry is a separate
  *submission* linked from the jam page — uploading the game alone does not enter it.
- **Fixing the build after the deadline.** Where uploads lock for rating, the locked build is
  what gets rated; posting a link to a newer build can disqualify the entry. Where fixes are
  allowed (Ludum Dare), fix only bugs, add no features, and list the changes on the entry.
- **Untested export.** "Works in the editor" is not "works in the build." Test the exported
  artifact on a clean path; missing assets and wrong working directories are classic.
- **Unlicensed assets.** Music/fonts/sprites pulled from the web can violate jam rules and
  break later distribution. Use assets you're licensed for and list them in the credits.
  Check the jam's generative AI rule too: some jams disqualify AI-made art or audio.
- **Polishing before the loop is fun.** Juice multiplies fun; it can't create it. Get the
  loop right with placeholders first.

## References

- For the throwaway-vs-keep prototyping mindset and greyboxing technique, read the
  `prototype-fast` skill.
- For the actual upload mechanics (project page, channels, `butler push`), read
  `itch-publish`.
- Primary sources for Pattern 5: the Ludum Dare rules (`ldjam.com/events/ludum-dare/rules`),
  the current GMTK Game Jam page on itch.io, and `globalgamejam.org` ("What is a game jam?"
  and "Upload your game!"). Rules change between events; read the live page.

## Related skills

- `prototype-fast` — validate a mechanic quickly before committing jam hours to it.
- `itch-publish` — create the page and upload the build (most jams are hosted on itch.io).
- Engine cores (`phaser-core`, `love2d-core`, `godot-gdscript`, …) and genre skills
  (`platformer`, `roguelike`, …) — build the actual loop the jam scopes around.


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
