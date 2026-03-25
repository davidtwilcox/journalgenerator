import math
from typing import List, Tuple


class Hexagon:
    def __init__(self, width: float):
        self.side_length: float = (2 / math.sqrt(3)) * (width / 2.0)
        self.short_diagonal: float = width
        self.long_diagonal: float = self.side_length * 2.0
        self.apothem: float = width / 2.0
        self.three_quarter_height: float = self.side_length + (self.side_length / 2.0)

    def get_coords(self, top_left: Tuple[float, float]) -> List[Tuple[float, float]]:
        half_length: float = self.side_length / 2.0
        p0: Tuple[float, float] = (top_left[0], top_left[1] + half_length)
        p1: Tuple[float, float] = (p0[0] + self.apothem, top_left[1])
        p2: Tuple[float, float] = (p1[0] + self.apothem, p0[1])
        p3: Tuple[float, float] = (p2[0], p2[1] + self.side_length)
        p4: Tuple[float, float] = (p1[0], p3[1] + half_length)
        p5: Tuple[float, float] = (top_left[0], p3[1])
        return [p0, p1, p2, p3, p4, p5]
