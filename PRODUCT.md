# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Developers using AI coding agents who need to discover a relevant runbook, inspect
its origin and requirements, and install it into their chosen agent.

## Product Purpose

Vie Agentic Skill is a searchable, multi-agent skill library with a local,
dependency-free Python manager. Success means finding an applicable skill,
understanding its constraints and copying an Agent Chat installation prompt or
a correct CLI command.

## Operating Context

The public repository is https://github.com/huytran1120/vie-agentic-skills.
The user requested publishing GitHub Pages and subsequently selected
https://chen08209.github.io/FlClash/ and its repository as the visual reference.
Use its warm palette, large typography and numbered sections as design cues,
with an original implementation for the VAS catalog.
Motion also follows this reference: an interactive capsule field, rolling agent
names, staggered entrances and scroll reveals, navigation hover and a theme wipe.
Decorative motion must respect reduced-motion preferences, pause the field when
offscreen or hidden, and never change the selected installation agent by itself.
The CLI remains `./vas`; individual task dependencies are not CLI dependencies.

## Capabilities and Constraints

- Preserve search, category filters, sorting, list/grid views, shared links,
  source/license information, explicit target agents and project/global scope.
- The website generates prompts and commands; it never installs software into a visitor's machine.
- Copy Agent Prompt targets the selected agent in the current project, without
  cloning VAS or requiring the CLI, Python or an absolute project path. Static
  per-skill manifests inventory all support files and immutable catalog-commit
  URLs with byte sizes, hashes, executable flags and compatible CLI receipts.
  Agents must check completeness, skip matching installations and ask before
  conflicting contents or identities are replaced. Downloaded tools are not run
  automatically; network/file permissions and individual prerequisites still apply.
- Quick installation and CLI installation are distinct. Global scope and
  link/copy controls affect only the CLI; quick `all` means seven current-project
  destinations. Both the install prompt and post-install usage prompt are localized.
- Preserve the existing library and independently authored document runbooks.
- Imported content retains its own licenses, support files and provenance.
- The YouTube collection includes 11 MIT runbooks and six Python helpers from
  Jakeschincariol/youtube-agent-skill. Each skill ships its helper dependencies
  and voice template for standalone installation; it does not connect accounts
  or publish videos automatically.
- Blender skills require a separately configured Blender MCP connection. Importing
  runbooks does not install or activate that connection.
- Hallmark is one MIT frontend skill with 50 bundled themes and optional Node.js
  helpers. Browser helpers need separately provided Chrome and Puppeteer; paid
  Together AI generation and individually licensed photos remain opt-in.
- TypeSafe is one MIT integration runbook with its license and live-doc links.
  API access, server-side keys, SDKs and paid probes are separate from installation;
  probes require permission, data disclosure and a budget.
- Android includes 35 Apache-2.0 skills with complete references, samples and
  local helpers; the existing android-cli stays unchanged. SDKs, optional protobuf,
  Perfetto binary downloads, devices and network operations require separate setup
  and permission, not automatic execution during installation.
- GameDev includes 77 specialized skills plus a standalone router under Apache-2.0.
  The router bundles read-only companion payloads without duplicate catalog entries.
  Two distinct name collisions use gamedev- folders. Engines, Pillow, platform
  accounts, asset generation and publishing remain separately authorized prerequisites.
- GitHub Pages is static and must work under the repository URL prefix.
- Shared links use a branded 1280-by-640 PNG with matching Open Graph and Twitter
  metadata. GitHub repository previews require a separate upload in Settings >
  Social preview; website metadata cannot change GitHub's repository card.
- The header's EN/VI button switches the complete interface between Vietnamese
  and English without resetting search, filters or installation settings.
  Vietnamese is the default; `?lang=vi` or `?lang=en` overrides the saved browser
  preference and is included in shared links. Only the language preference is
  saved, never local project paths. Runbooks and source metadata retain their
  original language; CLI commands are identical in both modes.
- Do not invent download counts, popularity, customer claims or safety guarantees.

## Brand Commitments

Keep the Vie Agentic Skill identity and Vietnamese-first interface. Adapt the
FlClash layout to skill discovery, technical documentation and installation.

## Evidence on Hand

The catalog and actual skill files provide skill/category counts. The Blender
source provides 94 MIT-licensed runbooks, their references and a credited render.

## Product Principles

- Make a working library, not a promotional dead end.
- Explain prerequisites before execution and show provenance.
- Keep local use and the published site consistent.
- Preserve users' local paths: never put installation paths in shared URLs.

## Open Decisions and Inferences

The latest request covers the whole catalog. Blender remains a featured
collection alongside other technical domains. No commercial positioning or new
supported agent is inferred.
