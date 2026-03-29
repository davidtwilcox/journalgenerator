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
| `--type` | Yes | | Page type: `H` (hex map), `L` (lined), `D` (dot grid), `S` (square grid). Case-insensitive. |
| `--pagesize` | No | `A5` | Page size name. See available sizes below. |
| `--size` | No | See below | Size value whose meaning depends on page type. |
| `--width` | No | See below | Width value whose meaning depends on page type. |
| `--numpages` | No | `1` | Number of pages to generate. Must be a positive integer. |
| `--output` | No | `journal-YYYYmmddHHMMSS.pdf` | Output filename. `.pdf` extension is added automatically if omitted. |
| `--margins` | No | See below | Page margins in mm as 2 or 4 comma-separated positive values. |
| `--mirror` | No | `false` | Swap left and right margins on odd-numbered pages (`true`/`false`). |
| `--rotated` | No | `false` | Use flat-top hexagon orientation (`true`/`false`). Default is pointy-top. Only applies to `H` type. |

### --size defaults by type

| Type | Default | Description     |
|---|---------|-----------------|
| `H` | `0.1`   | Line width (mm) |
| `L` | `0.1`   | Line width (mm) |
| `D` | `0.2`   | Dot size (mm)   |
| `S` | `0.1`   | Line width (mm) |

### --width defaults by type

| Type | Default | Description |
|---|---|---|
| `H` | `10.0` | Hex size (mm) |
| `L` | `8.0` | Line spacing (mm) |
| `D` | `5.0` | Dot spacing (mm) |
| `S` | `5.0` | Square size (mm) |

### --margins

Accepts 2 or 4 comma-separated positive values (in mm):

| Format | Values | Description |
|---|---|---|
| 2 values | `top/bottom,left/right` | e.g. `5,10` sets top=5, bottom=5, left=10, right=10 |
| 4 values | `top,right,bottom,left` | e.g. `4.5,4.5,4.5,10` |

Defaults: top=`4.5`, right=`4.5`, bottom=`4.5`, left=`10.0`.

When `--mirror true` is set, the provided margins apply to odd-numbered pages. Even-numbered pages have their left and right margins swapped.

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
journal-generator --type H --width 12

# A5 rotated hex map
journal-generator --type H --rotated true

# A5 square grid
journal-generator --type S

# 20-page lined journal with mirrored margins for binding
journal-generator --type L --numpages 20 --margins "4.5,4.5,4.5,10" --mirror true
```
