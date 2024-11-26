from bounding_box import BoundingBox
from point import Point

class Line:
    """Kelas untuk merepresentasikan (segmen) garis pada diagram voronoi."""

    EPSILON = 1e-7 # untuk toleransi floating point

    def __init__(self, start: Point, end: Point, neighbor = None):
        """Konstruktor untuk kelas Line."""
        self.start = start
        self.end = end
        self.neighbor = neighbor

    def __str__(self):
        """Mengembalikan representasi string untuk garis, dengan format [start -> end]"""
        return f"[{self.start} -> {self.end}]"

    def bisector(self, bounding_box: BoundingBox):
        """Menghitung garis bisector antara dua titik pada boundary bounding box."""
        return self.bisector_coords(bounding_box.x_min, bounding_box.y_min, bounding_box.x_max, bounding_box.y_max)

    def bisector_coords(self, x_min: float, y_min: float, x_max: float, y_max: float):
        """Menghitung bisektor garis antara dua titik pada batas-batas boundary box."""
        
        # hitung mid point
        x_mid = (self.start.x + self.end.x) / 2
        y_mid = (self.start.y + self.end.y) / 2
        
        # kalo garis vertikal, berarti bisectornya horizontal
        if abs(self.start.x - self.end.x) < self.EPSILON:
            return Line(Point(x_min, y_mid), Point(x_max, y_mid))
        
        # kalo garis horizontal, berarti bisectornya vertikal
        elif abs(self.start.y - self.end.y) < self.EPSILON:
            return Line(Point(x_mid, y_min), Point(x_mid, y_max))
        
        # persamaan garis untuk bisector (y = mx + c)
        m = -(self.end.x - self.start.x) / (self.end.y - self.start.y)
        c = y_mid - (m * x_mid)
        
        # find titik intersection, i.e. (x1, y1) dengan bounding box
        x1 = (y_min - c) / m
        y1 = y_min

        # perika sapakah x1,y1 di dalam bounding box. jika tidak, pindahkan ke ujung bounding box
        if x1 < x_min:
            x1 = x_min
            y1 = m * x_min + c
        elif x1 > x_max:
            x1 = x_max
            y1 = m * x_max + c

        # find intersection satunya lagi (x2, y2) dengan bounding box
        x2 = (y_max - c) / m
        y2 = y_max

        # perika apakah x2,y2 di dalam bounding box. jika tidak, pindahkan ke ujung bounding box
        if x2 < x_min:
            x2 = x_min
            y2 = m * x_min + c
        elif x2 > x_max:
            x2 = x_max
            y2 = m * x_max + c

        return Line(Point(x1, y1), Point(x2, y2)) # garis bisector

    def intersection(self, l):
        """Menghitung titik potong antara dua garis."""

        # compute determinan yang terbentuk antara 2 garis unutk menentukan bersilangan atau sejajar
        det = (self.start.x - self.end.x) * (l.start.y - l.end.y) - (self.start.y - self.end.y) * (l.start.x - l.end.x)

        # kalo det == 0, berarti sejajar/berimpit (tidak ada titik potong) -> tidak ada intersection
        if abs(det) <= self.EPSILON:
            return None
        
        # menghitung konstanta persamaan garis
        a = (self.start.x * self.end.y - self.start.y * self.end.x)
        b = (l.start.x * l.end.y - l.start.y * l.end.x)

        # hitung koordinat titik potong
        x = (a * (l.start.x - l.end.x) - (self.start.x - self.end.x) * b) / det
        y = (a * (l.start.y - l.end.y) - (self.start.y - self.end.y) * b) / det
        
        # jika titik potong x tidak dalam rentang kedua segmen garis
        if ((x + self.EPSILON < min(self.start.x, self.end.x))
            or (x - self.EPSILON > max(self.start.x, self.end.x))
            or (x + self.EPSILON < min(l.start.x, l.end.x))
            or (x - self.EPSILON > max(l.start.x, l.end.x))):
            return None
        # jik titik potong y tidak dalam rentang kedua segmen garis
        elif ((y + self.EPSILON < min(self.start.y, self.end.y))
              or (y - self.EPSILON > max(self.start.y, self.end.y))
              or (y + self.EPSILON < min(l.start.y, l.end.y))
              or (y - self.EPSILON > max(l.start.y, l.end.y))):
            return None
        # jika x dan y berada dalam rentang kedua segmen garis
        else:
            return Point(x, y)