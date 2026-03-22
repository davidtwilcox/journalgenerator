# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Setup:**
```bash
pip install -e .
```

**Run (generates test.pdf):**
```bash
python main.py
```

There are no tests, linting, or build steps configured.

## Architecture

`py_journal_generator` generates A5 PDF journal pages using [fpdf2](https://py-pdf.github.io/fpdf2/).

**Class hierarchy:**

- `journal_page.JournalPage` (abstract base) — stores page dimensions and margins, computes content area (width/height minus margins), defines `render(pdf)` interface
  - `lined_journal_page.LinedJournalPage` — horizontal ruled lines with configurable spacing
  - `dot_journal_page.DotJournalPage` — dot grid with configurable dot size and spacing
  - `hex_map_journal_page.HexMapJournalPage` — hexagon tessellation grid with optional row/column labels; uses `Hexagon` for geometry
- `hexagon.Hexagon` — geometry utility: computes diagonals, apothem, and 6 vertex coordinates from a side length
- `pdf.PDF` — thin subclass of `fpdf.FPDF` (no added behavior; exists for future extension)

**Data flow:** `main.py` creates a `PDF`, instantiates page objects (left/right variants via mirrored margin tuples), calls `render(pdf)` on each, then writes `test.pdf`.

**Key conventions:**
- All measurements are in millimeters
- Left vs. right page variants are created by swapping the left/right margin values (binding margin is 10mm, others 4.5mm)
- Content area origin is margin-offset from the PDF page corner; pages handle their own coordinate math
- Hexagon grid rows alternate with a half-hex horizontal offset for proper tessellation
