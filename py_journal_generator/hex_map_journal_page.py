from typing import Tuple

from py_journal_generator.hexagon import Hexagon
from py_journal_generator.journal_page import JournalPage
from py_journal_generator.pdf import PDF


class HexMapJournalPage(JournalPage):
    def __init__(self,
                 page_size: Tuple[float, float],
                 margins: Tuple[float, float, float, float],
                 hex_size: float):
        super().__init__(page_size, margins)
        self.hex_size: float = hex_size

    def render(self, pdf: PDF):
        pdf.add_page()
        hexagon: Hexagon = Hexagon(self.hex_size)
        rows: int = \
            int((self.content_height - hexagon.three_quarter_height) / hexagon.three_quarter_height)
        cols: int = int(self.content_width / hexagon.short_diagonal) - 1
        x_offset: float = self.left_margin
        for r in range(0, rows):
            indent: float = 0.0 if r % 2 == 0 else hexagon.apothem
            for c in range(0, cols):
                top_left: Tuple[float, float] = (
                    x_offset + indent + (float(c) * hexagon.short_diagonal),
                    (self.top_margin + (r * hexagon.three_quarter_height)))
                pdf.polygon(hexagon.get_coords(top_left))
