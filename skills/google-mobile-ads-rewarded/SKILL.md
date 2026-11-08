---
name: google-mobile-ads-rewarded
description: "Provides instructions for implementing, integrating, or configuring Google Mobile Ads (GMA) SDK rewarded ads in Android, iOS, or Unity mobile applications. Use when the task involves setting up rewarded ads. Don't use for \"rewarded interstitial\" ads."
category: marketing
tags: ["google", "google-cloud", "ads", "marketing", "mobile", "rewarded"]
risk: safe
author: "Google"
author_url: "https://github.com/google"
source: "https://github.com/google/skills/tree/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/skills/ads/google-mobile-ads-rewarded"
source_repo: "google/skills"
source_revision: "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee"
source_path: "skills/ads/google-mobile-ads-rewarded/SKILL.md"
license: "Apache-2.0"
license_source: "https://github.com/google/skills/blob/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/LICENSE"
---

# Google Mobile Ads SDK - Rewarded Ads

Rewarded ads reward users with in-app items for interacting with full-screen
ads. Rewarded ads are served after a user explicitly opts in to view a rewarded
ad.

## Workflow

1.  **Determine the user's platform**: Identify if the project is Android,
    iOS, or Unity. If unclear, ask before proceeding.

2.  **Read the platform guide** for implementation details:
    -   Android: `references/android-rewarded.md`
    -   iOS: `references/ios-rewarded.md`
    -   Unity: `references/unity-rewarded.md`

3.  **Follow these steps in order**:
    -   [ ] Load the ad
    -   [ ] Register for ad event callbacks
    -   [ ] Add a UI element to view the ad for a reward
    -   [ ] Show the ad
    -   [ ] Verify the implementation

---

## VAS installation notes

- Canonical ID: `google-mobile-ads-rewarded`
- Source repository: [`google/skills`](https://github.com/google/skills) at commit `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee` (`skills/ads/google-mobile-ads-rewarded/SKILL.md`).
- Author: Google (`https://github.com/google`).
- License: Apache-2.0 (Copyright 2026 Google LLC); see `LICENSE` and `NOTICE.md`.
- Install via CLI: `./vas install google-mobile-ads-rewarded --target <agent> --mode link` (or `--mode copy`).

