from line import Line
from point import Point

class Cell:
    """Kelas ini merepresentasikan sebuah voronoi cell dengan ID unik, site, dan setiap bordersnya."""
    
    def __init__(self, site: Point, id: int):
        """Konstruktor untuk inisialisasi voronoi cell dengan site dan ID unik."""
        self.id = id
        self.site = site # tengah dari voronoi cell
        self.borders: list[Line] = []

    def __hash__(self):
        """Mengembalikan ID sebagai nilai hash agar objek Cell dapat
        digunakan dalam struktur data seperti set atau dictionary."""
        return self.id

    def __str__(self):
        """Mengembalikan representasi string dari site cell."""
        return str(self.site)
