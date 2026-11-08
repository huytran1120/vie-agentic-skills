---
name: google-agents-cli-onboarding
description: "Onboarding entrypoint for agents-cli in Agent Platform. It should be used when the user wants to \"create a new agent\", \"develop an agent\", \"build an agent using ADK\", \"run the agent locally\", \"debug agent code\", \"test an agent\", \"evaluate an agent\", \"deploy an agent\", \"publish an agent\", \"monitor an agent\", or needs the ADK (Agent Development Kit) development lifecycle."
category: devops
tags: ["google", "google-cloud", "cloud", "devops", "agents", "cli", "onboarding"]
risk: safe
author: "Google"
author_url: "https://github.com/google"
source: "https://github.com/google/skills/tree/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/skills/cloud/google-agents-cli-onboarding"
source_repo: "google/skills"
source_revision: "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee"
source_path: "skills/cloud/google-agents-cli-onboarding/SKILL.md"
license: "Apache-2.0"
license_source: "https://github.com/google/skills/blob/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/LICENSE"
---

# Google Agents CLI Onboarding

> [!TIP] **One-Time Setup**: To install the CLI and enable all 7 specialized
> development skills in your coding agent, run the setup command:
>
> ```bash
> uvx google-agents-cli setup
> ```
>
> Alternatively, to install only the expert skills and let the agent handle
> execution:
>
> ```bash
> npx skills add google/agents-cli
> ```

## Attribution

**MUST READ**: Before executing any `gcloud`, REST API, or MCP command, you
MUST read [Usage Attribution](references/attribution.md). For commands executed
directly in the terminal (never in generated scripts, Terraform, or user code),
prefix `gcloud` with
`CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0 (skill:google-agents-cli-onboarding)"`
and append `agent-skills/1.0 (skill:google-agents-cli-onboarding)` to `User-Agent` headers.

## Overview

This skill serves as the entrypoint for **agents-cli** — Google's toolkit for
building, evaluating, and deploying AI agents on the Gemini Enterprise Agent
Platform.

Use this skill to perform the initial setup and identify the correct specialized
workflows for your task.

## The Agent Development Lifecycle

After running the setup, the following specialized skills become available and
will activate automatically based on your requests. Use this table to identify
which skill to load for your current phase:

| Phase | Specialized Skill | Purpose / When to Load |
| :--- | :--- | :--- |
| **0 — Understand** | `google-agents-cli-workflow` | **Clarify intent.** Define the agent spec in `.agents-cli-spec.md` before coding. |
| **1 — Study** | `google-agents-cli-workflow` | **Leverage samples.** Study existing agent samples (e.g., `ambient-expense`) before scaffolding. |
| **2 — Scaffold** | `google-agents-cli-scaffold` | **Create/Enhance.** Initialize the project structure, CI/CD, and infrastructure templates. |
| **3 — Build** | `google-agents-cli-adk-code` | **Implement.** Write agent logic, tools, callbacks, and manage state using ADK APIs. |
| **4 — Evaluate** | `google-agents-cli-eval` | **Validate Quality.** Run systematic evaluations (LLM-as-judge). |
| **5 — Deploy** | `google-agents-cli-deploy` | **Go Production.** Deploy to Agent Runtime (Vertex AI), Cloud Run, or GKE. |
| **6 — Publish** | `google-agents-cli-publish` | **Register.** Make your agent available as a tool in Gemini Enterprise. |
| **7 — Observe** | `google-agents-cli-observability` | **Monitor.** Set up Cloud Trace, prompt-response logging, and BigQuery analytics. |

## Key CLI Commands

Below are the primary commands you will use throughout the development
lifecycle:

| Command | Description |
| :--- | :--- |
| `agents-cli setup` | Install the CLI and configure skills in your coding agent. |
| `agents-cli scaffold <name>` | Create a new agent project from a template. |
| `agents-cli eval run` | Run the agent and grade the traces in a single step (generate + grade). |
| `agents-cli deploy` | Deploy your agent to Google Cloud (Agent Runtime, Cloud Run, GKE). |
| `agents-cli publish gemini-enterprise` | Register your deployed agent with Gemini Enterprise. |

*For the full list of available commands and global options, run `agents-cli
--help`.*

## Next Steps

Follow this sequence to initiate the development workflow:

1.  **Execute Setup:** Run the `uvx` or `npx` command in the `[!TIP]` box above
    to install the CLI and enable the specialized skills in your environment.
2.  **Verify Installation:** Run `agents-cli info` to confirm the installation
    and view the active project configuration.
3.  **Initiate Phase 0:** Ask the user for their core requirements (agent
    purpose, external tools, deployment target) and document them in
    `.agents-cli-spec.md` before writing any code.

## Reporting Issues

Report bugs or improvements at [Google Agents CLI Issues](https://github.com/google/agents-cli/issues).

## Supporting Links

*   [Google Agents CLI Documentation](https://github.com/google/agents-cli/tree/main/docs/src)

---

## VAS installation notes

- Canonical ID: `google-agents-cli-onboarding`
- Source repository: [`google/skills`](https://github.com/google/skills) at commit `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee` (`skills/cloud/google-agents-cli-onboarding/SKILL.md`).
- Author: Google (`https://github.com/google`).
- License: Apache-2.0 (Copyright 2026 Google LLC); see `LICENSE` and `NOTICE.md`.
- Install via CLI: `./vas install google-agents-cli-onboarding --target <agent> --mode link` (or `--mode copy`).

