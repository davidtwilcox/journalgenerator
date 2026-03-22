# Journal Generator

Generates journal pages as PDF documents.

## Setup

```bash
pip install -e .
```

## Usage

```bash
journal-generator --type <TYPE> [options]
```

Alternatively, run as a Python module:

```bash
python -m py_journal_generator --type <TYPE> [options]
```

Run without arguments to display this parameter reference.

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--type` | Yes | | Page type: `H` (hex map), `L` (lined), `D` (dot grid). Case-insensitive. |
| `--pagesize` | No | `A5` | Page size name. See available sizes below. |
| `--size` | No | See below | Size value whose meaning depends on page type. |
| `--width` | No | See below | Width value whose meaning depends on page type. Ignored for `H`. |
| `--numpages` | No | `1` | Number of pages to generate. Must be a positive integer. |
| `--output` | No | `journal-YYYYmmddHHMMSS.pdf` | Output filename. `.pdf` extension is added automatically if omitted. |

### --size defaults by type

| Type | Default | Description |
|---|---|---|
| `H` | `7.5` | Hex size (mm) |
| `L` | `8.0` | Line spacing (mm) |
| `D` | `0.2` | Dot size (mm) |

### --width defaults by type

| Type | Default | Description |
|---|---|---|
| `H` | — | Ignored |
| `L` | `0.1` | Line width (mm) |
| `D` | `5.0` | Dot spacing (mm) |

### Available page sizes

| Name | Width (mm) | Height (mm) |
|---|---|---|
| `A4` | 210 | 297 |
| `A5` | 148 | 210 |
| `A6` | 105 | 148 |
| `B4` | 250 | 353 |
| `B5` | 176 | 250 |
| `B6` | 125 | 176 |
| `letter` | 216 | 279 |
| `halfletter` | 140 | 216 |
| `legal` | 216 | 356 |

Page sizes are defined in `py_journal_generator/page_sizes.yaml`.

## Examples

```bash
# A5 hex map with default settings
journal-generator --type H

# A4 lined journal, 10 pages, saved to my-journal.pdf
journal-generator --type L --pagesize A4 --numpages 10 --output my-journal

# Letter-size dot grid with custom dot size and spacing
journal-generator --type D --pagesize letter --size 0.3 --width 6

# A5 hex map with larger hexagons
journal-generator --type H --size 10
```
