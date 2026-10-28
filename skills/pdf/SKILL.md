---
name: pdf
description: >-
  Read text from ordinary PDF files or create a simple PDF with Python.
  Use for local document extraction and basic PDF generation, with explicit
  handling of encrypted files, scanned pages, and output verification.
category: general
tags: [pdf, documents, python, extraction]
risk: safe
author: Vie Agentic Skill contributors
license: MIT
source: local-original
source_path: skills/pdf/SKILL.md
---

# PDF document workflow

This is an independently authored Vie Agentic Skill runbook. It does not
include or derive from the excluded upstream PDF skill or its helper scripts.
The project MIT license applies to this runbook; dependencies keep their own licenses.

## Before starting

Identify the input file, requested pages, expected output, and whether the
document contains sensitive information. Work locally. Confirm that the user
has permission to process it. Never overwrite the source or upload it to a
service without permission.

The catalog CLI requires no extra packages. To execute the examples, use a
dedicated environment and install only the task dependencies:

```bash
python3 -m venv .venv-documents
.venv-documents/bin/python -m pip install pypdf reportlab
```

On Windows, use `.venv-documents\Scripts\python.exe`.

## Extract selectable text

1. Check that the input exists and is a PDF. Do not execute embedded attachments.
2. Read the page count. Stop on encryption unless an authorized decryption
   workflow has been agreed; do not attempt password recovery.
3. Extract the requested pages and keep page boundaries in the text output.
4. If pages contain no selectable text, report that OCR is a separate task;
   do not present empty extraction as successful document understanding.

```python
from pathlib import Path
from pypdf import PdfReader

source = Path("input.pdf")
reader = PdfReader(source)
if reader.is_encrypted:
    raise ValueError("Encrypted input requires an authorized decryption workflow.")
pages = [page.extract_text() or "" for page in reader.pages]
if not any(text.strip() for text in pages):
    raise ValueError("No selectable text found; the document may need OCR.")
with Path("extracted.txt").open("x", encoding="utf-8") as output:
    output.write("\n\n".join(f"Page {i}\n{text}" for i, text in enumerate(pages, 1)))
```

## Create a basic PDF

```python
from pathlib import Path
from reportlab.pdfgen import canvas
from pypdf import PdfReader

destination = Path("notes.pdf")
with destination.open("xb") as output:
    document = canvas.Canvas(output)
    document.drawString(72, 750, "Project notes")
    document.drawString(72, 725, "Status: ready for review")
    document.save()
assert len(PdfReader(destination).pages) == 1
```

## Verify and report

Reopen the output, check page count and representative text, and visually
inspect a rendered page when layout matters. Report output paths, processed
pages, missing text and any unsupported content. Text order, tables and
reading order are not guaranteed by extraction. The basic example is not an
OCR, redaction, accessibility-tagging or digital-signature tool. Proper
Unicode font embedding and complex layouts require additional setup.
