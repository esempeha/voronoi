class BoundingBox:
    EPSILON = 1e-7

    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def contains(self, p):
        return ((p.x > self.x_min - self.EPSILON) and (p.x < self.x_max + self.EPSILON)
                and (p.y > self.y_min - self.EPSILON) and (p.y < self.y_max + self.EPSILON))

    def __str__(self):
        return f"[({self.x_min}, {self.y_min})->({self.x_max}, {self.y_max})"