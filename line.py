from point import Point

class Line:
    EPSILON = 1e-7

    def __init__(self, start, end, neighbor=None):
        self.start = start
        self.end = end
        self.neighbor = neighbor

    def __str__(self):
        return f"[{self.start} -> {self.end}]"

    def bisector(self, bb):
        return self.bisector_coords(bb.x_min, bb.y_min, bb.x_max, bb.y_max)

    def bisector_coords(self, x_min, y_min, x_max, y_max):
        x_mid = (self.start.x + self.end.x) / 2
        y_mid = (self.start.y + self.end.y) / 2
        
        if abs(self.start.x - self.end.x) < self.EPSILON:
            return Line(Point(x_min, y_mid), Point(x_max, y_mid))
        elif abs(self.start.y - self.end.y) < self.EPSILON:
            return Line(Point(x_mid, y_min), Point(x_mid, y_max))
        
        m = -(self.end.x - self.start.x) / (self.end.y - self.start.y)
        c = y_mid - (m * x_mid)
        
        x1 = (y_min - c) / m
        y1 = y_min
        if x1 < x_min:
            x1 = x_min
            y1 = m * x_min + c
        elif x1 > x_max:
            x1 = x_max
            y1 = m * x_max + c

        x2 = (y_max - c) / m
        y2 = y_max
        if x2 < x_min:
            x2 = x_min
            y2 = m * x_min + c
        elif x2 > x_max:
            x2 = x_max
            y2 = m * x_max + c

        return Line(Point(x1, y1), Point(x2, y2))

    def intersection(self, l):
        det = (self.start.x - self.end.x) * (l.start.y - l.end.y) - (self.start.y - self.end.y) * (l.start.x - l.end.x)
        if abs(det) <= self.EPSILON:
            return None
        
        a = (self.start.x * self.end.y - self.start.y * self.end.x)
        b = (l.start.x * l.end.y - l.start.y * l.end.x)
        x = (a * (l.start.x - l.end.x) - (self.start.x - self.end.x) * b) / det
        y = (a * (l.start.y - l.end.y) - (self.start.y - self.end.y) * b) / det
        
        if ((x + self.EPSILON < min(self.start.x, self.end.x))
            or (x - self.EPSILON > max(self.start.x, self.end.x))
            or (x + self.EPSILON < min(l.start.x, l.end.x))
            or (x - self.EPSILON > max(l.start.x, l.end.x))):
            return None
        elif ((y + self.EPSILON < min(self.start.y, self.end.y))
              or (y - self.EPSILON > max(self.start.y, self.end.y))
              or (y + self.EPSILON < min(l.start.y, l.end.y))
              or (y - self.EPSILON > max(l.start.y, l.end.y))):
            return None
        else:
            return Point(x, y)