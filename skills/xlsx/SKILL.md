---
name: xlsx
description: >-
  Inspect or create a local XLSX workbook with openpyxl.
  Use for tabular data, simple formulas and workbook validation without
  executing macros or pretending that formulas have been recalculated.
category: general
tags: [xlsx, spreadsheets, documents, python]
risk: safe
author: Vie Agentic Skill contributors
license: MIT
source: local-original
source_path: skills/xlsx/SKILL.md
---

# Spreadsheet workflow

This independently authored Vie Agentic Skill runbook does not reuse the
excluded upstream XLSX skill or its helper code. The project MIT license
applies to this runbook; dependencies keep their own licenses.

## Establish the data contract

Confirm input sheet names, expected columns, units, date conventions, null
values and output path. Work on a copy. Do not silently drop rows, infer
missing financial values or present estimates as source data.

The example dependency is optional and separate from the catalog CLI:

```bash
python3 -m venv .venv-documents
.venv-documents/bin/python -m pip install openpyxl
```

On Windows, use `.venv-documents\Scripts\python.exe`.

## Inspect a workbook

```python
from openpyxl import load_workbook

workbook = load_workbook(
    "input.xlsx", read_only=True, data_only=False, keep_links=False
)
try:
    print(workbook.sheetnames)
    sheet = workbook[workbook.sheetnames[0]]
    for row in sheet.iter_rows(min_row=1, max_row=5, values_only=True):
        print(row)
finally:
    workbook.close()
```

Limit previews and avoid shared logging of sensitive cells. `data_only=False`
returns formula expressions; `data_only=True` reads cached results that may
be stale or absent. Neither mode calculates formulas.

## Create a small workbook

```python
from pathlib import Path
from openpyxl import Workbook, load_workbook

workbook = Workbook()
sheet = workbook.active
sheet.title = "Summary"
sheet.append(["Item", "Quantity"])
sheet.append(["Documents", 4])
sheet.append(["Total", "=SUM(B2:B2)"])
sheet.freeze_panes = "A2"
sheet.auto_filter.ref = "A1:B2"
sheet.column_dimensions["A"].width = 24
destination = Path("summary.xlsx")
with destination.open("xb") as output:
    workbook.save(output)
checked = load_workbook(destination, data_only=False)
try:
    assert checked["Summary"]["B2"].value == 4
    assert checked["Summary"]["B3"].value == "=SUM(B2:B2)"
finally:
    checked.close()
```

## Protect and verify

Validate row counts, column names, numeric types and representative values.
Treat untrusted strings beginning with formula markers as literal text:
explicitly write them as string cells rather than accepting them as formulas.
Never interpolate untrusted text into formula expressions.

Do not enable macros, refresh external connections or fetch links. Use a
spreadsheet application for an approved recalculation and visual check when
computed results or formatting matter. Editing macro-enabled files, legacy
`.xls`, complex chart preservation and full Excel fidelity are outside this
runbook. Report the output path, changed sheets, validation results and any
formula results that still require recalculation.
