from typing import Tuple

from py_journal_generator.journal_page import JournalPage
from py_journal_generator.pdf import PDF


class LinedJournalPage(JournalPage):
    def __init__(self,
                 page_size: Tuple[float, float],
                 margins: Tuple[float, float, float, float],
                 line_width: float,
                 line_height: float):
        super().__init__(page_size, margins)
        self.line_width: float = line_width
        self.line_height: float = line_height

    def render(self, pdf: PDF):
        pdf.add_page()
        pdf.set_line_width(self.line_width)
        for r in range(0, int(self.content_height / self.line_height) + 1):
            y: float = self.top_margin + ((float(r) + 1.0) * self.line_height)
            pdf.line(self.left_margin, y, self.width - self.right_margin, y)
