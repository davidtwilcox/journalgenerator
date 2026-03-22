import math
from typing import List, Tuple

class Hexagon:
    def __init__(self, side_length: float):
        self.side_length: float = side_length
        self.short_diagonal: float = math.sqrt(3) * side_length
        self.long_diagonal: float = side_length * 2.0
        self.apothem: float = self.short_diagonal / 2.0
        self.three_quarter_height: float = side_length + (side_length / 2.0)

    def get_coords(self, top_left: Tuple[float, float]) -> List[Tuple[float, float]]:
        half_length: float = self.side_length / 2.0
        p0: Tuple[float, float] = (top_left[0], top_left[1] + half_length)
        p1: Tuple[float, float] = (p0[0] + self.apothem, top_left[1])
        p2: Tuple[float, float] = (p1[0] + self.apothem, p0[1])
        p3: Tuple[float, float] = (p2[0], p2[1] + self.side_length)
        p4: Tuple[float, float] = (p1[0], p3[1] + half_length)
        p5: Tuple[float, float] = (top_left[0], p3[1])
        return [p0, p1, p2, p3, p4, p5]