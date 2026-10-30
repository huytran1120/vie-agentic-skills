---
name: agp-9-upgrade
description: >-
  Upgrades, or migrates, an Android project to use Android Gradle Plugin (AGP) version 9. Do not use this skill for migrating Kotlin Multiplatform (KMP) projects.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-09-18'
  keywords:
  - Android Gradle Plugin 9
  - AGP 9
  - AGP Upgrade
  - AGP Migration
  - New AGP DSL
  - Migrate to built-in Kotlin
---

## Migration guide

See the [AGP 9 migration guide](references/android/build/releases/agp-9-0-0-release-notes.md) for the major changes, many
breaking, in AGP 9 compared to AGP 8.

## Requirements

If the user requests to update or migrate to AGP 9, first check the AGP version
used in the project. If it is lower than 9, stop and ask the user to run the AGP
Upgrade Assistant in Android Studio to update to the latest stable version of
AGP, and confirm when done. The user may also request that this requirement be
skipped; if this is the case, you should update the version of AGP to the latest
stable version as part of the AGP 9 migration. See the
[AGP 9 migration guide](references/android/build/releases/agp-9-0-0-release-notes.md) for how to do this.

Each version of AGP has its own set of compatibilities with other tools, such as
Gradle, JDK, and Kotlin. The release notes for each of these versions will
include a **Compatibility** table indicating the minimum versions for these
tools.

Do not use this skill for KMP projects, as they are unsupported.

## Steps

If AGP is already at 9 or higher, then do the following:

### Step 1: Update dependencies

If KSP (`com.google.devtools.ksp`) is used in the project, ensure it is on
version 2.3.6 or higher.

If Hilt is used in the project, ensure it is on version 2.59.2 or higher.

### Step 2: Migrate to built-in Kotlin

See [the guide](references/android/build/migrate-to-built-in-kotlin.md) for detailed information.

### Step 3. Migrate to the new AGP DSL

See [the guide](references/android/build/releases/agp-9-0-0-release-notes.md) for detailed information.

See also [gradle-recipes](references/recipes.md) for examples on how to migrate old code to code
that is compatible with AGP 9 and the new DSL.

### Step 4. Migrate kapt to KSP or legacy-kapt

If KSP (`com.google.devtools.ksp`) or kapt (`org.jetbrains.kotlin.kapt`) are
used in the project, see [KSP, kapt, and legacy-kapt](references/ksp-kapt.md) for detailed migration
steps.

### Step 5. BuildConfig

If any Android module contains custom BuildConfig fields, see [BuildConfig](references/buildconfig.md)
for detailed information.

### Step 6. Update gradle.properties

After the migration, check gradle.properties. Remove the following flags:

1. android.builtInKotlin
2. android.newDsl
3. android.uniquePackageNames
4. android.enableAppCompileTimeRClass

Additionally, delete all temporary files you've created.

## Guidelines

- Never write or run python scripts.
- Only search the Gradle dependency cache when inspecting external dependencies, and only as a last resort.
- Never add `android.disallowKotlinSourceSets=false` to `gradle.properties`.
- When verifying changes, don't run the `clean` task. This is a waste of time.

## Verification

After migration, verify the following:

1. Gradle IDE sync succeeds.
2. `./gradlew help` succeeds.
3. `./gradlew build --dry-run` succeeds.

## Troubleshooting

Paparazzi v2.0.0-alpha04 and lower versions have issues with AGP 9. See
[references/paparazzi-gradle-9.md](references/paparazzi-gradle-9.md) for details.


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
