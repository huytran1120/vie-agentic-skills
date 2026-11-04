---
name: scrapecreators-audience-research
description: Use when the user wants to evaluate a creator, influencer, or brand audience using public profile signals, TikTok audience demographics, follower/following data, comments, geography, language, and content fit. Helps judge sponsorship and market fit.
allowed-tools: Bash, Read, Write, WebFetch

version: 1.0.0
author: ScrapeCreators
license: MIT
homepage: https://scrapecreators.com
repository: https://github.com/ScrapeCreators/social-media-research-skills
metadata:
  openclaw:
    requires:
      env:
        - SCRAPECREATORS_API_KEY
    primaryEnv: SCRAPECREATORS_API_KEY
    homepage: https://scrapecreators.com
    tags:
      - social-media
      - research
      - scrapecreators
---

# Audience Research

## Overview

Evaluate whether a creator or social account reaches the right audience. This skill combines available public profile metrics, TikTok audience demographics, regional signals, follower/following data when available, comments, language, and content topics.

## When to Use

Use this skill when the user asks to:

- check if a creator's audience fits a market
- compare audience fit across creators
- find US-heavy, country-specific, or niche-specific creators
- evaluate sponsorship/influencer opportunities
- understand who appears to engage with an account

## Useful Sources

- `/v1/tiktok/user/audience`
- `/v1/tiktok/profile/region`
- profile endpoints across platforms
- follower/following endpoints where available
- comments on recent posts
- link-in-bio pages and creator shops for niche signals

## Workflow

1. Pull profile and available audience/demographic data.
2. Pull recent content and comments if audience intent matters.
3. Extract region, language, niche, product/category, and community signals.
4. Score audience fit against the user's target market.
5. Label confidence based on the strength of public data.

## Output Format

```markdown
# Audience Research: {creator}

## Fit Summary
- Target market:
- Fit score: High/Medium/Low
- Confidence: High/Medium/Low

## Evidence
| Signal | Evidence | Source |
|---|---|---|

## Audience Notes
- Geography:
- Language:
- Niche/content fit:
- Comment quality:

## Sponsorship Recommendation
- Good fit / Maybe / Poor fit
- Why:
```

## Common Pitfalls

- Do not infer exact demographics from vibes. Use available evidence and label assumptions.
- Do not overpromise audience details for platforms that do not expose them publicly.
- Do not ignore mismatch between creator location and audience location.

## VAS installation notes

- Canonical ID: `scrapecreators-audience-research`
- Source repository: [`ScrapeCreators/social-media-research-skills`](https://github.com/ScrapeCreators/social-media-research-skills) (revision `64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2`, path `skills/audience-research`)
- Author: ScrapeCreators ([@ScrapeCreators](https://github.com/ScrapeCreators))
- License: MIT License (see bundled `LICENSE`)
- Role: Social media research and intelligence workflow for AI coding agents.
- Prerequisites: Requires `SCRAPECREATORS_API_KEY` for live API scraping operations; offline analysis and prompt templating function without credentials.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
