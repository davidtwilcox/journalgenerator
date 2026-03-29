from typing import Tuple

from py_journal_generator.journal_page import JournalPage
from py_journal_generator.pdf import PDF


class SquareJournalPage(JournalPage):
    def __init__(self,
                 page_size: Tuple[float, float],
                 margins: Tuple[float, float, float, float],
                 line_width: float,
                 square_size: float):
        super().__init__(page_size, margins)
        self.line_width = line_width
        self.square_size = square_size

    def render(self, pdf: PDF):
        pdf.add_page()
        pdf.set_line_width(self.line_width)
        rows: int = int(self.content_height / self.square_size) + 1
        cols: int = int(self.content_width / self.square_size) + 1
        last_x: float = self.left_margin + (float(cols - 1) * self.square_size)
        last_y: float = self.top_margin + (float(rows - 1) * self.square_size)
        for r in range(0, rows):
            y: float = self.top_margin + (float(r) * self.square_size)
            pdf.line(self.left_margin, y, last_x, y)
        for c in range(0, cols):
            x: float = self.left_margin + (float(c) * self.square_size)
            pdf.line(x, self.top_margin, x, last_y)
