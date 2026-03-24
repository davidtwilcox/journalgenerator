import argparse
import sys
from datetime import datetime
from importlib.resources import files

import yaml

from py_journal_generator.dot_journal_page import DotJournalPage
from py_journal_generator.hex_map_journal_page import HexMapJournalPage
from py_journal_generator.lined_journal_page import LinedJournalPage
from py_journal_generator.pdf import PDF


def load_page_sizes() -> dict:
    text = files("py_journal_generator").joinpath("page_sizes.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return {entry["name"]: entry for entry in data["page_sizes"]}


def positive_int(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid integer.")
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"Value must be 1 or greater (got {ivalue}).")
    return ivalue


def nonzero_float(value: str) -> float:
    try:
        fvalue = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid number.")
    if fvalue == 0:
        raise argparse.ArgumentTypeError("Value must be non-zero.")
    return fvalue


def positive_float(value: str) -> float:
    try:
        fvalue = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid number.")
    if fvalue <= 0:
        raise argparse.ArgumentTypeError(f"Value must be positive (got {fvalue}).")
    return fvalue


def parse_bool(value: str) -> bool:
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    raise argparse.ArgumentTypeError(f"'{value}' is not a valid boolean. Use 'true' or 'false'.")


def parse_margins(value: str) -> tuple:
    parts = [p.strip() for p in value.split(",")]
    if len(parts) not in (2, 4):
        raise argparse.ArgumentTypeError("--margins requires 2 or 4 comma-separated values.")
    try:
        floats = [float(p) for p in parts]
    except ValueError:
        raise argparse.ArgumentTypeError("All margin values must be valid numbers.")
    for f in floats:
        if f <= 0:
            raise argparse.ArgumentTypeError(f"All margin values must be positive (got {f}).")
    if len(floats) == 2:
        top_bottom, left_right = floats
        return (top_bottom, left_right, top_bottom, left_right)  # top, right, bottom, left
    return tuple(floats)  # top, right, bottom, left


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate journal pages as a PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--pagesize",
        default="A5",
        metavar="NAME",
        help="Page size name from page_sizes.yaml (e.g. A5, A4, letter). Default: A5",
    )
    parser.add_argument(
        "--type",
        default=None,
        metavar="TYPE",
        help="Page type: H=Hex map, L=Lined, D=Dot grid (case-insensitive, required)",
    )
    parser.add_argument(
        "--size",
        type=nonzero_float,
        metavar="FLOAT",
        help=(
            "Size parameter: line width for L (default 0.1), dot size for D (default 0.2). Ignored for H"
        ),
    )
    parser.add_argument(
        "--width",
        type=positive_float,
        metavar="FLOAT",
        help=(
            "Width parameter: hex size for H (default 7.5), "
            "line spacing for L (default 8.0), dot spacing for D (default 5.0)"
        ),
    )
    parser.add_argument(
        "--numpages",
        type=positive_int,
        default=1,
        metavar="INT",
        help="Number of pages to generate (must be >= 1). Default: 1",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="FILENAME",
        help="Output PDF filename. Default: journal-YYYYmmddHHMMSS.pdf",
    )
    parser.add_argument(
        "--margins",
        type=parse_margins,
        default=None,
        metavar="FLOATS",
        help=(
            "Page margins in mm as 2 or 4 comma-separated positive values. "
            "2 values: top/bottom,left/right. "
            "4 values: top,right,bottom,left. "
            "Defaults: top=4.5, right=4.5, bottom=4.5, left=10.0"
        ),
    )
    parser.add_argument(
        "--mirror",
        type=parse_bool,
        default=False,
        metavar="BOOL",
        help="Swap left and right margins on odd-numbered pages (true/false). Default: false",
    )
    return parser


def main():
    page_sizes = load_page_sizes()
    parser = build_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.pagesize not in page_sizes:
        available = ", ".join(page_sizes.keys())
        print(f"Error: Unknown page size '{args.pagesize}'. Available sizes: {available}")
        sys.exit(1)

    if args.type is None:
        print("Error: --type is required. Use H for Hex map, L for Lined, or D for Dot grid.")
        sys.exit(1)

    page_type = args.type.upper()
    if page_type not in ("H", "L", "D"):
        print(f"Error: --type must be H, L, or D (got '{args.type}').")
        sys.exit(1)

    if args.output is not None and args.output.strip() == "":
        print("Error: --output filename cannot be empty.")
        sys.exit(1)

    if args.output is None:
        output_filename = datetime.now().strftime("journal-%Y%m%d%H%M%S.pdf")
    else:
        output_filename = args.output if args.output.lower().endswith(".pdf") else args.output + ".pdf"

    page_entry = page_sizes[args.pagesize]
    pdf_w = float(page_entry["width"])
    pdf_h = float(page_entry["height"])
    page_size = (pdf_w, pdf_h)
    base_margins = args.margins if args.margins is not None else (4.5, 4.5, 4.5, 10.0)

    pdf = PDF(unit="mm", format=(pdf_w, pdf_h))
    pdf.set_draw_color(63, 63, 63)
    pdf.set_line_width(0.1)

    for i in range(args.numpages):
        page_num = i + 1
        if args.mirror and page_num % 2 == 0:
            top, right, bottom, left = base_margins
            margins = (top, left, bottom, right)
        else:
            margins = base_margins

        if page_type == "H":
            page = HexMapJournalPage(page_size, margins, args.width if args.width is not None else 7.5)
        elif page_type == "L":
            page = LinedJournalPage(
                page_size,
                margins,
                args.size if args.size is not None else 0.1,
                args.width if args.width is not None else 8.0,
            )
        else:
            page = DotJournalPage(
                page_size,
                margins,
                args.size if args.size is not None else 0.2,
                args.width if args.width is not None else 5.0,
            )
        page.render(pdf)

    pdf.output(output_filename)
    print(f"Generated {output_filename}: {args.numpages} page(s), type={page_type}, pagesize={args.pagesize}")


if __name__ == "__main__":
    main()
