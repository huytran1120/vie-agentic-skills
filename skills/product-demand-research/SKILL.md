---
name: product-demand-research
description: Use when the user wants to validate a product idea, find pain points, mine demand signals, discover objections, or gather voice-of-customer language from Reddit, social posts, video transcripts, and comments. Produces evidence-backed product research.
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

# Product Demand Research

## Overview

Use public social data to understand whether people actually complain about, ask for, buy, hack around, or recommend solutions in a product category. The output should help founders and marketers decide what to build, position, or test.

## When to Use

Use this skill when the user asks to:

- validate a startup or product idea
- find pain points in a niche
- mine Reddit/TikTok/YouTube comments for product ideas
- find buyer language and objections
- understand alternatives people use today
- create messaging from demand evidence

## Signals to Extract

- repeated complaints
- "I wish" / "is there a tool" / "how do I" phrases
- workarounds and spreadsheets/manual processes
- comparison and alternative mentions
- buying intent
- objections to existing solutions
- exact words people use for the problem

## Workflow

1. Turn the idea into search queries and synonyms.
2. Search Reddit and relevant social platforms.
3. Pull comments/transcripts for promising posts/videos.
4. Cluster pains, triggers, alternatives, and desired outcomes.
5. Score demand by frequency, intensity, recency, and willingness-to-pay hints.
6. Produce messaging and product implications.

## Output Format

```markdown
# Product Demand Research: {idea/category}

## Verdict
- Demand signal: Strong/Medium/Weak
- Confidence: High/Medium/Low
- Why:

## Pain Points
| Pain | Evidence | Exact language | Source |
|---|---|---|---|

## Existing Alternatives / Workarounds
- ...

## Objections and Barriers
- ...

## Messaging Angles
- "..."

## Product Ideas / Tests
1. ...
2. ...
```

## Common Pitfalls

- Do not claim market validation from a handful of comments.
- Do not ignore negative evidence or existing alternatives.
- Do not paraphrase away the best customer language.

## VAS installation notes

- Canonical ID: `product-demand-research`
- Source repository: [`ScrapeCreators/social-media-research-skills`](https://github.com/ScrapeCreators/social-media-research-skills) (revision `64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2`, path `skills/product-demand-research`)
- Author: ScrapeCreators ([@ScrapeCreators](https://github.com/ScrapeCreators))
- License: MIT License (see bundled `LICENSE`)
- Role: Social media research and intelligence workflow for AI coding agents.
- Prerequisites: Requires `SCRAPECREATORS_API_KEY` for live API scraping operations; offline analysis and prompt templating function without credentials.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
