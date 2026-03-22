import pytest

from py_journal_generator.journal_page import JournalPage


@pytest.fixture
def page():
    # top, right, bottom, left
    return JournalPage(page_size=(148.0, 210.0), margins=(4.5, 4.5, 4.5, 10.0))


class TestJournalPageDimensions:
    def test_width(self, page):
        assert page.width == pytest.approx(148.0)

    def test_height(self, page):
        assert page.height == pytest.approx(210.0)


class TestJournalPageMargins:
    def test_top_margin(self, page):
        assert page.top_margin == pytest.approx(4.5)

    def test_right_margin(self, page):
        assert page.right_margin == pytest.approx(4.5)

    def test_bottom_margin(self, page):
        assert page.bottom_margin == pytest.approx(4.5)

    def test_left_margin(self, page):
        assert page.left_margin == pytest.approx(10.0)


class TestJournalPageContentArea:
    def test_content_width(self, page):
        assert page.content_width == pytest.approx(148.0 - 4.5 - 10.0)

    def test_content_height(self, page):
        assert page.content_height == pytest.approx(210.0 - 4.5 - 4.5)

    def test_content_width_symmetric_margins(self):
        p = JournalPage((100.0, 200.0), (10.0, 10.0, 10.0, 10.0))
        assert p.content_width == pytest.approx(80.0)

    def test_content_height_symmetric_margins(self):
        p = JournalPage((100.0, 200.0), (10.0, 10.0, 10.0, 10.0))
        assert p.content_height == pytest.approx(180.0)
