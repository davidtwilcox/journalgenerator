from typing import Tuple

from py_journal_generator.hexagon import Hexagon
from py_journal_generator.journal_page import JournalPage
from py_journal_generator.pdf import PDF


class HexMapJournalPage(JournalPage):
    def __init__(self,
                 page_size: Tuple[float, float],
                 margins: Tuple[float, float, float, float],
                 hex_size: float,
                 has_labels: bool = False):
        super().__init__(page_size, margins)
        self.hex_size: float = hex_size
        self.has_labels: bool = has_labels

    def render(self, pdf: PDF):
        pdf.add_page()
        pdf.set_font('Courier', '', 10)
        hexagon: Hexagon = Hexagon(self.hex_size)
        y_offset: float = 7.5 if self.has_labels else 0.0
        rows: int = \
            int((self.content_height - y_offset - hexagon.three_quarter_height) / hexagon.three_quarter_height)
        if self.has_labels:
            rows -= 1
        cols: int = int(self.content_width / hexagon.short_diagonal) - 1
        x_offset: float = self.left_margin + pdf.get_string_width(str(rows + 1)) + 2.5 if self.has_labels \
            else self.left_margin
        if self.has_labels:
            for c in range(0, cols):
                label: str = str(c + 1)
                pdf.set_x(x_offset + hexagon.short_diagonal * float(c))
                pdf.cell(int(hexagon.short_diagonal), 0, label, 0, 0, 'C')
        for r in range(0, rows):
            indent: float = 0.0 if r % 2 == 0 else hexagon.apothem
            if self.has_labels:
                label: str = str(r + 1)
                pdf.set_xy(self.left_margin, y_offset + self.top_margin + (r * hexagon.three_quarter_height))
                pdf.cell(int(x_offset), int(hexagon.long_diagonal), label, 0, 0, 'L')
            for c in range(0, cols):
                top_left: Tuple[float, float] = (
                    x_offset + indent + (float(c) * hexagon.short_diagonal),
                    (y_offset + self.top_margin + (r * hexagon.three_quarter_height)))
                pdf.polygon(hexagon.get_coords(top_left))