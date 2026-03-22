import pytest
from unittest.mock import MagicMock
from py_journal_generator.hex_map_journal_page import HexMapJournalPage
from py_journal_generator.hexagon import Hexagon


PAGE_SIZE = (148.0, 210.0)
MARGINS = (4.5, 4.5, 4.5, 10.0)
HEX_SIZE = 7.5


@pytest.fixture
def page():
    return HexMapJournalPage(PAGE_SIZE, MARGINS, HEX_SIZE)


@pytest.fixture
def page_with_labels():
    return HexMapJournalPage(PAGE_SIZE, MARGINS, HEX_SIZE, has_labels=True)


@pytest.fixture
def pdf():
    mock = MagicMock()
    mock.get_string_width.return_value = 5.0
    return mock


class TestHexMapJournalPageInit:
    def test_hex_size(self, page):
        assert page.hex_size == pytest.approx(HEX_SIZE)

    def test_has_labels_defaults_false(self, page):
        assert page.has_labels is False

    def test_has_labels_true(self, page_with_labels):
        assert page_with_labels.has_labels is True


class TestHexMapJournalPageRender:
    def test_adds_page(self, page, pdf):
        page.render(pdf)
        pdf.add_page.assert_called_once()

    def test_draws_polygons(self, page, pdf):
        page.render(pdf)
        assert pdf.polygon.call_count > 0

    def test_each_polygon_has_six_vertices(self, page, pdf):
        page.render(pdf)
        for c in pdf.polygon.call_args_list:
            coords = c.args[0]
            assert len(coords) == 6

    def test_expected_polygon_count(self, page, pdf):
        page.render(pdf)
        hexagon = Hexagon(HEX_SIZE)
        expected_rows = int(
            (page.content_height - hexagon.three_quarter_height) / hexagon.three_quarter_height
        )
        expected_cols = int(page.content_width / hexagon.short_diagonal) - 1
        assert pdf.polygon.call_count == expected_rows * expected_cols

    def test_no_cell_calls_without_labels(self, page, pdf):
        page.render(pdf)
        pdf.cell.assert_not_called()

    def test_cell_calls_with_labels(self, page_with_labels, pdf):
        page_with_labels.render(pdf)
        assert pdf.cell.call_count > 0
