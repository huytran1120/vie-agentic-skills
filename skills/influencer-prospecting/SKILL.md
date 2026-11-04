---
name: influencer-prospecting
description: Use when the user wants to find creators, influencers, affiliates, or social accounts in a niche for outreach, partnerships, sponsorships, UGC, seeding, or competitive research. Produces scored prospect lists from public social data.
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

# Influencer Prospecting

## Overview

Build practical creator prospect lists from public social data. The goal is to find accounts that fit the niche, have enough reach, and show evidence of relevant content or audience fit.

## When to Use

Use this skill when the user asks to:

- find influencers or creators in a niche
- build a UGC, affiliate, sponsorship, or seeding list
- find micro-influencers with strong engagement
- identify creators who already talk about a product category
- export prospects as CSV

## Useful Sources

- TikTok search users, popular creators, profile, profile videos, audience demographics
- Instagram search profiles, profile, posts, reels
- YouTube search and channel details
- Link-in-bio services: Linktree, Komi, Pillar, Linkbio, Linkme
- Amazon Shop and TikTok Shop showcase where relevant

## Scoring Framework

Score each prospect 1-5 on:

- **Niche fit** — content clearly matches the category
- **Audience fit** — country/language/platform fit when public data supports it
- **Reach** — followers/subscribers and recent views
- **Engagement quality** — comments look real and relevant
- **Brand safety** — obvious controversy or mismatch risk
- **Contactability** — public links/email/contact path available

## Output Format

```markdown
# Influencer Prospect List: {niche}

| Creator | Platform | Followers | Recent views | Fit | Contact path | Notes |
|---|---|---:|---:|---:|---|---|

## Best Fits
1. ...

## Outreach Angles
- ...

## CSV
```csv
creator,platform,profile_url,followers,recent_views,fit_score,contact_path,notes
```
```

## Common Pitfalls

- Do not equate large follower count with good fit.
- Do not scrape or expose private contact data. Use public links only.
- Do not hide uncertainty when profiles have limited public data.

## VAS installation notes

- Canonical ID: `influencer-prospecting`
- Source repository: [`ScrapeCreators/social-media-research-skills`](https://github.com/ScrapeCreators/social-media-research-skills) (revision `64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2`, path `skills/influencer-prospecting`)
- Author: ScrapeCreators ([@ScrapeCreators](https://github.com/ScrapeCreators))
- License: MIT License (see bundled `LICENSE`)
- Role: Social media research and intelligence workflow for AI coding agents.
- Prerequisites: Requires `SCRAPECREATORS_API_KEY` for live API scraping operations; offline analysis and prompt templating function without credentials.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
