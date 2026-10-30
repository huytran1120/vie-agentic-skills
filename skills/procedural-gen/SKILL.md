---
name: procedural-gen
description: >
  Generate game content procedurally — seeded deterministic RNG, value/Perlin/
  Simplex noise for terrain and heightmaps, grid dungeon generation (rooms +
  corridors, BSP, random walk, wave function collapse), and weighted loot/drop
  tables. Engine-neutral algorithms. Use when the user mentions procedural
  generation, perlin/simplex noise, random seed, dungeon generator, WFC,
  heightmap/terrain, or loot tables.
---

# Procedural generation

Generate levels, terrain, and loot from compact rules and a seed. The throughline
of good procgen is **determinism**: a single seed reproduces the same world, so
bugs are repeatable and players can share seeds. This skill owns the core
algorithms — noise, seeded RNG, dungeon layout, weighted tables; genres like
`roguelike` and `survival-crafting` consume it.

## When to use

- Use to generate maps, dungeons, terrain heightmaps, item drops, or any content
  you do not want to author by hand.
- Use when results must be **reproducible from a seed** (debugging, daily
  challenges, shareable worlds).
- Use to pick weighted random outcomes (loot rarity, spawn tables).

**When *not* to use:** for the engine's tile API to *paint* the result, use
`godot-tilemap` or `unity-tilemap-2d`. For routing AI through the generated map,
use `game-ai`. For carefully hand-paced levels, use `level-design` — procgen and
authored design are complementary, not interchangeable.

## Core workflow

1. **Own your randomness.** Create one seeded RNG instance and pass it
   everywhere. Never call the global/static random in generation code — it makes
   results irreproducible and order-dependent.
2. **Pick the technique for the content.** Continuous terrain/heightmaps → noise.
   Discrete rooms/corridors → space partitioning or agent-based carving.
   Outcomes with rarities → weighted tables.
3. **Generate into a plain data grid/array first**, decoupled from rendering.
   Generation fills `int[][]` or a dict; a separate pass draws it.
4. **Validate before shipping the result to the player.** Is every room
   reachable? Is the spawn safe? Is there a path to the exit? Reject or repair
   layouts that fail; do not hand the player a broken map.
5. **Tune with the seed fixed** so each parameter change is visible in isolation,
   then sweep seeds to check the distribution, not just one lucky map.

## Patterns

### 1. Seeded, deterministic RNG (the foundation)

```python
import random
rng = random.Random(seed)        # a dedicated instance — NOT the global random.*
room_count = rng.randint(5, 12)  # same seed -> same sequence, every run
# RIGHT: thread `rng` through every function that makes a choice.
# WRONG: calling random.randint(...) (global state) — order-dependent, unseedable.
```

Engine equivalents: Godot 4.7 `var rng := RandomNumberGenerator.new(); rng.seed = s`
(save `rng.state` to resume a sequence mid-way); Unity 6.3
`new Unity.Mathematics.Random(seed)` (a `uint`, must be non-zero) or
`new System.Random(seed)`. Avoid `UnityEngine.Random.InitState` for generation:
it seeds the one global generator that every other script also draws from.
Store the seed in the save file so a world can be regenerated.

### 2. Fractal (fBm) noise for heightmaps

```python
# Sum several octaves: each higher octave has higher frequency, lower amplitude.
def fbm(noise, x, y, octaves=5, lacunarity=2.0, gain=0.5):
    total, amp, freq, norm = 0.0, 1.0, 1.0, 0.0
    for _ in range(octaves):
        total += amp * noise(x * freq, y * freq)   # noise() returns ~0..1
        norm  += amp                                # track total amplitude
        amp   *= gain                               # each octave contributes less
        freq  *= lacunarity                         # ...at a higher frequency
    return total / norm                             # normalize back into 0..1

# Redistribute to carve flat valleys / sharpen peaks: higher exp -> more lowland.
elevation = pow(fbm(noise, nx, ny), 2.2)
```

Use a real noise library (`FastNoiseLite`, `opensimplex`,
`Unity.Mathematics.noise`, or `Mathf.PerlinNoise`) — do not implement gradient
noise yourself. Seed **elevation and moisture with different seeds** so a
biome lookup over both fields isn't perfectly correlated. Full biome lookup and
island shaping are in `references/noise.md`.

### 3. Weighted loot table (rarity-correct selection)

```python
# Roll proportional to weight: common drops far more often than legendary.
def weighted_pick(rng, table):           # table: list of (item, weight)
    total = sum(w for _, w in table)
    roll = rng.uniform(0, total)          # a point on the cumulative line
    upto = 0.0
    for item, w in table:
        upto += w
        if roll < upto:                   # first bucket the roll falls into
            return item
    return next(i for i, w in reversed(table) if w > 0)  # roll == total (float edge)

loot = weighted_pick(rng, [("common", 70), ("rare", 25), ("legendary", 5)])
```

Weights need not sum to 100 — they are relative, and a weight of 0 never drops.
Built-ins do the same job: Python `rng.choices(items, weights)`, Godot
`rng.rand_weighted(PackedFloat32Array(weights))` (returns an index). To prevent
bad streaks, use a "pity"/bag system (see `references/dungeon-generation.md`
notes on distributions).

### 4. Rooms-and-corridors dungeon (sketch)

```python
# 1. Place non-overlapping rooms; 2. connect them; 3. carve into the grid.
rooms = []
for _ in range(attempts):
    r = Rect(rng.randint(1, W-w-1), rng.randint(1, H-h-1), w, h)
    if not any(r.intersects(o.expand(1)) for o in rooms):  # keep a 1-tile gap
        rooms.append(r)
for a, b in zip(rooms, rooms[1:]):       # connect each room to the next
    carve_l_corridor(grid, a.center, b.center, rng)   # horizontal then vertical
```

The complete generator (BSP partitioning, L-corridors, reachability check, and
random-walk caves) is in `references/dungeon-generation.md`.

## Pitfalls

- **Using the global RNG** inside generation makes worlds unreproducible and
  breaks the moment call order changes. Always pass a seeded instance.
- **Correlated noise fields**: sampling elevation and moisture from the *same*
  seed/offset produces biomes that line up in bands. Offset or reseed each field.
- **Octave artifacts**: adding octaves without renormalizing pushes values out of
  `0..1`; divide by the summed amplitude (and beware library output ranges — some
  return `-1..1`, some `0..1`).
- **No connectivity check**: rooms or caves can end up isolated. Flood-fill from
  the spawn and discard/reconnect unreachable regions before play.
- **Unbounded placement loops**: "keep trying until N rooms fit" can spin forever
  on a small grid. Cap attempts and accept fewer rooms.
- **Seeding once globally, then relying on frame timing**: any non-deterministic
  input (time, physics, hash randomization) leaking into generation destroys
  reproducibility. A common hidden one: `rng.choice(list(some_set))` over
  strings in Python, whose set order changes per process. Sort first.
- **Seeds that stop matching after an update.** Library RNGs promise the same
  sequence only on the same version: Python guarantees only `random()` across
  versions (not `randint`/`choice`), .NET says `System.Random` may change
  between major versions, and Godot calls its PCG32 an implementation detail.
  If shared seeds, daily challenges or seed-only saves must survive updates,
  ship your own small PRNG (PCG32, xorshift, SplitMix64) with a test that pins
  its first outputs — or save the generated result instead of the seed.
- **Flat noise at integer coordinates**: Perlin noise is 0 at every integer
  lattice point, so sampling raw `noise(x, y)` (e.g. `Mathf.PerlinNoise`) at
  whole tile coordinates returns the same value everywhere. Scale by a
  non-integer frequency (`x / width * f`); libraries with a frequency setting,
  such as FastNoiseLite, apply it for you.

## References

- `references/noise.md` — octaves/lacunarity/gain, redistribution, island
  shaping, two-axis biome lookup, blue-noise object scatter.
- `references/dungeon-generation.md` — BSP, rooms+corridors, random-walk caves,
  cellular-automata smoothing, wave function collapse, connectivity validation,
  distribution/pity tables.

## Related skills

- `godot-tilemap`, `unity-tilemap-2d` — paint the generated grid into the engine.
- `game-ai` — pathfinding over the generated graph.
- `level-design` — pacing and hand-authored structure that procgen complements.
- `roguelike`, `survival-crafting` — genres that compose this skill.


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
