import math
cos = lambda r: round(math.cos(r), 10)
sin = lambda r: round(math.sin(r), 10)
pi = math.pi


class Circle:
    def __init__(self, center: tuple[int, int], radius: int, std_deg: float = 0):
        self._center = center
        self._radius = radius
        self._std_deg = std_deg

    def get_coords(self, deg: float, rad_padding: float = 0) -> tuple[int, int]:
        deg = self._std_deg + deg
        rad = (pi / 180) * deg
        radius = self._radius + rad_padding
        x, y = radius * cos(rad), radius * sin(rad)

        x += self._center[0]
        y += self._center[1]

        return (x, y)
