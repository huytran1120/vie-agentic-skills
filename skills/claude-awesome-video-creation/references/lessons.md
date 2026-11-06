# Lessons: what the user asked for, and the rule it became

These come from building "Teach It Once", a 1:54 course video about Claude Code Agent Skills, together with a university student over one long session. Each line is a request, then the rule to apply by default next time.

## Content and structure
| Request | Rule |
|---|---|
| "Can others follow this and use the tool on their own computer?" | Tutorial mode: install → add → use → write your own → cheat sheet. Every command appears in full on screen while the voice says it. |
| "The Agent Skills content is too shallow" | Show the mechanism, not just a slogan: real paths, the file anatomy, and the three loading stages (discovery, activation, execution). |
| "Higher information density, richer content" | About 160 wpm of VO; each scene carries its own on-screen facts (commands, paths, labels), not decoration. |
| "Avoid `.md` jargon, make it easier to understand" | Say the plain word ("instruction file") and show the filename next to it. Never speak a filename as the only explanation. |
| "The audience is university students" | Use examples from their life: lab reports, slides, reference lists, citations, exam revision, thesis drafts, "your project group". |
| "Say this is only the basics; skills go much deeper" | Add a "This is just the basics" card listing what else it can do, plus the author's contact for questions. |
| "Put my contact at the end" | Show the email on a card while the VO says "Email me any time", then keep it in the footer. |
| "Ask for votes at the end" | Finish with a vote or like call to action: a bright card, one VO line, a sound hit, confetti. Make it say *what* to vote for (ID and title). |
| "Use my own skill and link it" | The skill demoed is the author's own published skill: the install command, a link, and "a reusable workflow I optimised". |
| "Optimise the overall logic" | One thread through the video: the skill I explain is the skill I built, and it is the skill that made this video. |

## Pace and sound
| Request | Rule |
|---|---|
| "Make the background music calmer" | Half-time kick, softer pads, fewer hats; the energetic version stays behind a flag. |
| "Tighter rhythm, slightly faster speech" | Re-split scenes from measured speech; slack per scene 0.3–0.8 s; draft TTS at +11–16%. |
| "A bit slower again" | Keep one constant for the TTS rate and change only that; never re-time scenes by hand. |
| "1:17 has an obvious stutter" | That was 0.5 s of black plus total silence before the drop. Ban dead air: suck-in visuals and a continuous riser. |
| "The second half of the sentence is too far from the first" | A sentence split across a cut must resume within about 1.2 s of the drop. |

## Look
| Request | Rule |
|---|---|
| "Premium, fancy, more varied animation" | Every transition is designed (zoom-through, whip, push-in, fold, converge), with motion blur, masked rises and sheen; no two scenes share an exit. |
| "Bigger terminal fonts" | Terminal text ≥ 25 px at 1080p; commands 26–32 px. |
| "Too plain, add colour" | Navy stage plus aurora lights; one hue per step, stage and label; syntax colours in every command. |
| "A popular blue terminal background" | Cobalt2-style blue `#193549` for windows. |
| "A little glass, and keep the terminal separate from the background" | Fake glass (translucent gradient, sheen, light rim) plus a layered shadow and a faint cyan halo. No `backdrop-filter`. |
| "Mac-style terminal, high-end" | 12 px corners, 38 px title bar, centred title (`my-project — zsh — 96×24`), a `%` prompt, and traffic lights with highlights. |
| "Make the S09 'made by Claude' moment dazzling" | A Droste spiral of the video inside itself, flying real source lines, beat rings, and words slammed in sync with the voice. |

## Mascot
| Request | Rule |
|---|---|
| "Use Squirtle / my Squirtle avatar" | Refuse politely (third-party IP, and "all content must be your own"); offer an original character that keeps the vibe. |
| "The second design, blue hoodie and headphones, a cap, square glasses, a silver Mac, chubbier" | Iterate on the locked base by edits. A silver laptop has no logo, because the logo is a trademark. |
| "The screenshot is cut off at top and bottom" | Re-frame the base with ≥ 14% margin before making any variants. |
| "Not a fixed position; smooth movement; no flicker; more frames; richer mouth shapes" | Timed hop moves, turns through scaleX = 0, in-between gesture frames, 7 visemes, opaque crossfade compositing. |

## Process
- Before rewriting content, get the script approved; a changed script means changed TTS timing and voice-clone input.
- Verify commands against the official docs on the day you build (install script URLs, skill paths, `/skills`).
- A render that has stopped making progress is broken: check whether the output file is still growing and fix the cause; don't wait.
- Report outcomes with numbers: duration, frames, LUFS, static runs, measured render time.
