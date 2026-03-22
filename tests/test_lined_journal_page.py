import pytest
from unittest.mock import MagicMock, call
from py_journal_generator.lined_journal_page import LinedJournalPage


PAGE_SIZE = (148.0, 210.0)
MARGINS = (4.5, 4.5, 4.5, 10.0)
LINE_WIDTH = 0.1
LINE_HEIGHT = 8.0


@pytest.fixture
def page():
    return LinedJournalPage(PAGE_SIZE, MARGINS, LINE_WIDTH, LINE_HEIGHT)


@pytest.fixture
def pdf():
    return MagicMock()


class TestLinedJournalPageInit:
    def test_line_width(self, page):
        assert page.line_width == pytest.approx(LINE_WIDTH)

    def test_line_height(self, page):
        assert page.line_height == pytest.approx(LINE_HEIGHT)


class TestLinedJournalPageRender:
    def test_adds_page(self, page, pdf):
        page.render(pdf)
        pdf.add_page.assert_called_once()

    def test_sets_line_width(self, page, pdf):
        page.render(pdf)
        pdf.set_line_width.assert_called_once_with(LINE_WIDTH)

    def test_draws_correct_number_of_lines(self, page, pdf):
        page.render(pdf)
        expected_lines = int(page.content_height / LINE_HEIGHT) + 1
        assert pdf.line.call_count == expected_lines

    def test_lines_span_content_width(self, page, pdf):
        page.render(pdf)
        for c in pdf.line.call_args_list:
            x1, _y1, x2, _y2 = c.args
            assert x1 == pytest.approx(page.left_margin)
            assert x2 == pytest.approx(page.width - page.right_margin)

    def test_first_line_y_position(self, page, pdf):
        page.render(pdf)
        _x1, y1, _x2, _y2 = pdf.line.call_args_list[0].args
        assert y1 == pytest.approx(page.top_margin + LINE_HEIGHT)

    def test_lines_evenly_spaced(self, page, pdf):
        page.render(pdf)
        ys = [c.args[1] for c in pdf.line.call_args_list]
        gaps = [ys[i + 1] - ys[i] for i in range(len(ys) - 1)]
        for gap in gaps:
            assert gap == pytest.approx(LINE_HEIGHT)
