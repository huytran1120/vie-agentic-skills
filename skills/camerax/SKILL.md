---
name: camerax
description: >-
  Provide technical guidance for Android camera development with CameraX. Use when implementing camera features, handling asynchronous recording lifecycles, wiring low-level hardware interop using CameraX, or integrating ML Kit or Media3 effects.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-10-08'
  keywords:
  - recipe
  - Android
  - Camera
  - Camera1
  - Camera2
  - CameraX
  - migration
  - Compose
  - guide
  - dependencies
  - PreviewView
  - CameraXViewfinder
  - ImageCapture
  - VideoCapture
  - ImageAnalysis.
---

This skill provides procedural guidance and standard patterns for building
camera applications on Android, with a focus on CameraX, including its
`Camera2Interop` utilities, and Media3 integrations.

## Core workflows

### Handling immutable API patterns

Various Android camera and media APIs, especially CameraX `VideoCapture`, use a
**fluent, immutable builder-like pattern** where methods return a new instance.
Failing to reassign these results in settings, such as audio, being ignored.

**Pattern: Reassignment is required**


```kotlin
// WRONG
run {
  val pending = recorder.prepareRecording(context, opts)
  pending.withAudioEnabled() // This returns a new instance which is ignored
  val active = pending.start(exec, listener)
}

// CORRECT
run {
  val pending = recorder.prepareRecording(context, opts)
      .withAudioEnabled() // Chaining works
  val active = pending.start(exec, listener)
}

// ALSO CORRECT
run {
  var pending = recorder.prepareRecording(context, opts)
  pending = pending.withAudioEnabled() // Reassignment
  val active = pending.start(exec, listener)
}
```

<br />

See [immutability](references/immutability.md) for a list of affected classes.

### Migrating to CameraX

When migrating legacy camera codebases to the CameraX Jetpack library:

- **Camera1 to CameraX** : For migrating legacy `android.hardware.Camera` implementations, surface handling, and manual lifecycles, see the [Camera1 migration guide](references/camera1-to-camerax.md).
- **Camera2 to CameraX** : For migrating more recent but verbose `android.hardware.camera2` implementations, session state callbacks, and interop patterns, see the [Camera2 migration guide](references/camera2-to-camerax.md).

### Comprehensive feature blueprinting

For multi-step features that involve multiple files and hardware-level wiring,
follow the [Structural Blueprinting](references/expert-blueprints.md) approach to avoid
system timeouts. Such complex features include:

- **Manual controls** : Break down into the `ViewModel` state, the controller layer, and the `Camera2Interop` wiring in the session.
- **RAW capture**: Separate JPEG and RAW output configurations into discrete build steps.
- **Custom effects** : Prefer `Media3Effect` or `SurfaceProcessor` over manual OpenGL pipelines unless absolute performance is required.
- **Low-light** : See [low-light](references/low-light.md) for Night Mode and LLB guidance.
- **Foldables** : See [foldables](references/foldables.md) for handling dynamic postures and hinge states.
- **XR, AR, and VR** : See [xr](references/xr.md) for spatial tracking, passthrough synchronization, and latency guardrails.
- **Thermals and power** : See [thermals](references/thermals.md) for managing `StreamUseCase` optimizations and `PowerManager` thermal states.
- **Testing and mocking** : See [testing](references/testing.md) for using `FakeCameraConfig`, handling asynchronous lifecycles, and validating analysis pipelines.
- **ML Kit spatial analysis** : See [mlkit-spatial](references/mlkit-spatial.md) for coordinate mapping, rotation logic, and mirrored lens handling.
- **Wear OS camera remote** : See [wear-os](references/wear-os.md) for circular UI constraints, Data Layer API syncing, and remote trigger logic.

See [expert-blueprints](references/expert-blueprints.md) for step-by-step guides.

### API discovery

Always use higher-level abstractions instead of low-level manual wiring:

- **Analysis** : Use `MlKitAnalyzer` instead of manual `ImageAnalysis.Analyzer`.
- **Filters and effects** : Use `Media3Effect` for standard post-processing.
- **Multi-camera** : Use `ConcurrentCamera` APIs for dual-stream setups.

See [modern-apis](references/modern-apis.md) for current recommendations.

### Code quality and architectural rules

Adhere to the following Android ecosystem standard patterns when building your
camera implementations:

- **Testing, fakes over mocks** : Avoid mocking libraries like `Mockito`, especially for multi-step CameraX interfaces like `ImageProxy`. Build "Fakes" to verify state rather than unreliable implementation details.
- **Google Truth assertions** : Use `assertThat` over standard `JUnit` assertions like `assertEquals` for improved readability.
- **Explicit test runners** : Always define an explicit `@RunWith` for test classes to ensure the CI environment executes them correctly.
- **Semantic UI merging** : When building custom camera controls in Compose, such as a button with an `Icon` and `Text`, use `semantics {
  mergeDescendants = true }` to ensure screen readers announce them as a single, coherent unit.

## Hardware and device diversity

Camera apps run on a wide variety of hardware, from mobile phones and
foldables to tablets, laptops, and even smart appliances. Have consideration
for the specific hardware the app is running on.

- **Form factors**: Account for screen size and orientation changes on foldables and tablets.
- **Multi-camera arrays**: Some devices have a rear-facing camera and a front-facing camera. Other devices have multiple rear-facing cameras, such as wide-angle and telephoto lenses.
- **Feature parity**: Features like flash or auto-focus behave differently across hardware. For example, CameraX handles both physical flash, back, and screen-based flash, front, and both must be considered when implementing flash functionality.

## Common pitfalls

- **Asynchronous lifecycles** : Check `isRecording` state before attempting to stop or pause. Handle `VideoRecordEvent.Start` for UI state updates, not just the initial call.
- **Thread safety**: Camera callbacks often run on background executors. Dispatch UI updates on the main thread.
- **Permission handling** : Check `CAMERA` permission; check for `RECORD_AUDIO` specifically when enabling audio in `VideoCapture`.


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
