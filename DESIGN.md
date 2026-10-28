---
name: "Vie Agentic Skill"
description: "A warm charcoal technical-art studio for a Vietnamese-first agent-runbook library."
colors:
  paper: "#151515"
  surface: "#1d1d1c"
  ink: "#f0eee9"
  muted: "#b0ada7"
  line: "#393835"
  soft: "#252523"
  accent: "#f59962"
  accent-hover: "#ffb585"
  on-accent: "#241a13"
  selected: "#302720"
  selected-line: "#916545"
  warning: "#edbe7c"
  paper-light: "#f6f4ef"
  surface-light: "#fffefa"
  ink-light: "#242321"
  muted-light: "#615e58"
  line-light: "#d7d2c9"
  soft-light: "#ebe7de"
  accent-light: "#a64416"
  accent-hover-light: "#84330d"
  on-accent-light: "#fff9f3"
  selected-light: "#f8e9dc"
  selected-line-light: "#be8d6b"
  warning-light: "#82500b"
typography:
  headline:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "30px"
    lineHeight: 1.2
    letterSpacing: "-.035em"
  title:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "18px"
    lineHeight: 1.2
  body:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "15px"
    lineHeight: 1.65
  description:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "13px"
    lineHeight: 1.75
  label:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "12px"
    lineHeight: 1.65
  button:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "13px"
    fontWeight: 600
    lineHeight: 1.65
  mono:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "12px"
    lineHeight: 1.7
rounded:
  inset: "4px"
  control: "5px"
  button: "6px"
  surface: "8px"
spacing:
  compact: "8px"
  tight: "12px"
  control: "16px"
  item: "20px"
  group: "24px"
  loose: "28px"
  section-mobile: "32px"
  section-inner: "36px"
  split: "40px"
  broad: "48px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "10px 16px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.on-accent}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "10px 16px"
  button-secondary-hover:
    backgroundColor: "{colors.soft}"
  button-text:
    textColor: "{colors.accent}"
    typography: "{typography.button}"
    padding: "8px 0"
  search:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "0 18px"
  filter-chip:
    rounded: "{rounded.control}"
    typography: "{typography.label}"
    padding: "8px 14px"
  filter-chip-selected:
    backgroundColor: "{colors.selected}"
    textColor: "{colors.accent}"
  catalog-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "{spacing.item}"
  catalog-row:
    textColor: "{colors.ink}"
    padding: "20px 8px"
  navigation:
    textColor: "{colors.ink}"
  install-disclosure:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "0 16px"
  command:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.button}"
    padding: "{spacing.compact}"
---

# Design System: Vie Agentic Skill

## Overview

**Creative North Star: "The Warm Charcoal Technical-Art Studio"**

The website combines a technical library's precision with a working 3D studio's
warm, dark surround. This describes the built world, not a new brand proposition:
Vie Agentic Skill remains a Vietnamese-first, multi-agent runbook library. The
pinned Blender Skills reference informs the charcoal/orange material language;
it does not replace the identity or make the whole library a Blender product.

Expression comes from the actual credited Blender render, tightly spaced system
headings, orange actions and readable ruled surfaces. Task controls stay familiar:
native form elements, inline detail, clear prerequisites and compact metadata.
Dark is the default; the light alternative preserves the same hierarchy and
changes the palette by role. This root system covers the public website only,
not the independent design instructions contained inside individual skills.

**Key Characteristics:**
- Warm charcoal surfaces with a restrained orange action hierarchy.
- System sans for Vietnamese text; monospace reserved for commands and shortcuts.
- Flat ruled lists, modest corners and tonal selection rather than floating panels.
- Real credited imagery and visible source, license and prerequisite information.
- Native disclosure, keyboard-visible states and responsive task controls.

## Colors

One orange accent family sits against warm neutrals; amber communicates caution
rather than a second decorative brand color. The frontmatter preserves the exact
source hex values. Unsuffixed tokens are the dark defaults; `-light` tokens are
the corresponding role overrides, not additional accents to mix into dark mode.
Sidecar tonal ramps are synthesized preview metadata, not extra shipped theme
tokens.

### Primary
- **Studio Orange** (`accent`): primary actions, useful links, search icon,
  active navigation and selected filter text.
- **Action Hover** (`accent-hover`): primary-button hover. It becomes lighter in
  the dark theme and deeper in the light theme.
- **Action Ink** (`on-accent`): text on solid orange buttons; use the paired theme
  value rather than assuming white text.

### Neutral
- **Charcoal Ground** (`paper`): page background, command wells and path inputs.
  The light counterpart is warm off-white.
- **Raised Work Surface** (`surface`): search, settings, selects and grid cards.
- **Reading Ink** (`ink`): names, headings and primary text.
- **Quiet Ink** (`muted`): descriptions, labels, supporting instructions and
  provenance; it remains readable rather than disappearing into the ground.
- **Rule** (`line`): one-pixel boundaries between rows, sections and fields.
- **Soft Surface** (`soft`): neutral hover feedback and loading placeholders.
- **Selected Surface** (`selected`) and **Selected Edge** (`selected-line`):
  warm selection fill and its stronger boundary for expanded rows and filters.

### Status
- **Caution Amber** (`warning`): risk metadata and invalid installation-path
  borders. This is informational caution, not a safety certification.

### Named Rules
**The Action Orange Rule.** Use orange for actions, links and selection; keep ordinary descriptions and provenance muted.

**The Paired Theme Rule.** Switch the whole set of role values together, including action text, warning and selection colors.

## Typography

**Display Font:** System sans (`-apple-system`, `BlinkMacSystemFont`, `"Segoe UI"`,
`sans-serif`).

**Body Font:** The same system sans stack.

**Label/Mono Font:** Labels stay sans; code and keyboard hints use `ui-monospace`,
`SFMono-Regular`, `Consolas`, `monospace`.

**Character:** Practical and compact, with no external font dependency or
decorative display face. Tight, balanced major headings contrast with generous
description line-height and small, quiet supporting labels.

### Hierarchy
- **Display** (weight 740, 62px, line-height 1.08): The introduction is a local large-type treatment, not a reusable
  size token: weight (740), line-height (1.08), sizes (62px), (52px) at the
  1200px breakpoint, (44px) at 980px and (42px) at 640px. Major headings share
  tight tracking and balanced wrapping.
- **Headline** (frontmatter headline role): Repeated section headings use the frontmatter headline role.
  Prominent split-section headings range from (40px) down to (32px); catalog
  headings use (32px), then (28px) on narrow screens. These are contextual
  hierarchy adjustments, not a mathematical modular scale.
- **Title** (frontmatter title role): Recurring support titles use the title role; result and collection
  headings also use (22px). Runbook names are (15px), weight (650),
  line-height (1.4) and tracking (-.015em).
- **Body** (frontmatter body role): The base role sets ordinary reading rhythm. Intro/support copy uses
  (14–16px) depending on context; repeated runbook descriptions use the
  description role. Supporting reading blocks are commonly constrained to
  (55–75ch), while the introduction uses (48ch).
- **Label** (frontmatter label role): The label role is the normal supporting size, with (11px) tags and
  counts. Most Vietnamese labels keep natural case; explicit lifecycle labels
  may be uppercase. Buttons use the dedicated medium-weight role.
- **Mono** (frontmatter mono role): Commands use the mono role with wrapping for long arguments; general
  inline code starts at (.85em) relative to its surrounding text.

### Named Rules
**The Readable Density Rule.** Create compactness through hierarchy and grouping, not by compressing description line-height or clipping an expanded runbook's only full-text access.

## Layout

The shared shell is centered with a maximum width (1440px) and horizontal padding
(56px), reducing to (32px) at 1200px and (20px) at 640px. The spacing entries are
observed recurring steps, not an enforced single-base arithmetic scale.

The catalog is list-first, with an optional grid. On wide screens a sticky filter
rail (210px) sits beside a flexible result column with a (36px) gap; at 1200px it
becomes (190px) with a (24px) gap. At 980px the rail becomes a static, two-column
form above the results. Grid results use three columns, two at 1200px and one at
640px. Ruled rows align identity, a short description and the open action;
expanded detail remains inline. Narrow rows put the description beneath the
identity and stack the installation panel below it.

Split reading sections collapse to one column at 640px. Image collections step
from five columns to three at 1200px and two at 640px. On narrow screens the quick
filters scroll horizontally rather than shrinking targets; the lifecycle track
also scrolls when necessary. Settings fields stack at 640px.

The header stays at the top. Desktop navigation yields to a native button-driven
menu at 980px; at 640px the header is shorter and secondary header content is
hidden. Anchor offsets account for the sticky header. Recurring major sections
use a top rule and generous separation (88px above, 56px inside on desktop;
60px and 36px on mobile). Local viewport choreography belongs in the existing
surface brief, not in this reusable system.

## Elevation & Depth

Depth is predominantly flat and structural: one-pixel rules, slightly distinct
surface tones and warm selected fills. Cards, search and ordinary settings do
not float on shadows. The actual render supplies photographic depth without
turning the surrounding controls into a simulated 3D interface.

### Shadow Vocabulary
- **Status overlay** (`box-shadow: 0 8px 24px #00000040`): the transient toast.
- **Manual-copy overlay** (`box-shadow: 0 8px 30px #00000040`): the clipboard
  fallback panel above the page.

### Named Rules
**The Flat Workspace Rule.** Keep ordinary content flat; reserve drop shadows for the toast and manual-copy overlays.

## Shapes

The recurring surface corner is modest and gently curved, never a capsule.
The surface radius covers search, settings, selected rows, grid cards and fallback
panels; button corners also shape command wells and toasts. Smaller control
corners shape selects, filter buttons, path inputs and thumbnails, with inset
corners for shortcut hints and the search input's inner focus outline.
Separators are predominantly straight one-pixel rules. Simple outline icons
normally occupy (20px) with stroke width (1.7), round caps and round joins.

## Components

### Buttons
Direct and recognizable rather than ornamental.
- **Shape:** Button radius, one-pixel border, inline-flex alignment, (10px) icon
  gap and padding (10px 16px); common minimum target height (44px). Intro action
  targets grow to (48px).
- **Primary:** Solid action color with its paired action ink; hover uses the
  action-hover token.
- **Secondary:** Work-surface fill and rule border; hover changes to soft fill
  and muted border.
- **Text / icon:** Text actions are orange with no filled container. Icon actions
  are at least (44px) wide and use soft fill on hover.
- **Focus / disabled:** Interactive elements have a (2px) accent outline offset
  (4px). Disabled buttons use opacity (.6) and a not-allowed cursor.
- **Motion:** Filled and icon buttons transition background and border colors
  over (.18s ease-out), without a lift or scale transform.

### Filters and Metadata
Filters are small rectangular controls, not rounded status badges.
- Filter controls use the control radius, rule border, label type and padding
  (8px 14px), with a minimum height (44px).
- Selected filters use the selected surface, selected edge and orange text;
  `aria-pressed` carries the state. Sidebar category selection uses the same
  fill and text relationship without a surrounding stroke.
- Runbook tags are plain muted text with slash separators. Do not confuse these
  metadata labels with interactive filter chips.

### Lists / Cards / Containers
The result list is the primary discovery pattern; the grid is an existing
alternative, not a replacement.
- Collapsed rows are separated by rules, with padding (20px 8px) on desktop.
  Names and explicit open buttons both provide access to detail.
- Expanded rows use selected fill and edge, surface corners and padding (24px).
  Provenance and runbook access remain visible next to installation controls.
- Grid cards use work-surface fill, rule borders, surface corners and padding
  (20px), without a drop shadow.
- Showcase items are image-led thumbnails followed by a text action and short
  description, not large filled promotional cards.

### Inputs / Fields
Native controls framed with the same warm rules.
- Search is a work-surface container with surface corners, minimum height (60px)
  and an orange icon. Its border turns orange on focus-within; the input retains
  a visible inner focus outline.
- Selects use a rule border, control corners, native affordance and minimum
  height (44px). Path fields use the page ground, with warning-colored borders
  for `aria-invalid="true"` and adjacent explanatory text.
- Preserve labels, keyboard shortcuts and wrapping of long paths. The mobile
  layout hides only the visual shortcut hint, not keyboard support.

### Navigation
Quiet, text-led and anchored to the working library.
- Desktop links are small (13px); the current link is orange with an inset
  bottom rule (2px). Hovered text links become orange.
- The identity combines the VAS mark with the Vie Agentic Skill name. The mark
  becomes white in dark mode; it is not replaced with the reference site's brand.
- Mobile navigation uses the existing menu control, visible focus,
  `aria-expanded` and a wrap-friendly link area.

### Native Disclosure and Inline Installation
Additional setup is available without keeping a full settings form on display.
- Installation preferences use native `details` / `summary` in a bordered work
  surface. A destination link opens the disclosure before moving to its field.
- Native description and FAQ disclosures retain access to longer text.
- Installation commands sit in a bordered page-ground well with button corners,
  wrapping mono text and an explicit copy action. Invalid or incomplete
  destinations disable copy and show the actual requirement.
- Use the existing toast for copy success and the manual-copy panel when the
  Clipboard API is unavailable. Loading, retry and empty-result states are real
  task states, not decorative illustrations.

### Imagery and Credits
The Blender artwork is a real supplied render, not evidence of universal 3D
capability. Keep its source link and MIT credit visible. Supporting collection
illustrations keep their image-first proportions and do not replace runbook
names or descriptions. Retain the broader VAS identity and explicit Blender/MCP
prerequisites wherever the collection is explained.

## Do's and Don'ts

### Do:
- **Do** use the complete theme role set and the paired text color on orange actions.
- **Do** preserve Vietnamese-first labels, system-font rendering and readable supporting text.
- **Do** keep ruled list discovery and the optional grid consistent with the same selected state.
- **Do** retain visible focus, native disclosure and the reduced-motion alternative.
- **Do** keep the credited Blender render, VAS identity, provenance and explicit prerequisites.
- **Do** let long commands, paths and runbook names wrap within responsive containers.

### Don't:
- **Don't** turn the orange action hierarchy into decorative full-surface color.
- **Don't** add floating shadows to ordinary catalog rows, cards or settings.
- **Don't** replace plain metadata with interactive-looking badges.
- **Don't** substitute the reference site's identity for Vie Agentic Skill or imply every runbook operates Blender.
- **Don't** present catalog risk metadata as a safety guarantee or hide requirements behind promotional copy.
- **Don't** introduce movement that survives the existing reduced-motion preference.
