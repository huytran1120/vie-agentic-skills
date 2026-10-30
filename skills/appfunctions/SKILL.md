---
name: appfunctions
description: >-
  Analyzes Android apps to find user workflows to expose as AppFunctions, such as creating a note, playing media, or sending a message. AI agents, voice commands, and system shortcuts then run them without opening the app UI. Generates Kotlin code with the androidx.appfunctions library, and refines KDoc and the app description so that agents choose and call functions correctly. Use this skill when discovering, implementing, documenting, testing, or upgrading AppFunctions in an Android app, including @AppFunctionDeclaration, @AppFunctionSerializable, @AppFunctionServiceEntryPoint, AppFunctionService, app_metadata.xml, appfn:instructions, adb shell cmd app_function, and legacy @AppFunction or AppFunctionConfiguration.Provider code. Don't use for building agents that call AppFunctions or for remote MCP servers.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-10-28'
  keywords:
  - AppFunctions
  - Kotlin
  - KSP
  - ADB
  - AI
  - LLM
  - MCP
---

Analyzes Android apps to identify key user workflows to expose as AppFunctions,
such as creating a note, playing media, or sending a message, for AI agents,
voice commands, and system shortcuts to run without opening the app UI.

Generates Kotlin code to expose these workflows to the Android system,
allowing agents to discover and execute them on-device.

Also refines KDoc documentation and the app description so AI agents correctly
understand and use the provided functionality.

## Prerequisites

The app must **`targetSdk 36`** or newer and use **`compileSdk 37`** or newer as
AppFunctions, part of the Android platform API, are available from Android 16
onwards.
Always use the Jetpack library because it handles backward compatibility.
Use `androidx.appfunctions:appfunctions` and the KSP compiler
`androidx.appfunctions:appfunctions-compiler`, version 1.0.0-beta01 or later.

## Workflows

This skill enables the caller to discover features that will be provided to
system agents, implement these with AppFunctions, improve function description
for agents, and use ADB commands for local evaluation and testing.

The full AppFunction development flow consists of these four steps:

- *[Step 1: Discovery](references/feature-discovery-analysis.md)*: Analyze Android codebases to identify and recommend potential AppFunctions. Use this step when a user asks to "discover AppFunctions," "find features for AI," or "analyze my app for agentic tools."
- *[Step 2: Implementation and configuration](references/implementation-configuration.md)*: Generate Kotlin implementations of AppFunctions, manage system-wide configuration, and configure build dependencies. Use this step when a user asks to "implement AppFunctions," "set up the AppFunctions framework," or "configure Hilt for AppFunctions."
- *[Step 3: KDoc refinement](references/kdoc-refinement-optimization.md)*: Optimize AppFunction KDoc and the app description for AI agents and Model Context Protocol. If a user asks to "write KDoc", "optimize for MCP", or "refactor tool descriptions for LLMs", use this step.
- *[Step 4: Testing and debugging](references/adb-interaction-testing.md)*: Provide commands to interact with AppFunctions using ADB for testing and debugging. If a user wants to "list app functions", "invoke an app function", or "verify app function registration" on a device, use this step.

When the user asks for a subset of the steps, run those steps and any step
that the critical constraints require. Then list the skipped steps and ask
whether to run them.

If they apply, you must load the following references:

- *[Context and terminology](references/context.md)*: Defines the ubiquitous language, architecture definitions, and design patterns across the AppFunctions skill suite. Load when you need to understand core architecture terminology or check the distinctions between modern and legacy AppFunctions APIs.
- *[Migration to service entry point](references/migrate-to-service-entry-point.md)* : Migrates apps on AppFunctions 1.0.0-alpha09 or lower to the `AppFunctionServiceEntryPoint` architecture from 1.0.0-alpha10, and upgrades apps to 1.0.0-beta01. Load it when a user asks to migrate or upgrade existing AppFunctions code. When you find legacy `AppFunctionConfiguration.Provider` implementations, `@AppFunction` annotations, or `appfn:description` attributes, load it and ask the user before you migrate.

## Critical constraints

- **Modular consistency**: You must refine KDocs immediately after you generate AppFunction implementations.
- **Security**: Expose only safe, non-destructive tasks that the app's UI already offers on that form factor. Never give agents wide-ranging access to user data or system resources. Never require or return passwords, financial details, private keys, or other highly sensitive personal information.
- **Descriptions**: Describe what each function does, never how an agent must behave. Put call order across functions in the app description, not in function KDoc.

## Troubleshooting

- If you encounter build-time errors such as Kotlin Symbol Processing (KSP) issues, see [Implementation and configuration](references/implementation-configuration.md).
- If you encounter runtime errors such as missing services or execution failures, see [Testing and debugging](references/adb-interaction-testing.md).
- If you need architecture definitions and vocabulary, see [Context and terminology](references/context.md).
- If you encounter issues when upgrading AppFunctions, such as errors on `@AppFunction`, which is no longer an annotation, see [Migration to service entry point](references/migrate-to-service-entry-point.md).


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
