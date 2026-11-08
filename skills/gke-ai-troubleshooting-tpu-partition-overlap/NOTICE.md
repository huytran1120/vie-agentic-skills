# Notices

`gke-ai-troubleshooting-tpu-partition-overlap` is imported from [google/skills](https://github.com/google/skills) at revision `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee` (`skills/cloud/gke-ai-troubleshooting-tpu-partition-overlap/SKILL.md`) under the Apache License 2.0 (Copyright 2026 Google LLC); see `LICENSE`.

## Purpose & Prerequisites

- Diagnose and resolve GKE TPU slice creation failures (SliceCreationFailed) caused by partition overlap conflicts where requested TPU partitions or their nodes are already used by a...
- Official Agent Skills developed by Google for Google Cloud, AI, and developer workflows.
- Standalone execution: runbooks, scripts, and references are self-contained.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No processes are executed, no external dependencies or runtimes are installed, and no cloud accounts or credentials are connected during installation.
