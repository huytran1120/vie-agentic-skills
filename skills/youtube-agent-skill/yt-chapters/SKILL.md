---
name: yt-chapters
description: >-
  Write YouTube chapters from a transcript, validated against YouTube's own
  rules so they actually render. Use for "add chapters", "timestamps",
  "break this video into sections".
---

# yt-chapters

```bash
python3 chapters.py transcript.srt --target 8
```

## The rules, which are not optional

A chapter list that breaks any of these silently does not become chapters at all - the block just
sits in the description doing nothing:

- The first entry must be **00:00**.
- There must be **at least three**.
- Each must be **at least 10 seconds** long.

The tool checks all three and tells you when a list is invalid rather than letting you paste it.

## Retitle every line

`chapters.py` finds the BOUNDARIES well - it scores the pauses you actually took by how much the
vocabulary shifts across them. The titles it emits are the topic words, and they are a draft. A
chapter called "Thumbnails Titles Packaging" is a placeholder. Rewrite each one as the promise of
that section, in the user's voice, three to five words.

Chapters are also a retention diagnostic: if a section cannot be named in five words, it is two
sections or it is filler.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**


## VAS installation notes

Run Python helper commands from this installed skill's directory. The helpers use
only the Python 3 standard library. Any helper dependencies needed by this skill
are bundled locally, so installing sibling skills is not required to run them.

The optional voice profile template is [templates/voice.md](templates/voice.md).
The upstream profile location is `~/.claude/youtube/voice.md`; create or update it
only with the user's permission. Installing this skill does not create that file.

The `/yt-*` names in this runbook refer to the upstream Claude commands. Other
agents can read this `SKILL.md` directly; related workflows are separate VAS
skills. Nothing in this pack connects to an account or publishes automatically.
