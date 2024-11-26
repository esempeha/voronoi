from geometry import Geometry
from bounding_box import BoundingBox
from cell import Cell
from line import Line
from point import Point

class VoronoiDiagram:
    """Kelas untuk konstruksi diagram voronoi dengan menggunakan voronoi cell dan garis bisector."""

    def __init__(self, max_dimension):
        """Constructor diagram Voronoi dengan ukuran maksimum tertentu."""
        self.boundary = BoundingBox(0.0, 0.0, max_dimension, max_dimension)
        self.cells = []
        self.id_cell = 0
        self.setup()

    def setup(self):
        """Membentuk cell awal di luar area bounding box."""

        # minimum, maksimum, dan range dari bounding box
        x_min, y_min = self.boundary.x_min, self.boundary.y_min
        x_max, y_max = self.boundary.x_max, self.boundary.y_max
        x_range, y_range = x_max - x_min, y_max - y_min

        # perbesar area untuk super triangle
        x_super, y_super = x_range * 4, y_range * 4

        # membuat bounding box yang lebih besar untuk garis bisector
        x_min_bisect = x_min - x_super * 3
        y_min_bisect = y_min - y_super * 3
        x_max_bisect = x_max + x_super * 3
        y_max_bisect = y_max + y_super * 3
        self.bisector_bound = BoundingBox(x_min_bisect, y_min_bisect, x_max_bisect, y_max_bisect)

        # initialize bounding box awal
        x_min_init = x_min - x_super * 4
        y_min_init = y_min - y_super * 4
        x_max_init = x_max + x_super * 4
        y_max_init = y_max + y_super * 4
        init_bound = BoundingBox(x_min_init, y_min_init, x_max_init, y_max_init)

        # tiga titik yang membentuk super triangle
        p1 = Point(x_min + x_range / 2, y_min - y_super + y_range / 2) # atas tengah dari bounding box super
        p2 = Point(x_max + x_super - x_range / 2, y_max + y_super - y_super / 2) # kanan bawah bounding box super
        p3 = Point(x_min - x_super + x_range / 2, y_max + y_super - y_super / 2) # kiri bawah bounding box super

        # buat voronoi cell untuk ketiga titik
        c1 = Cell(p1, self.id_cell)
        self.id_cell += 1
        c2 = Cell(p2, self.id_cell)
        self.id_cell += 1
        c3 = Cell(p3, self.id_cell)
        self.id_cell += 1

        # buat bisector untuk pasangan setiap titik
        l1 = Line(p1, p2).bisector(init_bound)
        l2 = Line(p2, p3).bisector(init_bound)
        l3 = Line(p1, p3).bisector(init_bound)

        # titik potong antara bisector
        i1 = l1.intersection(l2)
        i2 = l2.intersection(l3)
        i3 = l1.intersection(l3)

        # garis untuk setiap cell
        c1.borders.append(Line(l1.start, i1, c2))
        c2.borders.append(Line(l1.start, i1, c1))
        c2.borders.append(Line(i2, l2.end, c3))
        c3.borders.append(Line(i2, l2.end, c2))
        c1.borders.append(Line(l3.start, i3, c3))
        c3.borders.append(Line(l3.start, i3, c1))

        # simpan voronoi cell
        self.add_cell(c1)
        self.add_cell(c2)
        self.add_cell(c3)

    def add_cell(self, c):
        """Menambahkan cell ke dalam list of Voronoi cell."""
        self.cells.append(c)

    def add_point(self, p):
        """Menambahkan titik baru ke diagram Voronoi dan membentuk cell baru."""
        new_cell = Cell(p, self.id_cell)
        self.id_cell += 1
        first = self.find_cell(p)
        
        # jika titik sudah ada
        if p == first.site:
            return False

        visited = {}
        current_cell = first

        # membagi cell-cell yang terpengaruh oleh site/titik baru
        while True:
            hp = Line(p, current_cell.site).bisector(self.bisector_bound) # membentuk garis bisector baru antara titik baru dan generator dari cell yang sedang diproses
            i1 = None
            l1 = None
            new_border = []
            num_intersections = 0
            next_cell = None

            # cari intersection antara bisector baru dengan garis batas cell
            for current_line in current_cell.borders:
                intersection = hp.intersection(current_line)
                if intersection:
                    num_intersections += 1
                    
                    if i1 is None:
                        i1 = intersection
                        l1 = current_line
                    
                    else:
                        # tentukan arah dan neighbor dari garis baru yang terbentuk
                        if Geometry.cross_product(i1, intersection, p) > 0:
                            new_cell.borders.append(Line(i1, intersection, current_cell))
                            new_border.append(Line(i1, intersection, new_cell))
                            next_cell = current_line.neighbor
                        else:
                            new_cell.borders.append(Line(intersection, i1, current_cell))
                            new_border.append(Line(intersection, i1, new_cell))
                            next_cell = l1.neighbor

                        tmp = current_line.start if Geometry.closer_to(current_line.start, p, current_cell.site) == current_cell.site else current_line.end
                        new_border.append(Line(intersection, tmp, current_line.neighbor))
                        tmp = l1.start if Geometry.closer_to(l1.start, p, current_cell.site) == current_cell.site else l1.end
                        new_border.append(Line(i1, tmp, l1.neighbor))

                # tambahkan garis boundary yang tidak terpengaruh
                if (Geometry.closer_to(current_line.start, current_cell.site, p) == current_cell.site
                    and Geometry.closer_to(current_line.end, current_cell.site, p) == current_cell.site):
                    new_border.append(current_line)

            # validasi jumlah intersection (harusnya ada 2)
            if num_intersections != 2:
                for k, borders in visited.items():
                    k.borders = borders
                return False
            elif current_cell in visited:
                for k, borders in visited.items():
                    k.borders = borders
                return False

            # simpan cell yang sudah diproses
            visited[current_cell] = current_cell.borders
            current_cell.borders = new_border
            current_cell = next_cell

            if current_cell == first:
                break

        self.add_cell(new_cell)
        return True
    
    def find_cell(self, p):
        """Mencari cell yang paling dekat dengan titik yang diberikan."""
        current_cell = self.cells[-1]
        best = Geometry.dist_squared(current_cell.site, p)
        old = float('inf')

        # loop sampai tidak ditemukan cell yang lebih dekat
        while old > best:
            old = best
            for vl in current_cell.borders:
                dist = Geometry.dist_squared(vl.neighbor.site, p)
                if dist < best:
                    current_cell = vl.neighbor
                    best = dist

        return current_cell

    def get_cells(self):
        """Mengembalikan semua cell yang ada di diagram Voronoi."""
        return self.cells

    def get_size(self):
        """Mendapatkan ukuran dari bounding box."""
        return self.boundary.x_max
    
    def clear(self):
        """Menghapus semua cell yang ada dan menginisialisasi ulang diagram Voronoi."""
        self.cells = []
        self.id_cell = 0
        self.setup()