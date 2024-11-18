from point import Point

class BoundingBox:
    """Kelas ini merepresentasikan sebuah bounding box dengan koordinat batas
    (x_min, y_min) hingga (x_max, y_max) agar half-line menjadi line-segment"""

    EPSILON = 1e-7  # toleransi untuk floating point

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float):
        """Konstruktor untuk inisialisasi koordinat batas kotak."""
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def contains(self, p: Point):
        """Memeriksa apakah titik p berada di dalam bounding box."""
        return ((p.x > self.x_min - self.EPSILON) and (p.x < self.x_max + self.EPSILON)
                and (p.y > self.y_min - self.EPSILON) and (p.y < self.y_max + self.EPSILON))

    def __str__(self):
        """Mengembalikan representasi string dari bounding box."""
        return f"min=({self.x_min}, {self.y_min}), max=({self.x_max}, {self.y_max})"
