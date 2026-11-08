---
name: google-mobile-ads-get-started
description: "Provides instructions for integrating the Google Mobile Ads (GMA) SDK. Use this skill when the user wants to get started with, install, integrate, set up, or configure the SDK for AdMob or Ad Manager, GMA Next-Gen SDK or mobile ads framework in an Android, iOS, or Unity application."
category: marketing
tags: ["google", "google-cloud", "ads", "marketing", "mobile", "get", "started"]
risk: safe
author: "Google"
author_url: "https://github.com/google"
source: "https://github.com/google/skills/tree/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/skills/ads/google-mobile-ads-get-started"
source_repo: "google/skills"
source_revision: "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee"
source_path: "skills/ads/google-mobile-ads-get-started/SKILL.md"
license: "Apache-2.0"
license_source: "https://github.com/google/skills/blob/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/LICENSE"
---

# Google Mobile Ads SDK - Install

## Workflow

1.  **Determine the user's platform**: Identify if the project is Android, iOS,
    or Unity. If unclear, ask before proceeding.

2. **Read the platform guide** for implementation details:
    - Android: `references/android-get-started.md`
    - iOS: `references/ios-get-started.md`
    - Unity: `references/unity-get-started.md`

3. **Follow these steps in order**:
   - [ ] Add the SDK dependency
   - [ ] Set the application identifier
   - [ ] Initialize the SDK
   - [ ] Verify the integration

4. After the SDK is successfully installed, ask the user to select an ad format
   to continue the integration.

---

## VAS installation notes

- Canonical ID: `google-mobile-ads-get-started`
- Source repository: [`google/skills`](https://github.com/google/skills) at commit `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee` (`skills/ads/google-mobile-ads-get-started/SKILL.md`).
- Author: Google (`https://github.com/google`).
- License: Apache-2.0 (Copyright 2026 Google LLC); see `LICENSE` and `NOTICE.md`.
- Install via CLI: `./vas install google-mobile-ads-get-started --target <agent> --mode link` (or `--mode copy`).

