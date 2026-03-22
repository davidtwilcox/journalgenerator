# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Setup:**
```bash
pip install -e .
```

**Run:**
```bash
journal-generator --type <H|L|D> [--pagesize NAME] [--size FLOAT] [--width FLOAT] [--numpages INT] [--output FILENAME]
# or
python -m py_journal_generator --type <H|L|D> ...
```

Run without arguments to see the full help message.

**Lint:**
```bash
python3 -m ruff check .
python3 -m ruff check . --fix   # auto-fix
```

**Test:**
```bash
python3 -m pytest -v
```

## Architecture

`py_journal_generator` generates A5 PDF journal pages using [fpdf2](https://py-pdf.github.io/fpdf2/).

**Class hierarchy:**

- `journal_page.JournalPage` (abstract base) — stores page dimensions and margins, computes content area (width/height minus margins), defines `render(pdf)` interface
  - `lined_journal_page.LinedJournalPage` — horizontal ruled lines with configurable spacing
  - `dot_journal_page.DotJournalPage` — dot grid with configurable dot size and spacing
  - `hex_map_journal_page.HexMapJournalPage` — hexagon tessellation grid with optional row/column labels; uses `Hexagon` for geometry
- `hexagon.Hexagon` — geometry utility: computes diagonals, apothem, and 6 vertex coordinates from a side length
- `pdf.PDF` — thin subclass of `fpdf.FPDF` (no added behavior; exists for future extension)

**Entry point:** `py_journal_generator/__main__.py` — parses CLI args, loads `page_sizes.yaml` via `importlib.resources`, creates a `PDF` sized to the chosen page, renders `--numpages` pages of the chosen type, and writes the output PDF. Registered as the `journal-generator` console script in `pyproject.toml`.

**`page_sizes.yaml`** — bundled inside the package (`py_journal_generator/page_sizes.yaml`) and loaded via `importlib.resources`. `--pagesize` must match a `name` entry.

**Key conventions:**
- All measurements are in millimeters
- Margins are `(top, right, bottom, left)` = `(4.5, 4.5, 4.5, 10.0)` — 10mm binding margin on the left
- Content area origin is margin-offset from the PDF page corner; pages handle their own coordinate math
- Hexagon grid rows alternate with a half-hex horizontal offset for proper tessellation
