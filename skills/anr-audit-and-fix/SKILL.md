---
name: anr-audit-and-fix
description: >-
  Audits Android codebases for ANR risks and diagnoses ANR stack dumps. Use this skill when scanning Android code for ANR risks or triaging ANR stack dumps. Don't use for non-ANR crashes, dropped frames, general CPU profiling, or Perfetto system traces.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-10-16'
  keywords:
  - Android
  - ANR
  - Application Not Responding
  - responsiveness
  - main thread
  - ANR stack dump
  - Sync Barrier Leak
---

Select the execution path matching the user's request:

## 1. Path A: Static codebase ANR risk audit

When auditing source files or scanning for thread-blocking operations:

- Follow [references/risk_analysis_guide.md](references/risk_analysis_guide.md) step by step: list candidates, **prove the executing thread** (trace callers when the thread depends on them), **prove the call blocks**, then attribute and grade. Report only candidates that pass these checks; list the dismissed ones separately with a one-line reason.
- Evaluate off-main-thread mutations of attached Views not merely as crash risks (`CalledFromWrongThreadException`), but as **Sync Barrier Leak ANR** risks with their own proof (off-main execution plus an attached View).

## 2. Path B: Trace-driven diagnosis and remediation

When analyzing ANR traces or stack dumps:

- Diagnose systematically using [references/trace_analysis_guide.md](references/trace_analysis_guide.md) and format the report with [references/anr_trace_report_template.md](references/anr_trace_report_template.md).
- Base findings strictly on log evidence. Propose application fixes **only** for `APP_DEFECT` or `APP_RESOURCE_OVERLOAD` (never for `EXTERNAL_BOTTLENECK`).


## VAS installation notes

Distributed from android/skills at
`6daa53ef27fa2aa87827d183a85c06cedceca833` under Apache-2.0, by Google LLC and
the Android Open Source Project. Original copyright headers are retained and
the complete upstream LICENSE.txt is included with every standalone skill.
Only the frontmatter description/license formatting and these VAS notes differ;
the original workflow and all supporting files are preserved.

Use the VAS website's Copy Agent Prompt or `./vas install <skill-id> --target <agent>`
with VAS's existing agent-folder mapping. Installing this skill only copies or
links its files and writes the CLI-compatible receipt. It does not install or
update Android CLI, SDK, Gradle, JDK, Python packages, plugins, MCP servers,
models or native binaries, connect to devices/services, run bundled helpers,
collect traces or send app source, credentials or application data.

Before using a workflow, check the project's compatible SDK/JDK/Gradle/library
versions and any required device, emulator, preview access or account. External
documentation, libraries, model weights and services are not bundled snapshots
and may have separate terms. Obtain explicit permission before downloads,
installer execution, package installation, telemetry, network requests, device
changes, sensitive-data processing or paid operations. Review downloaded code
and its provenance before execution; never pipe a network installer into a shell.
Surface missing prerequisites and command failures rather than inventing results.

The r8-analyzer protobuf converter needs a compatible google.protobuf runtime
(the bundled generated module declares version 6.33.4); this dependency is not
installed automatically. Its keep_radius_pb2.py helper is bundled locally.
play-policy-insights includes its scanner, scraper and template_engine helpers;
scraping Play Store pages requires network access and consent, and its report
is assistance, not a guarantee of Google Play approval or legal compliance.
android-profiler includes the upstream Perfetto Python launcher, not native
Perfetto binaries: running it can download/cache and execute a platform binary.
Review its pinned URL/hash and cache destination before approving execution.
Keep upstream executable permissions; the launcher is non-executable upstream
and can be invoked with python3 only after approval. No helpers were run and
no runtime packages or external binaries were installed during this import.
