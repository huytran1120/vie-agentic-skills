# Vie Agentic Skill (VAS) - Instructions for AI Agents

This is **Vie Agentic Skill (VAS)**, a local adaptation of the upstream catalog curated by **Huy Tran** (`huytran1120`).
It serves as a comprehensive catalog of 3,045+ modular, agentic skills designed for **Google Antigravity, Claude Code, Cursor, Windsurf (Codeium), OpenAI Codex, Cline, and GitHub Copilot CLI**. OpenCode and Roo Code can use the shared `.agents/skills/` directory via `--target workspace`; their native discovery directories differ from Codex and Cline.

The upstream snapshot is `8dd77cd14fea84ad3a9f51573461a227ae06082e` from
https://github.com/huytran1120/vietnam-agentic-skills. Keep individual skill
licenses and notices. The `pdf`, `docx`, `pptx`, `xlsx` runbooks are independently
authored replacements under MIT; do not restore the restricted upstream versions
or their scripts/assets. Old full-text distribution dumps were not imported.

Preview from the project root using `python3 -m http.server 8765 --bind 127.0.0.1`
and open `http://127.0.0.1:8765/docs/`. Local runbook links require serving the
project root, not just `docs/`. The project repository is
https://github.com/huytran1120/vie-agentic-skills. The primary public website is
https://vie-agentic-skills.vercel.app/, built with `vercel.json`. UX, UI, content,
and SEO improvements target this primary website. GitHub Pages remains available at
https://huytran1120.github.io/vie-agentic-skills/ as its last published version.
It is frozen: the Pages deployment workflow has been removed. Do not update,
redirect, republish, or unpublish that site unless the user explicitly requests it.
All ongoing website development and deployment target Vercel.

## Vercel publication budget

- After adding assets or importing skills, run `python3 scripts/build_pages.py`.
- The normal build and CI use `vercel-budget.json`: warn at 1,000,000,000 bytes and fail above 1,500,000,000 bytes.
- These are project operating budgets, not Vercel provider limits. Keep `0 < warning_bytes < max_bytes`; do not remove the guard to make a large import pass.
- The budget counts every published file in `_site/`, including runbooks, assets, and generated manifests. It does not measure first-page transfer size, repository size, build cache, or the team's retained Deployment Storage.
- Before raising the budget or importing a large asset collection, check the Vercel team's actual Deployment Storage usage and retained deployments. Hobby's published 10 GB allowance applies across retained deployments at team level, not to each website. Recheck the current plan and [official storage guidance](https://vercel.com/docs/deployment-storage).
- Keep deployments on the configured GitHub-to-Vercel integration. The [CLI upload limit](https://vercel.com/docs/limits#static-file-uploads) is a different limit from generated build output.
- `pages-budget.json` is retained only as a legacy reference (850 MB warning / 900 MB maximum); it does not constrain Vercel or trigger Pages publication. GitHub Pages remains frozen.
- CI validates the full Vercel build and its budget on pull requests and pushes to the main branches. Build logs show the five largest directories.

## Vercel UX/UI regression rules

- Preserve the approved light/dark palette, system font stacks, hero wordmark, agent reel and decorative motion unless the user requests a design change. The baseline is `tests/fixtures/ui-contract.json`; never change it just to make a regression pass.
- Keep the homepage order: hero → catalog/search → work categories → selected guides → quickstart → FAQ/sources. Search and the skill library remain primary; full articles belong under `/blog/`.
- Keep working native links, exact canonical skill IDs, language/agent context, browser Back/Forward, reader fragments and return focus. Use the existing agent directory mapping and installation prompt generator.
- Support 320, 390, 768, 1024 and 1440 px widths in Vietnamese and English. Do not introduce horizontal overflow, overlapping controls, hidden primary actions, or content that stays invisible with reduced motion. Preserve visible keyboard focus and accessible control names.
- New blog articles need real static HTML, an index entry, sitemap/canonical metadata and valid skill links. Stage the intended article files before the final preflight; untracked drafts from other tasks are not release candidates.
- Before pushing a website change, run `python3 scripts/verify_vercel_ui.py`. It requires Node.js and Chrome/Chromium, builds the artifact and fails rather than silently skipping the browser checks. Run the full repository checks when CLI, catalog or import data also change.
- For visible UX/UI changes, compare a local demo or Vercel preview before production, including desktop/mobile screenshots, both themes/languages, keyboard navigation and native theme motion. Follow [the verification checklist](docs/vercel-ui-verification.md); automated geometry checks do not replace visual review.
- Review the intended staged/committed snapshot and preserve unrelated work. After publishing, verify the exact commit, deployment status, public catalog/Blog/runbook and install manifest; report any unverified part.
- Vercel's build runs the fast catalog/design-contract tests before building. Full browser checks run locally and in GitHub CI; the Git integration does not wait for GitHub CI automatically. Do not claim that a green deployment proves all UI checks passed.
- Keep GitHub Pages frozen and retain the Vercel publication budget above. Do not restore Pages deployment or weaken the budget/tests to publish a failing change.
- Keep Web Analytics centralized in the Vercel build (`VERCEL=1`), after asset versioning. Preserve the `beforeSend` URL redaction in `docs/analytics.js`, Vercel's dynamic intake routes and automatic pageviews; do not add duplicate snippets to individual articles or collect form values/custom installation paths.

## Golden Rules for Agents

1. **Zero NPX / Zero External Dependencies**:
   - Never run `npx` or prompt the user to run `npx`.
   - All management, searching, listing, and installing must be performed using `./vas` or `python3 vas.py`.
2. **Progressive Disclosure**:
   - Do NOT dump thousands of full files into prompt context.
   - Use `./vas install <skill_id> --target <agent> --mode link` to install only the necessary skills.
   - AI Agents scan the YAML frontmatter (`name`, `description`) of installed skills and load full instructions on-demand.
3. **Skill Structure**:
   Every skill inside `skills/<skill_name>/` follows the Open Agent Skills specification (`agentskills.io`):
   ```text
   skills/<skill_name>/
   ├── SKILL.md          # Required: Frontmatter (name, description, category, tags) + Runbook
   ├── scripts/          # Optional: Helper scripts (bash, python)
   ├── examples/         # Optional: Example inputs/outputs
   └── references/       # Optional: In-depth specifications and reference material
   ```

## Agent Runbook

- **To search for a skill**:
  `./vas search <keyword>`
- **To view a skill**:
  `./vas show <skill_id>`
- **To install into the current workspace**:
  - Antigravity / Universal: `./vas install <skill_id> --target antigravity --mode link`
  - OpenAI Codex: `./vas install <skill_id> --target codex --mode link`
  - Claude Code: `./vas install <skill_id> --target claude --mode link`
  - Cursor: `./vas install <skill_id> --target cursor --mode link`
  - Windsurf: `./vas install <skill_id> --target windsurf --mode link`
  - Cline: `./vas install <skill_id> --target cline --mode link`
  - OpenCode / Roo Code (universal directory): `./vas install <skill_id> --target workspace --mode link`
  - GitHub Copilot CLI: `./vas install <skill_id> --target copilot --mode link`
  - All Agents: `./vas install <skill_id> --target all`
- **To view status**:
  `./vas status --target <agent>`
- **To rebuild index after adding new skills**:
  `./vas sync`
