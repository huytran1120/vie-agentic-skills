---
name: projected-hardware
description: >-
  Provides instructions and workflows for accessing and managing hardware on Android XR projected devices, such as audio glasses and display glasses. Use this skill when building experiences for intelligent eyewear in an Android app and you need to access device hardware like the camera and microphone, handle glasses-specific runtime permissions, or manage connection lifecycles using projected context.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-10-17'
  keywords:
  - Android XR
  - intelligent eyewear
  - audio glasses
  - display glasses
  - glasses hardware
  - ProjectedContext
  - projected context
  - runtime permissions
  - CameraX
  - audio recording
---

## Prerequisites

- You must use a `compileSdk` of 36 or higher.

## Connection and lifecycle management

Intelligent eyewear hardware is only accessible while the glasses are connected
to the host phone. Monitor connection state and manage resource lifecycles using
`ProjectedContext`. You must read
[Understand projected activities and projected contexts](references/android/develop/xr/jetpack-xr-sdk/glasses/support-different-types.md) to understand
how to get a projected context and [how to manage its lifecycle](references/android/develop/xr/jetpack-xr-sdk/glasses/check-availability.md).

## Request glasses hardware permissions

- **Hardware permissions and opt-in** : You must read [Request hardware permissions](references/android/develop/xr/jetpack-xr-sdk/request-hardware-permissions.md) to understand how to declare camera and microphone runtime permissions in the Android Manifest file, request runtime permissions in different scenarios, and handle permission results.

## Glasses hardware access and capabilities

- **Camera capture and CameraX** : You must read [Capture an image with the glasses' camera](references/android/develop/xr/jetpack-xr-sdk/access-hardware-projected-context.md) to understand the implementation patterns for capturing a photo with the glasses' camera using a `ProjectedContext`.


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
