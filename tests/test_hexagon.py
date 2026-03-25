import math

import pytest

from py_journal_generator.hexagon import Hexagon


@pytest.fixture
def hex10():
    return Hexagon(10.0)


class TestHexagonDimensions:
    def test_short_diagonal(self, hex10):
        assert hex10.short_diagonal == pytest.approx(10.0)

    def test_long_diagonal(self, hex10):
        assert hex10.long_diagonal == pytest.approx(20.0 / math.sqrt(3))

    def test_apothem(self, hex10):
        assert hex10.apothem == pytest.approx(hex10.short_diagonal / 2.0)

    def test_three_quarter_height(self, hex10):
        assert hex10.three_quarter_height == pytest.approx(5.0 * math.sqrt(3))


class TestHexagonCoords:
    def test_returns_six_vertices(self, hex10):
        coords = hex10.get_coords((0.0, 0.0))
        assert len(coords) == 6

    def test_all_vertices_are_tuples_of_two_floats(self, hex10):
        for x, y in hex10.get_coords((0.0, 0.0)):
            assert isinstance(x, float)
            assert isinstance(y, float)

    def test_leftmost_vertex_at_top_left_x(self, hex10):
        top_left = (5.0, 3.0)
        coords = hex10.get_coords(top_left)
        # p0 and p5 are on the left edge (x == top_left[0])
        assert coords[0][0] == pytest.approx(top_left[0])
        assert coords[5][0] == pytest.approx(top_left[0])

    def test_topmost_vertex_at_top_left_y(self, hex10):
        top_left = (5.0, 3.0)
        coords = hex10.get_coords(top_left)
        # p1 is the top vertex (y == top_left[1])
        assert coords[1][1] == pytest.approx(top_left[1])

    def test_width_equals_short_diagonal(self, hex10):
        coords = hex10.get_coords((0.0, 0.0))
        xs = [p[0] for p in coords]
        assert max(xs) - min(xs) == pytest.approx(hex10.short_diagonal)

    def test_height_equals_long_diagonal(self, hex10):
        coords = hex10.get_coords((0.0, 0.0))
        ys = [p[1] for p in coords]
        assert max(ys) - min(ys) == pytest.approx(hex10.long_diagonal)

    def test_offset_shifts_all_vertices(self, hex10):
        base = hex10.get_coords((0.0, 0.0))
        shifted = hex10.get_coords((10.0, 5.0))
        for (bx, by), (sx, sy) in zip(base, shifted):
            assert sx == pytest.approx(bx + 10.0)
            assert sy == pytest.approx(by + 5.0)
