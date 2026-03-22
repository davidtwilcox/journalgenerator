from typing import Tuple

from py_journal_generator.hex_map_journal_page import HexMapJournalPage
from py_journal_generator.lined_journal_page import LinedJournalPage
from py_journal_generator.dot_journal_page import DotJournalPage
from py_journal_generator.pdf import PDF

PDF_W: float = 148
PDF_H: float = 210

if __name__ == "__main__":
    pdf = PDF(unit='mm', format='A5')

    pdf.set_draw_color(63, 63, 63)
    pdf.set_line_width(0.1)

    page_size: Tuple[float, float] = (PDF_W, PDF_H)
    right_page_margins: Tuple[float, float, float, float] = (4.5, 4.5, 4.5, 10.0)
    left_page_margins: Tuple[float, float, float, float] = (4.5, 10.0, 4.5, 4.5)

    hex_size: float = 7.5
    hex_right_page: HexMapJournalPage = HexMapJournalPage(page_size, right_page_margins, hex_size, False)
    hex_left_page: HexMapJournalPage = HexMapJournalPage(page_size, left_page_margins, hex_size, False)
    hex_right_page.render(pdf)
    hex_left_page.render(pdf)

    line_width: float = 0.1
    line_size: float = 8.0
    lined_right_page: LinedJournalPage = LinedJournalPage(page_size, right_page_margins, line_width, line_size)
    lined_left_page: LinedJournalPage = LinedJournalPage(page_size, left_page_margins, line_width, line_size)
    lined_right_page.render(pdf)
    lined_left_page.render(pdf)

    dot_size: float = 0.2
    dot_space: float = 5.0
    dot_right_page: DotJournalPage = DotJournalPage(page_size, right_page_margins, dot_size, dot_space)
    dot_left_page: DotJournalPage = DotJournalPage(page_size, left_page_margins, dot_size, dot_space)
    dot_right_page.render(pdf)
    dot_left_page.render(pdf)

    pdf.output('test.pdf')
