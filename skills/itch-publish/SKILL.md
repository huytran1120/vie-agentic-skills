---
name: itch-publish
description: >
  Publish and update a game on itch.io: create the project page and upload builds with the
  butler CLI (butler push) to named channels. Use for itch.io publishing, butler push,
  channel naming for Windows/macOS/Linux/HTML5, versioning uploads, or shipping a jam or
  release build to itch.io.
---

# itch.io Publish (butler)

Get a build onto an itch.io page and keep it updated. The page is created in the browser; all
uploads go through **butler**, itch.io's command-line tool, with one command you'll use
forever: `butler push`. butler diffs against the previous build and uploads only what
changed. Deep CI/CD and flag detail lives in `references/butler-ci.md`.

## When to use

- Use when creating/updating an itch.io project page, installing or logging in to butler,
  uploading a build with `butler push`, choosing channel names, versioning uploads, or
  shipping a jam/demo/release build to itch.io.
- Triggers: `butler push`, `butler login`, channels, `.itch.toml`, "publish on itch",
  "upload to itch".

**When *not* to use:** publishing on Steam (use `steam-publish`); jam *scope/planning* (use
`game-jam` — this skill is only the upload mechanics); building the game itself (engine
skills).

## Core workflow

1. **Create the project page** at `itch.io/game/new` — butler pushes only to a page that
   already exists. Set the **Kind of project**: keep *Downloadable* for native builds, or
   choose **HTML** for a browser-playable game (this is required for web builds — see
   Pitfalls). Set pricing and keep visibility at **Draft** (or Restricted for testers) until
   the page is finished: the first public publish puts it on *Most Recent* once, and it
   cannot go back to the top later.
2. **Install butler and log in.** Download from `itchio.itch.io/butler`, add it to `PATH`,
   then `butler login` (opens a browser to authorize). Verify with `butler version`. For
   CI, use `BUTLER_API_KEY` instead — see the reference. (The itch desktop app also has a
   graphical push screen that uses its own bundled butler, if the user prefers no CLI.)
3. **Prepare a portable build folder** — the exact files a player runs, nothing extra. Push a
   **folder** (or a single `.zip` *of* that folder), **not an installer** and **not a
   pre-compressed archive of archives** (hurts patching; see Pitfalls).
4. **Push to a channel:** `butler push <dir> <user>/<game>:<channel>`. `<user>/<game>` is
   the lowercase page address (`finji.itch.io/overland` → `finji/overland`). The channel name
   determines the platform tag (see Patterns). The first push uploads everything; later
   pushes to the same channel upload only the diff.
5. **Fill in the *Edit game* page, then Save.** Fix platform tags if a channel wasn't
   auto-tagged correctly — tick only platforms you have actually run the build on. For
   browser games also flip the page to **HTML** and tag the channel *playable in browser*.
   Answer the **AI generation disclosure** section if any shipped content was made with
   generative AI (mandatory for asset pages, which are delisted without it), and mark adult
   content under *Metadata → Classification*.
6. **Version your builds** (optional but recommended): `--userversion 1.2.0` or
   `--userversion-file build.txt` so you control the version string players and the update
   API see.
7. **Update later** by pushing to the *same* channel again. Use `butler status <user>/<game>`
   to see channels/builds and `butler push-preview` to see what a push would change before
   sending it.

## Patterns

### 1. The one command you need — `butler push`

```bash
# butler push <directory-or-zip> <user>/<game>:<channel>
butler push ./build/windows leafy/my-game:windows
butler push ./build/mac     leafy/my-game:osx
butler push ./build/linux   leafy/my-game:linux
butler push ./web           leafy/my-game:html   # browser build (also set page Kind = HTML)
```

### 2. Channel naming controls the platform tag (kebab-case, lowercase)

```text
Substring in channel name -> auto-applied tag:
  win / windows  -> Windows        linux -> Linux
  mac / osx      -> macOS          android -> Android
Multiple platforms in one channel are allowed: e.g. a Java jar:
  butler push ./jar leafy/my-game:win-linux-mac
Convention: lowercase words separated by dashes (windows-beta, osx-demo, soundtrack).
Tags are only the INITIAL guess — fix them anytime on the Edit game page (then Save).
There is no tag for CPU architecture: name the channel (windows-arm64) if you ship several.
```

### 3. Version, verify, and preview

```bash
butler version                              # print version; confirms install + PATH
butler login                                # authorize this machine (opens browser)

# Set an explicit version string instead of itch's auto-incrementing integer:
butler push ./build leafy/my-game:windows --userversion 1.2.0
butler push ./build leafy/my-game:windows --userversion-file build_number.txt

butler status leafy/my-game                 # list channels + latest builds/versions
butler push-preview ./build leafy/my-game:windows   # NEW/MODIFIED/DELETED/SAME, uploads nothing
```

### 4. First-time, hidden, and filtered pushes

```bash
# Hide a brand-new channel from the page until you're ready (NEW channels only):
butler push ./build leafy/my-game:windows-beta --hidden

# Exclude files from the upload without copying the folder (--ignore is repeatable):
butler push ./build leafy/my-game:windows --ignore '*.pdb' --ignore '*.dSYM'

# Preview exactly what would be sent, without sending it:
butler push ./build leafy/my-game:windows --dry-run
```

## Pitfalls

- **Pushing an installer.** itch.io patches *portable* builds; an installer (`.exe`/`.msi`)
  defeats patching and the itch app's auto-update, and may need admin rights players don't
  have. Push the extracted, runnable folder instead.
- **Pre-compressed builds.** Pushing a heavily compressed archive (or an archive of archives)
  makes patches huge — a tiny change rewrites the whole compressed blob. Push uncompressed
  files; itch.io compresses on its side.
- **A folder containing only one `.zip`.** butler auto-unzips it and pushes the contents
  (to avoid a "zip in a zip"). Pass `--no-auto-unzip` only if you truly want the zip uploaded
  as one opaque file.
- **HTML5 game shows as a download.** Two switches are required: set the page **Kind** to
  *HTML* and tag the channel *playable in browser* on the *Edit game* page after the first
  push — neither happens automatically from the channel name.
- **HTML5 build loads a blank page or 403s.** The upload needs `index.html` at its root and
  must stay within itch.io's limits: at most 1,000 files, 500 MB extracted, 200 MB per file,
  240 characters per path. The CDN is case-sensitive, serves the game from a subfolder (so
  paths starting with `/` break — use relative paths), returns 403 for folder URLs, and only
  allows HTTPS requests to other domains. HTML5 pages take payment only as donations; sell a
  web game by making the page *Downloadable*.
- **`invalid target (bad user)` / `(bad game)`.** The target must match the page address
  exactly — subdomain for the user, URL slug for the game, all lowercase — and the page must
  exist already.
- **macOS `.app` loses its structure.** Push the `.app` folder itself (or the folder that
  contains it); butler keeps the bundle as the top-level directory and marks Mac/Linux
  executables as executable by default.
- **`--hidden` on an existing channel errors.** It only applies when the push *creates* a new
  channel. Unhide later from *Edit game*.
- **Channel typos make duplicate slots.** `windows` and `win-final` are different channels and
  create separate downloads. Decide your channel names up front and reuse them.
- **30 GB cap.** itch.io rejects builds whose total *uncompressed* size exceeds 30 GB.
- **Paid page delisted or payouts frozen.** Selling requires following the payment
  processors' rules (itch.io's creator FAQ lists themes card networks will not process), and
  adult content must be classified as such. Check before setting a price.
- **Secrets in CI logs.** A `BUTLER_API_KEY` printed in a public log is compromised — revoke
  it immediately on the API keys page. See the reference for safe CI usage.

## References

- For CI/CD (GitHub Actions/GitLab) with `BUTLER_API_KEY`, automated install via `broth`, the
  full flag list, and the update-check API, read `references/butler-ci.md`.
- Primary docs: the butler manual — `itch.io/docs/butler` (installing, login, pushing);
  itch.io creator docs — `itch.io/docs/creators/html5` (web build limits) and
  `itch.io/docs/creators/quality-guidelines` (tagging, AI disclosure, delisting rules).

## Related skills

- `steam-publish` — the same game on Steam via SteamPipe (often shipped alongside itch.io).
- `game-jam` — most jams are hosted on itch.io; this skill handles the upload step.
- `prototype-fast` — share an early prototype on a Draft/restricted itch page for playtesting.


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
