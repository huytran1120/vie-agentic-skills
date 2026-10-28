---
name: pptx
description: >-
  Build or inspect a simple PowerPoint presentation with python-pptx.
  Use for local slide titles, text and basic shapes, followed by structural
  and visual checks before delivery.
category: general
tags: [pptx, presentations, documents, python]
risk: safe
author: Vie Agentic Skill contributors
license: MIT
source: local-original
source_path: skills/pptx/SKILL.md
---

# Presentation workflow

This is an independently authored Vie Agentic Skill runbook. It does not
reuse the excluded upstream PPTX skill, templates, scripts or assets.
The project MIT license applies to this runbook; dependencies keep their own licenses.

## Define the presentation

Confirm audience, purpose, slide count, aspect ratio, language and any
authorized template or media. Draft one message per slide before writing
code. Do not invent supporting data, branding permissions or image credits.

The catalog CLI remains dependency-free. The examples optionally require:

```bash
python3 -m venv .venv-documents
.venv-documents/bin/python -m pip install python-pptx
```

On Windows, use `.venv-documents\Scripts\python.exe`.

## Inspect slide text

```python
from pptx import Presentation

presentation = Presentation("input.pptx")
for number, slide in enumerate(presentation.slides, 1):
    text = [shape.text for shape in slide.shapes if shape.has_text_frame]
    print(number, text)
```

This is a text inventory, not a complete extraction of charts, notes, tables
or grouped content. Avoid logging private slide text to shared output.

## Create a small deck

1. Use a standard slide size and consistent text hierarchy.
2. Keep messages brief enough for the slide, not just for the text box.
3. Save a new file and inspect it after writing.

```python
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches

presentation = Presentation()
presentation.slide_width = Inches(13.333)
presentation.slide_height = Inches(7.5)
title = presentation.slides.add_slide(presentation.slide_layouts[0])
title.shapes.title.text = "Project update"
title.placeholders[1].text = "Review meeting"
summary = presentation.slides.add_slide(presentation.slide_layouts[1])
summary.shapes.title.text = "Next decisions"
summary.placeholders[1].text = "Review the implementation\nConfirm the release scope"
destination = Path("update.pptx")
with destination.open("xb") as output:
    presentation.save(output)
checked = Presentation(destination)
assert len(checked.slides) == 2
assert checked.slides[1].shapes.title.text == "Next decisions"
```

## Acceptance and limits

Open the deck in an approved presentation viewer or local renderer. Check
every slide for clipping, overflow, legibility, contrast and missing fonts.
Structural assertions cannot replace visual review.

For edits, retain the original file and explain any unsupported content.
Do not execute macros, embedded applications or external links. Animation,
SmartArt editing, legacy `.ppt` conversion and faithful rendering are not
provided by this runbook. Report slide count, output path and remaining
visual-review requirements.
