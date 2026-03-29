# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Setup:**
```bash
pip install -e .
```

**Run:**
```bash
journal-generator --type <H|L|D|S> [--pagesize NAME] [--size FLOAT] [--width FLOAT] [--numpages INT] [--output FILENAME] [--margins FLOATS] [--mirror BOOL] [--rotated BOOL]
# or
python -m py_journal_generator --type <H|L|D|S> ...
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

`py_journal_generator` generates PDF journal pages using [fpdf2](https://py-pdf.github.io/fpdf2/).

**Class hierarchy:**

- `journal_page.JournalPage` (abstract base) — stores page dimensions and margins, computes content area (width/height minus margins), defines `render(pdf)` interface
  - `lined_journal_page.LinedJournalPage` — horizontal ruled lines with configurable line width and spacing
  - `dot_journal_page.DotJournalPage` — dot grid with configurable dot size and spacing
  - `hex_map_journal_page.HexMapJournalPage` — hexagon tessellation grid; supports flat-top and rotated (pointy-top) orientations; uses `Hexagon` for geometry
  - `square_journal_page.SquareJournalPage` — square grid with configurable line width and square size
- `hexagon.Hexagon` — geometry utility: computes diagonals, apothem, and 6 vertex coordinates from a width (short diagonal); supports `rotated=True` for pointy-top orientation
- `pdf.PDF` — thin subclass of `fpdf.FPDF` (no added behavior; exists for future extension)

**Entry point:** `py_journal_generator/__main__.py` — parses CLI args, loads `page_sizes.yaml` via `importlib.resources`, creates a `PDF` sized to the chosen page, renders `--numpages` pages of the chosen type, and writes the output PDF. Registered as the `journal-generator` console script in `pyproject.toml`.

**`page_sizes.yaml`** — bundled inside the package (`py_journal_generator/page_sizes.yaml`) and loaded via `importlib.resources`. `--pagesize` must match a `name` entry.

**Key conventions:**
- All measurements are in millimeters
- Margins are `(top, right, bottom, left)` = `(4.5, 4.5, 4.5, 10.0)` — 10mm binding margin on the left
- Content area origin is margin-offset from the PDF page corner; pages handle their own coordinate math
- `Hexagon` takes `width` (the short diagonal / flat-top horizontal span); side length is derived as `(2/√3) * (width/2)`
- Flat-top hex rows alternate with a half-hex (`apothem`) horizontal offset for tessellation; rotated (pointy-top) rows alternate with a `three_quarter_height` offset
- `--rotated` and `--size` only apply to type `H`; `--rotated` is ignored by `L`, `D`, and `S`
