---
name: ima-sdk-client-side
description: "Supports Interactive Media Ads (IMA) SDK. Use this skill for client-side ad insertion when you are requesting video ads for websites, apps, TVs or other platforms using VAST or VMAP. Do not use for Dynamic Ad Insertion (DAI), SSAI, or SGAI."
category: marketing
tags: ["google", "google-cloud", "ads", "marketing", "ima", "sdk", "client", "side"]
risk: safe
author: "Google"
author_url: "https://github.com/google"
source: "https://github.com/google/skills/tree/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/skills/ads/ima-sdk-client-side"
source_repo: "google/skills"
source_revision: "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee"
source_path: "skills/ads/ima-sdk-client-side/SKILL.md"
license: "Apache-2.0"
license_source: "https://github.com/google/skills/blob/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/LICENSE"
---

# IMA SDK client-side

The Google IMA SDK (Interactive Media Ads) lets you load in-stream video and
audio ads into websites, apps, TVs and other digital platforms. Use an IMA SDK
to request ads from any VAST-compliant ad server and manage ad playback.

## Prerequisites

Before integrating the IMA SDK, you **must** read the platform-specific guide
below to support all platforms that your app can support:

*   **Web/HTML5/ReactJs/NodeJs/Angular:** Read all these guides
    [ima-sdk-web-guide.md](references/ima-sdk-web-guide.md),
    [ima-sdk-web-iframe-mode.md](references/ima-sdk-web-iframe-mode.md),
    [ima-sdk-web-mobile-safari.md](references/ima-sdk-web-mobile-safari.md)
*   **Android/AndroidTV/ReactNative:** Read [ima-sdk-android-guide.md](references/ima-sdk-android-guide.md)
*   **iOS/tvOS/ReactNative:** Read all these guides
    [ima-sdk-ios-guide.md](references/ima-sdk-ios-guide.md),
    [ima-sdk-tvos-guide.md](references/ima-sdk-tvos-guide.md)

--------------------------------------------------------------------------------

## Quick start (general workflow)

1.  Import the SDK: Prerequisites, dependencies.
2.  Initialization: Early setup, Warmup, Settings Configuration, and Ad UI
    Setup.
3.  Ad Request: Creating and triggering the request, User gesture compliance.
4.  Ad Load Success/Failure: Handling the load event to get the AdsManager, or
    handling early fatal errors.
5.  Ad Playback Events: Listening to playback events via AdsManager to
    coordinate content play/pause, and handling non-fatal LOG events and fatal
    active playback errors.
6.  Cleanup: Properly destroying the AdsManager to release resources and prevent
    memory leaks.

For detailed, platform-specific implementation details, always refer to the
guides in the Prerequisites section.

---

## VAS installation notes

- Canonical ID: `ima-sdk-client-side`
- Source repository: [`google/skills`](https://github.com/google/skills) at commit `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee` (`skills/ads/ima-sdk-client-side/SKILL.md`).
- Author: Google (`https://github.com/google`).
- License: Apache-2.0 (Copyright 2026 Google LLC); see `LICENSE` and `NOTICE.md`.
- Install via CLI: `./vas install ima-sdk-client-side --target <agent> --mode link` (or `--mode copy`).

