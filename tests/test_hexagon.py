import math

import pytest

from py_journal_generator.hexagon import Hexagon


@pytest.fixture
def hex10():
    return Hexagon(10.0)


@pytest.fixture
def hex10_rotated():
    return Hexagon(10.0, rotated=True)


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


class TestHexagonRotatedFlag:
    def test_rotated_false_by_default(self, hex10):
        assert hex10.rotated is False

    def test_rotated_true_when_set(self, hex10_rotated):
        assert hex10_rotated.rotated is True


class TestHexagonRotatedCoords:
    def test_returns_six_vertices(self, hex10_rotated):
        assert len(hex10_rotated.get_coords((0.0, 0.0))) == 6

    def test_all_vertices_are_tuples_of_two_floats(self, hex10_rotated):
        for x, y in hex10_rotated.get_coords((0.0, 0.0)):
            assert isinstance(x, float)
            assert isinstance(y, float)

    def test_leftmost_vertex_at_top_left_x(self, hex10_rotated):
        top_left = (5.0, 3.0)
        coords = hex10_rotated.get_coords(top_left)
        # p0 is the leftmost vertex
        assert coords[0][0] == pytest.approx(top_left[0])

    def test_topmost_vertices_at_top_left_y(self, hex10_rotated):
        top_left = (5.0, 3.0)
        coords = hex10_rotated.get_coords(top_left)
        # p1 and p2 share the topmost y
        assert coords[1][1] == pytest.approx(top_left[1])
        assert coords[2][1] == pytest.approx(top_left[1])

    def test_width_equals_two_apothems_plus_side_length(self, hex10_rotated):
        coords = hex10_rotated.get_coords((0.0, 0.0))
        xs = [p[0] for p in coords]
        expected = 2 * hex10_rotated.apothem + hex10_rotated.side_length
        assert max(xs) - min(xs) == pytest.approx(expected)

    def test_height_equals_half_length_plus_apothem(self, hex10_rotated):
        coords = hex10_rotated.get_coords((0.0, 0.0))
        ys = [p[1] for p in coords]
        expected = hex10_rotated.side_length / 2.0 + hex10_rotated.apothem
        assert max(ys) - min(ys) == pytest.approx(expected)

    def test_offset_shifts_all_vertices(self, hex10_rotated):
        base = hex10_rotated.get_coords((0.0, 0.0))
        shifted = hex10_rotated.get_coords((10.0, 5.0))
        for (bx, by), (sx, sy) in zip(base, shifted):
            assert sx == pytest.approx(bx + 10.0)
            assert sy == pytest.approx(by + 5.0)
