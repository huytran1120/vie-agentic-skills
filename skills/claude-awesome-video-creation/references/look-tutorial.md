# Look: tutorial mode

## Tokens (one file, nothing hard-coded elsewhere)
| token | hex | role |
|---|---|---|
| ink | `#081024` | stage (deep navy) |
| surface / surface2 | `#10224A` / `#163061` | code boxes, chips |
| line / line2 | `#213B6E` / `#2D4C85` | hairlines |
| text / muted / dim | `#EEF2FF` / `#93A4C8` / `#5E719A` | type |
| term / termBar | `#193549` / `#15232D` | Cobalt2-blue windows |
| cyan / violet / gold / pink / lime | `#5EE7FF` / `#B48CFF` / `#FFC857` / `#FF6FA3` / `#9BE564` | step, stage and label hues; syntax |
| ember / emberGlow | `#E07A50` / `#FFB38A` | the brand accent: the skill, the payoff word |

## Stage
`KeyLight` aurora: three radial gradients (cyan 0.09, violet 0.10, ember 0.08 alpha) orbiting slowly, `mixBlendMode: screen`, plus a vignette and light grain.

## macOS glass window (`Win` in `assets/examples/teach-it-once/ui.tsx`)
- 12 px radius; border `1px rgba(255,255,255,0.16)`; shadow `0 0 0 1px black/0.5, 0 34px 90px black/0.55, 0 12px 30px black/0.35, 0 0 70px cyan/0.07`.
- Body: `linear-gradient(135deg, white/0.09 0%, white/0.02 28%, transparent 50%), linear-gradient(180deg, term/0.92, term/0.82)`.
- 38 px title bar: a white/0.10 → termBar/0.55 gradient, an inset top highlight, 12 px traffic lights (radial highlight, 0.5 px dark rim), and the title centred in 15 px sans.
- Titles like a real Mac terminal: `my-project — zsh — 96×24`, `my-project — claude`.

## Syntax (`Sh`)
Tokens are split on spaces and quoted strings:
- the prompt (`%`, `$`, `>`, `PS>`) is lime;
- the first word after a prompt, `&&` or `|` is the command, cyan and bold;
- `-flags` are gold;
- URLs and paths are violet;
- `"strings"` are pink;
- `<placeholders>` are gold.

## Colour-coding ideas
- STEP 1/2/3 use cyan / violet / lime as solid chips with dark text and a glow.
- Loading stages: Discovery cyan, Activation violet, Execution lime.
- File-tree labels and editor tags each get a hue (name cyan, description gold, steps violet).
- Cheat-sheet row numbers are solid chips in five hues.

## Type
Geist for UI and statements, JetBrains Mono for code and terminals, and Instrument Serif Italic for the single payoff word per scene ("zero.", "right now.", "Teach it once.").
