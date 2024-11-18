import math
from itertools import combinations
from geometry import Geometry
from bounding_box import BoundingBox
from cell import Cell
from line import Line
from point import Point


class VoronoiDiagram:
    SUPER_FACTOR = 4
    INIT_BISECT_FACTOR = 4
    GENERAL_BISECT_FACTOR = 3

    def __init__(self, max_dimension):
        self.boundary = BoundingBox(0.0, 0.0, max_dimension, max_dimension)
        self.cells = []
        self.id_cell = 0
        self.setup(max_dimension)

    def setup(self, max_dimension):
        x_min, y_min = self.boundary.x_min, self.boundary.y_min
        x_max, y_max = self.boundary.x_max, self.boundary.y_max
        x_range, y_range = x_max - x_min, y_max - y_min
        x_super, y_super = x_range * self.SUPER_FACTOR, y_range * self.SUPER_FACTOR

        x_min_bisect = x_min - x_super * self.GENERAL_BISECT_FACTOR
        y_min_bisect = y_min - y_super * self.GENERAL_BISECT_FACTOR
        x_max_bisect = x_max + x_super * self.GENERAL_BISECT_FACTOR
        y_max_bisect = y_max + y_super * self.GENERAL_BISECT_FACTOR
        self.bisector_bound = BoundingBox(x_min_bisect, y_min_bisect, x_max_bisect, y_max_bisect)

        x_min_init = x_min - x_super * self.INIT_BISECT_FACTOR
        y_min_init = y_min - y_super * self.INIT_BISECT_FACTOR
        x_max_init = x_max + x_super * self.INIT_BISECT_FACTOR
        y_max_init = y_max + y_super * self.INIT_BISECT_FACTOR
        init_bound = BoundingBox(x_min_init, y_min_init, x_max_init, y_max_init)

        v1 = Point(x_min + x_range / 2, y_min - y_super + y_range / 2)
        v2 = Point(x_max + x_super - x_range / 2, y_max + y_super - y_super / 2)
        v3 = Point(x_min - x_super + x_range / 2, y_max + y_super - y_super / 2)

        c1 = Cell(v1, self.id_cell)
        self.id_cell += 1
        c2 = Cell(v2, self.id_cell)
        self.id_cell += 1
        c3 = Cell(v3, self.id_cell)
        self.id_cell += 1

        l1 = Line(v1, v2).bisector(init_bound)
        l2 = Line(v2, v3).bisector(init_bound)
        l3 = Line(v1, v3).bisector(init_bound)

        i1 = l1.intersection(l2)
        i2 = l2.intersection(l3)
        i3 = l1.intersection(l3)

        c1.borders.append(Line(l1.start, i1, c2))
        c2.borders.append(Line(l1.start, i1, c1))
        c2.borders.append(Line(i2, l2.end, c3))
        c3.borders.append(Line(i2, l2.end, c2))
        c1.borders.append(Line(l3.start, i3, c3))
        c3.borders.append(Line(l3.start, i3, c1))

        self.add_cell(c1)
        self.add_cell(c2)
        self.add_cell(c3)

    def add_cell(self, c):
        self.cells.append(c)

    def add_point(self, p):
        new_cell = Cell(p, self.id_cell)
        self.id_cell += 1
        first = self.find_cell(p)
        
        if p == first.generator:
            print(f"Trying to add duplicate point: {p}")
            return False

        visited = {}
        curr_cell = first

        while True:
            hp = Line(p, curr_cell.generator).bisector(self.bisector_bound)
            i1 = None
            l1 = None
            new_border = []
            num_intersections = 0
            next_cell = None

            for curr_line in curr_cell.borders:
                intersection = hp.intersection(curr_line)
                if intersection:
                    num_intersections += 1
                    if i1 is None:
                        i1 = intersection
                        l1 = curr_line
                    else:
                        if Geometry.cross_product(i1, intersection, p) > 0:
                            new_cell.borders.append(Line(i1, intersection, curr_cell))
                            new_border.append(Line(i1, intersection, new_cell))
                            next_cell = curr_line.neighbor
                        else:
                            new_cell.borders.append(Line(intersection, i1, curr_cell))
                            new_border.append(Line(intersection, i1, new_cell))
                            next_cell = l1.neighbor
                        tmp = curr_line.start if Geometry.closer_to(curr_line.start, p, curr_cell.generator) == curr_cell.generator else curr_line.end
                        new_border.append(Line(intersection, tmp, curr_line.neighbor))
                        tmp = l1.start if Geometry.closer_to(l1.start, p, curr_cell.generator) == curr_cell.generator else l1.end
                        new_border.append(Line(i1, tmp, l1.neighbor))

                if (Geometry.closer_to(curr_line.start, curr_cell.generator, p) == curr_cell.generator
                    and Geometry.closer_to(curr_line.end, curr_cell.generator, p) == curr_cell.generator):
                    new_border.append(curr_line)

            if num_intersections != 2:
                print(f"Skipped degenerate cell ({p.x:.2f}, {p.y:.2f}) [wrong # of intersections: {num_intersections}]")
                for k, borders in visited.items():
                    k.borders = borders
                return False
            elif curr_cell in visited:
                print(f"Skipped degenerate cell ({p.x:.2f}, {p.y:.2f}) [missed cell border]")
                for k, borders in visited.items():
                    k.borders = borders
                return False

            visited[curr_cell] = curr_cell.borders
            curr_cell.borders = new_border
            curr_cell = next_cell

            if curr_cell == first:
                break

        self.add_cell(new_cell)
        return True
    
    def find_cell(self, p):
        current = self.cells[-1]
        best = Geometry.dist_squared(current.generator, p)
        old = float('inf')

        while old > best:
            old = best
            for vl in current.borders:
                dist = Geometry.dist_squared(vl.neighbor.generator, p)
                if dist < best:
                    current = vl.neighbor
                    best = dist

        return current

    def get_cells(self):
        return self.cells

    def get_size(self):
        return self.boundary.x_max
    
    def clear(self):
        self.cells = []
        self.id_cell = 0
        self.setup(self.boundary.x_max)
