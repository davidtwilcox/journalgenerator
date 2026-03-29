from unittest.mock import MagicMock

import pytest

from py_journal_generator.square_journal_page import SquareJournalPage

PAGE_SIZE = (148.0, 210.0)
MARGINS = (4.5, 4.5, 4.5, 10.0)
LINE_WIDTH = 0.1
SQUARE_SIZE = 5.0


@pytest.fixture
def page():
    return SquareJournalPage(PAGE_SIZE, MARGINS, LINE_WIDTH, SQUARE_SIZE)


@pytest.fixture
def pdf():
    return MagicMock()


class TestSquareJournalPageInit:
    def test_line_width(self, page):
        assert page.line_width == pytest.approx(LINE_WIDTH)

    def test_square_size(self, page):
        assert page.square_size == pytest.approx(SQUARE_SIZE)


class TestSquareJournalPageRender:
    def test_adds_page(self, page, pdf):
        page.render(pdf)
        pdf.add_page.assert_called_once()

    def test_sets_line_width(self, page, pdf):
        page.render(pdf)
        pdf.set_line_width.assert_called_once_with(LINE_WIDTH)

    def test_total_line_count(self, page, pdf):
        page.render(pdf)
        expected_rows = int(page.content_height / SQUARE_SIZE) + 1
        expected_cols = int(page.content_width / SQUARE_SIZE) + 1
        assert pdf.line.call_count == expected_rows + expected_cols

    def test_horizontal_lines_start_at_top_margin(self, page, pdf):
        page.render(pdf)
        first_call = pdf.line.call_args_list[0]
        _x1, y1, _x2, _y2 = first_call.args
        assert y1 == pytest.approx(page.top_margin)

    def test_horizontal_lines_evenly_spaced(self, page, pdf):
        page.render(pdf)
        rows = int(page.content_height / SQUARE_SIZE) + 1
        ys = [pdf.line.call_args_list[r].args[1] for r in range(rows)]
        gaps = [ys[i + 1] - ys[i] for i in range(len(ys) - 1)]
        for gap in gaps:
            assert gap == pytest.approx(SQUARE_SIZE)

    def test_horizontal_lines_span_full_width(self, page, pdf):
        page.render(pdf)
        rows = int(page.content_height / SQUARE_SIZE) + 1
        cols = int(page.content_width / SQUARE_SIZE) + 1
        expected_last_x = page.left_margin + float(cols - 1) * SQUARE_SIZE
        for r in range(rows):
            x1, _y1, x2, _y2 = pdf.line.call_args_list[r].args
            assert x1 == pytest.approx(page.left_margin)
            assert x2 == pytest.approx(expected_last_x)

    def test_vertical_lines_start_at_left_margin(self, page, pdf):
        page.render(pdf)
        rows = int(page.content_height / SQUARE_SIZE) + 1
        first_vertical = pdf.line.call_args_list[rows]
        x1, _y1, _x2, _y2 = first_vertical.args
        assert x1 == pytest.approx(page.left_margin)

    def test_vertical_lines_evenly_spaced(self, page, pdf):
        page.render(pdf)
        rows = int(page.content_height / SQUARE_SIZE) + 1
        cols = int(page.content_width / SQUARE_SIZE) + 1
        xs = [pdf.line.call_args_list[rows + c].args[0] for c in range(cols)]
        gaps = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
        for gap in gaps:
            assert gap == pytest.approx(SQUARE_SIZE)

    def test_vertical_lines_span_full_height(self, page, pdf):
        page.render(pdf)
        rows = int(page.content_height / SQUARE_SIZE) + 1
        cols = int(page.content_width / SQUARE_SIZE) + 1
        expected_last_y = page.top_margin + float(rows - 1) * SQUARE_SIZE
        for c in range(cols):
            _x1, y1, _x2, y2 = pdf.line.call_args_list[rows + c].args
            assert y1 == pytest.approx(page.top_margin)
            assert y2 == pytest.approx(expected_last_y)

    def test_no_cell_calls(self, page, pdf):
        page.render(pdf)
        pdf.cell.assert_not_called()
