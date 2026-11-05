# Notices

`store-screenshots` skill code, reference texts, and classification data are MIT licensed (Copyright (c) 2026 Alpiworks); see bundled `LICENSE`.

## Third-party material

`skills/store-screenshots/assets/library/img/` contains downscaled App Store screenshots of third-party apps,
collected from Apple's public App Store listings on 2026-11-04 for study and reference only. They remain the
property of their respective publishers; app names and marks are trademarks of their owners. They are not
covered by this project's license, must not be reused in store listings or other products, and will be
removed on request by a rights holder (open an issue).

The OCR text, labels and notes in `catalog.json` / `classifications.json` are Alpiworks' own analysis.

## Prerequisites & External Services

- Standard screenshot planning, visual DNA extraction, and copy rules run dependency-free with Python standard library.
- Scene rendering and SVG output optionally use `Pillow` and `resvg-py` for PNG and SVG rasterization.
- Multi-language OCR checks optionally use system `tesseract` (with language models such as `tur.traineddata`).
- No external runtime, network API key, or MCP service is required for installation or baseline offline operation.

## Safe Operation

Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`.
No unapproved scripts are executed, no external dependencies or MCP servers are installed, and
no background processes or accounts are connected during installation.
