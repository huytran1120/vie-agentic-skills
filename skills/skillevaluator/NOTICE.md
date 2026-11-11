# Notice for skillevaluator

This skill payload is adapted from upstream repository [NVIDIA/SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator)
at commit revision `7ae25d2522c9c3b151111fedaa67b814cc3dc5c5`.

- Author: Christopher Kevin <christopherk@nvidia.com>
- Upstream Organization: NVIDIA Corporation & Affiliates
- Upstream License: Apache License 2.0 (see bundled LICENSE)
- Upstream Source Path: `skills/skillevaluator`
- Adapted for Vie Agentic Skill (VAS) distribution.

## Bundled Components and Provenance

- `SKILL.md`: Core runbook and Agent Skills specification for operating the SkillEvaluator CLI across Tier 1, Tier 2, and Tier 3 evaluation workflows.
- `evals/`: Evaluator dataset and configuration for self-evaluation (`config.yml`, `evals.json`).
- `references/`: Comprehensive reference runbooks for:
  - `commands-tier1.md`: Tier 1 quality, security, and rubric evaluation commands.
  - `commands-tier2-tier3.md`: Tier 2 deduplication and Tier 3 live agent evaluation commands.
  - `commands-validate.md`: Combined validation pipeline commands.
  - `custom-graders.md`: Bring-your-own-grader (BYOG) and Harbor task specifications.
  - `providers.md`: LLM provider configuration and API credentials.
  - `reports-and-ci.md`: Report formats, exit codes, and CI integration.
  - `tier3-datasets.md`: Eval dataset authoring, case structure, and Harbor task formats.
  - `tier3-running.md`: Live evaluation execution, agent selection, Docker and local sandbox modes.
  - `troubleshooting.md`: Common errors, doctor commands, and fixes.

## VAS Adaptation Notes

- Preserves upstream directory structure and standalone execution semantics.
- Appended standard VAS installation, attribution, and safety notes to `SKILL.md`.
- Mapped to existing `agent-evaluation` category to preserve the exact 119-category taxonomy.
- Managed by Vie Agentic Skill (VAS) with zero external package manager dependencies (no NPX).
