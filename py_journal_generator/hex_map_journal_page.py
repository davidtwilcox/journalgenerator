from typing import Tuple

from py_journal_generator.hexagon import Hexagon
from py_journal_generator.journal_page import JournalPage
from py_journal_generator.pdf import PDF


class HexMapJournalPage(JournalPage):
    def __init__(self,
                 page_size: Tuple[float, float],
                 margins: Tuple[float, float, float, float],
                 hex_size: float,
                 line_width: float,
                 rotated: bool = False) -> None:
        super().__init__(page_size, margins)
        self.hex_size: float = hex_size
        self.line_width: float = line_width
        self.rotated: bool = rotated

    def render(self, pdf: PDF):
        pdf.add_page()
        pdf.set_line_width(self.line_width)
        hexagon: Hexagon = Hexagon(self.hex_size, self.rotated)
        rows: int = 0
        cols: int = 0
        if self.rotated:
            rows = int(self.content_height / hexagon.apothem) - 1
        else:
            rows = \
                int((self.content_height - hexagon.three_quarter_height) / hexagon.three_quarter_height)
        if self.rotated:
            cols = int(self.content_width / (hexagon.three_quarter_height * 2.0))
        else:
            cols = int(self.content_width / hexagon.width) - 1
        x_offset: float = self.left_margin
        for r in range(0, rows):
            indent: float = 0.0
            if self.rotated:
                indent = 0.0 if r % 2 == 0 else hexagon.three_quarter_height
            else:
                indent = 0.0 if r % 2 == 0 else hexagon.apothem
            for c in range(0, cols):
                top_left: Tuple[float, float] = (0.0, 0.0)
                if self.rotated:
                    top_left = (x_offset + indent + (float(c) * hexagon.side_length) + (float(c) * hexagon.long_diagonal),
                                (self.top_margin + (r * hexagon.apothem)))
                else:
                    top_left = (x_offset + indent + (float(c) * hexagon.short_diagonal),
                        (self.top_margin + (r * hexagon.three_quarter_height)))
                pdf.polygon(hexagon.get_coords(top_left))
