# VAS packaging and attribution

Original work: Unslop by Damir Sokolovsky ([@heydamir](https://x.com/heydamir)).
Source: https://github.com/heydamir/unslop/tree/4652254daff586ff4739849395a127b56f7f8cc7
Original revision: `4652254daff586ff4739849395a127b56f7f8cc7`.
License: CC-BY-4.0; full original text is in LICENSE, author citation in CITATION.cff.
The references and visual examples retain the author's credit and license.
Keep attribution, the source link and license in copies/adaptations; identify
later changes. VAS does not imply endorsement or relicense the upstream content.

VAS adaptation:

- Rename only the SKILL.md YAML name to `heydamir-unslop`, because the existing
  `unslop` prose-cleanup CLI skill is unrelated; both can be installed together.
- Add reversible installation, attribution, prerequisites and consent notes.
- In snapshot.mjs and story.mjs, change only the missing-Playwright diagnostic
  to approval-first setup guidance without NPX; mark each changed helper.
- Include the original top-level examples directory, LICENSE and CITATION.cff
  in the standalone payload. Reference images and helper logic remain unchanged.

Original/vendored SHA-256, Git blobs, modes and exact reversible replacements
are recorded in VAS data/unslop-import.json. No bundled code was executed and
no package, browser runtime, MCP server or service was installed/connected.
