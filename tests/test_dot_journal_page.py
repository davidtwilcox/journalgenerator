import pytest
from unittest.mock import MagicMock
from py_journal_generator.dot_journal_page import DotJournalPage


PAGE_SIZE = (148.0, 210.0)
MARGINS = (4.5, 4.5, 4.5, 10.0)
DOT_WIDTH = 0.2
DOT_SPACE = 5.0


@pytest.fixture
def page():
    return DotJournalPage(PAGE_SIZE, MARGINS, DOT_WIDTH, DOT_SPACE)


@pytest.fixture
def pdf():
    return MagicMock()


class TestDotJournalPageInit:
    def test_dot_width(self, page):
        assert page.dot_width == pytest.approx(DOT_WIDTH)

    def test_dot_space(self, page):
        assert page.dot_space == pytest.approx(DOT_SPACE)


class TestDotJournalPageRender:
    def test_adds_page(self, page, pdf):
        page.render(pdf)
        pdf.add_page.assert_called_once()

    def test_sets_line_width(self, page, pdf):
        page.render(pdf)
        pdf.set_line_width.assert_called_once_with(DOT_WIDTH)

    def test_draws_correct_number_of_dots(self, page, pdf):
        page.render(pdf)
        expected_rows = int(page.content_height / DOT_SPACE)
        expected_cols = int(page.content_width / DOT_SPACE) + 1
        assert pdf.ellipse.call_count == expected_rows * expected_cols

    def test_dot_size_arguments(self, page, pdf):
        page.render(pdf)
        for c in pdf.ellipse.call_args_list:
            _x, _y, w, h, style = c.args
            assert w == pytest.approx(DOT_WIDTH)
            assert h == pytest.approx(DOT_WIDTH)
            assert style == 'DF'

    def test_dots_start_at_left_margin(self, page, pdf):
        page.render(pdf)
        first_row_calls = pdf.ellipse.call_args_list[:int(page.content_width / DOT_SPACE) + 1]
        assert first_row_calls[0].args[0] == pytest.approx(page.left_margin)

    def test_dots_evenly_spaced_horizontally(self, page, pdf):
        page.render(pdf)
        cols = int(page.content_width / DOT_SPACE) + 1
        first_row_xs = [pdf.ellipse.call_args_list[c].args[0] for c in range(cols)]
        gaps = [first_row_xs[i + 1] - first_row_xs[i] for i in range(len(first_row_xs) - 1)]
        for gap in gaps:
            assert gap == pytest.approx(DOT_SPACE)

    def test_dots_evenly_spaced_vertically(self, page, pdf):
        page.render(pdf)
        cols = int(page.content_width / DOT_SPACE) + 1
        rows = int(page.content_height / DOT_SPACE)
        col0_ys = [pdf.ellipse.call_args_list[r * cols].args[1] for r in range(rows)]
        gaps = [col0_ys[i + 1] - col0_ys[i] for i in range(len(col0_ys) - 1)]
        for gap in gaps:
            assert gap == pytest.approx(DOT_SPACE)
