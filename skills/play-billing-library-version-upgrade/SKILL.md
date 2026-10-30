---
name: play-billing-library-version-upgrade
description: >-
  Use this skill when upgrading or migrating an Android project from any legacy Google Play Billing Library (PBL) version to the latest stable version of PBL.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-10-06'
  keywords:
  - android
  - play billing
  - play billing library
  - pbl
  - upgrade
  - migration
  - deprecation
  - google play
---

## Phase 0: Intent Message

**Reporting Action**: Before proceeding, immediately tell the user: "I will
upgrade Play Billing Library to the latest version."

## Phase 1: Discovery \& Situational Awareness

1. **Primary Check (Build Version)** : Locate the project's billing dependency (e.g., `com.android.billingclient:billing`) in `build.gradle`, `build.gradle.kts`, or `libs.versions.toml`.
2. **Initial Compilation Test**: Attempt to sync and build the project immediately.
3. **Fallback Discovery (Effective Version)** :
   - **Trigger**: Only if the build fails immediately, scan the source code for deprecated artifacts.
   - **Logic** : The presence of deprecated APIs indicates the **"Effective
     Version"** ---defined as the version where those specific APIs were **last
     available**, not when they were introduced.
   - **Example** : If `SkuDetails` is present, treat the baseline as **PBL v7** or earlier (regardless of the version string in `build.gradle`).
4. **Identify Target \& Path** : Access the version tool or release notes to find the latest stable version and calculate a \[Direct/Stepped\] migration path based on the **Effective Version** baseline.

- **Calculate Migration Path** :
  - If the **Effective Version** is within 2 major versions of the target: Plan a **Direct Migration**.
  - If it is more than 2 major versions behind: Plan a **Stepped
    Migration**. Migrate by two major versions at a time (e.g., v4 -\> v6 -\> v8) until you are within two versions of the target.
- **Reporting Action**: Before proceeding, tell the user: "I've detected you are effectively on PBL \[Current\] and the latest is \[Target\]. I am planning a \[direct/stepped\] migration path."

## Phase 2: Contextual Document Mapping \& Planning

For every major version jump identified in your path, you **MUST** synthesize
instructions from:

- **[Migration Guide](https://developer.android.com/google/play/billing/migrate-gpblv%5BX%5D)** (where `[X]` is the target major version).
- **Release Highlights** : The "Deprecations" and "Breaking Changes" sections of the relevant [Release Notes](references/android/google/play/billing/release-notes.md).
- **Developer Documentation**: Consult your knowledge of the Google Play Billing documentation regarding the relevant features used in this app (e.g., Subscriptions, One-Time Products).
- **Develop the Plan**: Identify every specific code change required (API removals, class replacements, logic shifts) and print this out as a checklist.

## Phase 3: Instructions for Execution

*Reporting Action: For each of the following steps, give a brief explanation of
what you will be doing prior to execution, and a brief summary of what you
accomplished afterwards.*

### Step 1: SDK \& Environment Alignment

- **Action** : Update `build.gradle` to meet SDK requirements (e.g., "PBL 9 requires `compileSdk` 35").
- **Gradle Version**: Verify if the new library requires a newer Android Gradle Plugin (AGP) or Kotlin version.

### Step 2: Intent-based Refactoring

Analyze the intent of the existing code rather than performing purely textual
string replacement.

- **Action** : You **MUST** follow all deprecation instructions and refactor patterns from **both** the [references/migration-logic.md](references/migration-logic.md) section, the official migration guides, and the general documentation pages identified in Phase 2.
- **Verification** : Verify you are doing **all steps from all documentation** and then making sure you follow the specific directions from the checklist in the references.

### Step 3: Sequential Verification (Only applicable for Stepped Migrations)

1. **Upgrade** to the first major intermediate version in your path.
2. **Run `./gradlew assembleDebug`** to verify no intermediate breaking changes were missed.
3. **Repeat** until you reach the final target version.

### Step 4: Final Validation Checklist

1. **Smart Checklist Verification**:
2. Open [references/version-checklist.md](references/version-checklist.md) and locate the **Smart Version-Specific Checklist**.
3. **Action**: For every version between your \[Detected Effective Version\] and \[Detected New Version\], verify that every item has been addressed in the code using "Find in Files" or structural analysis.
4. **Tests** : Run all unit and implementation tests (`./gradlew test`).
5. **Clean Build** : Verify the project completes a full clean build: `./gradlew clean assembleDebug`. Then, run `./gradlew sync` and `./gradlew build` so that the user can immediately test the new version manually.

## Final Report

Explain the "Why" to the developer:

- "I updated your SDK to \[Version\] because PBL \[Version\] requires it for \[Reason from docs\]."
- "I removed your custom `retryConnection()` logic because it is now handled natively by the library using `enableAutoServiceReconnection()`."
- "Successfully upgraded from PBL \[Old\] to PBL \[New\] and verified with unit tests. Based on an analysis of features in the latest library and this application's current feature set, I suggest exploring \[New Feature\] (e.g., Prepaid Plans or Installments) from the latest release because it is now available but not yet implemented."


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
