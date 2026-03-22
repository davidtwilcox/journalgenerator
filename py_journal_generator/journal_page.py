from typing import Tuple

from py_journal_generator.pdf import PDF


class JournalPage:
    def __init__(self, page_size: Tuple[float, float], margins: Tuple[float, float, float, float]):
        self.width: float = page_size[0]
        self.height: float = page_size[1]

        self.top_margin: float = margins[0]
        self.right_margin: float = margins[1]
        self.bottom_margin: float = margins[2]
        self.left_margin: float = margins[3]

        self.content_width: float = self.width - (self.right_margin + self.left_margin)
        self.content_height: float = self.height - (self.bottom_margin + self.top_margin)

    def render(self, pdf: PDF):
        pass
