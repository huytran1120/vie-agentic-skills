---
name: navigation-3
description: >-
  Learn how to install and migrate to Jetpack Navigation 3, and how to implement features and patterns such as deep links, multiple backstacks, scenes (dialogs, bottom sheets, list-detail, two-pane, supporting pane), conditional navigation (such as logged-in navigation versus anonymous), returning results from flows, integration with Hilt, ViewModel, Kotlin, and view interoperability.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-10-22'
  keywords:
  - recipe
  - Android
  - Navigation 2
  - Navigation 3
  - migration
  - Compose
  - guide
  - dependencies
  - NavKey
  - NavHost
  - NavDisplay
  - BottomSheet
  - list-detail
  - scenes
  - two-pane
  - supporting pane
  - multiple backstacks
  - dialog
  - Hilt
  - ViewModel
  - View interop.
---

*** ** * ** ***

## Migration guide

- *[Navigation 2 to Navigation 3 migration guide](references/android/guide/navigation/navigation-3/migration-guide.md)*: Step-by-step guide to migrate an Android application from Navigation 2 to Navigation 3, covering dependency updates, route changes, state management, and UI component replacements.

### Requirements

- *[Guide: Migrate to type-safe navigation in Compose](references/android/guide/navigation/type-safe-destinations.md)* : Step-by-step guide to migrating an Android application from string-based navigation to **Type-Safe Navigation** in Jetpack Compose using Jetpack Navigation 2.

## Developer documentation

- *[Navigation 3](references/android/guide/navigation/navigation-3/index.md)*. Search documentation for more information on basics, saving and managing navigation state, modularizing navigation code, creating custom layouts using Scenes, animating between destinations, or applying logic or wrappers to destinations.

## Recipes

Code examples showcasing common patterns.

### Basic API usage

- *[Basic](references/android/guide/navigation/navigation-3/recipes/basic.md)*: Shows most basic API usage.
- *[Saveable back stack](references/android/guide/navigation/navigation-3/recipes/basicsaveable.md)*: Shows basic API usage with a persistent back stack.
- *[Entry provider DSL](references/android/guide/navigation/navigation-3/recipes/basicdsl.md)*: Shows basic API usage using the entryProvider DSL.

### Common UI

- *[Common UI](references/android/guide/navigation/navigation-3/recipes/common-ui.md)*: Demonstrates how to implement a common navigation UI pattern with a bottom navigation bar and multiple back stacks, where each tab in the navigation bar has its own navigation history.

### Deep links

- *[Static URI](references/android/guide/navigation/navigation-3/recipes/deeplinks-staticuri.md)*: Shows how to handle simple static URI deep links.
- *[URI with Arguments](references/android/guide/navigation/navigation-3/recipes/deeplinks-uriarguments.md)*: Shows how to parse path and query arguments from a deep link.
- *[Synthetic BackStack](references/android/guide/navigation/navigation-3/recipes/deeplinks-syntheticbackstack.md)*: Shows how to handle deep links with a synthetic back stack.
- *[Custom Matcher](references/android/guide/navigation/navigation-3/recipes/deeplinks-custommatcher.md)*: Shows how to implement custom deep link matching logic.

### Scenes

#### Use built-in Scenes

- *[Dialog](references/android/guide/navigation/navigation-3/recipes/dialog.md)*: Shows how to create a Dialog.

#### Create custom Scenes

- *[BottomSheet](references/android/guide/navigation/navigation-3/recipes/bottomsheet.md)*: Shows how to create a BottomSheet destination.
- *[List-Detail Scene](references/android/guide/navigation/navigation-3/recipes/scenes-listdetail.md)*: Demonstrates how to implement adaptive list-detail layouts using the Navigation 3 Scenes API.
- *[Two pane Scene](references/android/guide/navigation/navigation-3/recipes/scenes-twopane.md)*: Demonstrates how to implement adaptive two-pane layouts using the Navigation 3 Scenes API.

### Material Adaptive

- *[Material List-Detail](references/android/guide/navigation/navigation-3/recipes/material-listdetail.md)*: Demonstrates how to implement an adaptive list-detail layout using Material 3 Adaptive.
- *[Material Supporting Pane](references/android/guide/navigation/navigation-3/recipes/material-supportingpane.md)*: Demonstrates how to implement an adaptive supporting pane layout using Material 3 Adaptive.

### Animations

- *[Animations](references/android/guide/navigation/navigation-3/recipes/animations.md)*: Shows how to override the default animations for all destinations and a single destination.
- *[Conditional Transitions](references/android/guide/navigation/navigation-3/recipes/conditional-transitions.md)*: Shows how to implement conditional transition animations.

### Common back stack behavior

- *[Multiple back stacks](references/android/guide/navigation/navigation-3/recipes/multiple-backstacks.md)*: Shows how to create multiple top level routes, each with its own back stack. Top level routes are displayed in a navigation bar allowing users to switch between them. State is retained for each top level route, and the navigation state persists config changes and process death.

### Conditional navigation

- *[Conditional navigation](references/android/guide/navigation/navigation-3/recipes/conditional.md)*: Switch to a different navigation flow when a condition is met. For example, for authentication or first-time user onboarding.

### Lifecycle

- *[Lifecycle Owner](references/android/guide/navigation/navigation-3/recipes/lifecycle-owner.md)*: Shows how to use and observe Lifecycle in Navigation 3.

### Architecture

- *[Modularized navigation code (Hilt)](references/android/guide/navigation/navigation-3/recipes/modular-hilt.md)*: Demonstrates how to decouple navigation code into separate modules using Hilt or Dagger for DI.
- *[Modularized navigation code (Koin)](references/android/guide/navigation/navigation-3/recipes/modular-koin.md)*: Demonstrates how to decouple navigation code into separate modules using Koin for DI.

### Working with ViewModel

#### Passing navigation arguments

- *[Basic ViewModel](references/android/guide/navigation/navigation-3/recipes/passingarguments.md)* : Navigation arguments are passed to a `ViewModel` constructed using `viewModel()`

### Returning results

- *[Returning Results as Events](references/android/guide/navigation/navigation-3/recipes/results-event.md)* : Returning results as events to content in another `NavEntry`
- *[Returning Results as State](references/android/guide/navigation/navigation-3/recipes/results-state.md)* : Returning results as state stored in a `CompositionLocal`


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
