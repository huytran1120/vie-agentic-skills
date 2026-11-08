# Notices

`cloud-armor-crs-rule-upgrader` is imported from [google/skills](https://github.com/google/skills) at revision `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee` (`skills/cloud/cloud-armor-crs-rule-upgrader/SKILL.md`) under the Apache License 2.0 (Copyright 2026 Google LLC); see `LICENSE`.

## Purpose & Prerequisites

- Upgrades Google Cloud Armor security policies from OWASP CRS 3.0 and 3.3 to OWASP CRS 4.22. Preserves signature opt-in and opt-out lists, translates evaluatePreconfiguredExpr to na...
- Official Agent Skills developed by Google for Google Cloud, AI, and developer workflows.
- Standalone execution: runbooks, scripts, and references are self-contained.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No processes are executed, no external dependencies or runtimes are installed, and no cloud accounts or credentials are connected during installation.
