from typing import Tuple

from py_journal_generator.journal_page import JournalPage
from py_journal_generator.pdf import PDF


class DotJournalPage(JournalPage):
    def __init__(self,
                 page_size: Tuple[float, float],
                 margins: Tuple[float, float, float, float],
                 dot_width: float,
                 dot_space: float):
        super().__init__(page_size, margins)
        self.dot_width: float = dot_width
        self.dot_space: float = dot_space

    def render(self, pdf: PDF):
        pdf.add_page()
        pdf.set_line_width(self.dot_width)
        rows: int = int(self.content_height / self.dot_space)
        cols: int = int(self.content_width / self.dot_space) + 1
        for r in range(0, rows):
            y: float = self.top_margin + ((float(r) + 1.0) * self.dot_space)
            for c in range(0, cols):
                pdf.ellipse(self.left_margin + (float(c) * self.dot_space), y, self.dot_width, self.dot_width, 'DF')
