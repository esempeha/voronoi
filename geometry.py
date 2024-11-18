import math
from point import Point

class Geometry:
    """Kelas untuk operasi geometri yang diperlukan."""

    EPSILON = 1e-7  # toleransi untuk floating point

    @staticmethod
    def closer_to(to: Point, p1: Point, p2: Point) -> Point:
        """Mengembalikan titik yang lebih dekat ke 'to' antara p1 dan p2."""
        d1 = Geometry.dist_squared(to, p1)
        d2 = Geometry.dist_squared(to, p2)
        return p1 if d1 < d2 else p2

    @staticmethod
    def cross_product(p1: Point, p2: Point, p3: Point) -> float:
        """Menghitung cross product (p1 -> p2) x (p1 -> p3)."""
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

    @staticmethod
    def distance(p1: Point, p2: Point) -> float:
        """Menghitung jarak antara p1 dan p2."""
        return math.sqrt(Geometry.dist_squared(p1, p2))

    @staticmethod
    def dist_squared(p1: Point, p2: Point) -> float:
        """Menghitung jarak squared antara p1 dan p2."""
        return (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2