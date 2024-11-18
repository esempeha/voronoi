class Point:
    """Kelas ini digunakan untuk merepresentasikan titik pada koordinat kartesius (x, y)."""

    EPSILON = 1e-7 # toleransi untuk floating point

    def __init__(self, x: float, y: float):
        """Inisialisasi objek Point dengan koordinat x dan y."""
        self.x = x
        self.y = y

    def __str__(self):
        """Mengembalikan representasi string dari objek Point."""
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        """Membandingkan apakah dua objek Point memiliki koordinat yang 'hampir' sama."""
        if not isinstance(other, Point):
            return False
        return (abs(self.x - other.x) < self.EPSILON) and (abs(self.y - other.y) < self.EPSILON)