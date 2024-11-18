from point import Point

class Cell:
    """Kelas ini merepresentasikan sebuah voronoi cell dengan ID unik dan generator yang menentukan sifatnya."""
    
    def __init__(self, generator: Point, id: int):
        """Konstruktor untuk inisialisasi voronoi cell dengan generator dan ID unik."""
        self.id = id
        self.generator = generator
        self.borders = []

    def __hash__(self):
        """Mengembalikan ID sebagai nilai hash agar objek Cell dapat digunakan dalam struktur data seperti set atau dictionary."""
        return self.id

    def __str__(self):
        """Mengembalikan representasi string dari generator cell."""
        return str(self.generator)
