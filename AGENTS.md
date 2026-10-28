# Vie Agentic Skill (VAS) - Instructions for AI Agents

This is **Vie Agentic Skill (VAS)**, a local adaptation of the upstream catalog curated by **Huy Tran** (`huytran1120`).
It serves as a comprehensive catalog of 2,951+ modular, agentic skills designed for **Google Antigravity, Claude Code, Cursor, Windsurf (Codeium), OpenAI Codex / OpenCode, Cline / Roo Code, and GitHub Copilot CLI**.

The upstream snapshot is `8dd77cd14fea84ad3a9f51573461a227ae06082e` from
https://github.com/huytran1120/vietnam-agentic-skills. Keep individual skill
licenses and notices. The `pdf`, `docx`, `pptx`, `xlsx` runbooks are independently
authored replacements under MIT; do not restore the restricted upstream versions
or their scripts/assets. Old full-text distribution dumps were not imported.

Preview from the project root using `python3 -m http.server 8765 --bind 127.0.0.1`
and open `http://127.0.0.1:8765/docs/`. Local runbook links require serving the
project root, not just `docs/`. The project repository is
https://github.com/huytran1120/vie-agentic-skills. No public website deployment is configured.

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
  - Cline / Roo Code: `./vas install <skill_id> --target cline --mode link`
  - GitHub Copilot CLI: `./vas install <skill_id> --target copilot --mode link`
  - All Agents: `./vas install <skill_id> --target all`
- **To view status**:
  `./vas status --target <agent>`
- **To rebuild index after adding new skills**:
  `./vas sync`
