class Point:
    EPSILON = 1e-7

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return (abs(self.x - other.x) < self.EPSILON) and (abs(self.y - other.y) < self.EPSILON)
        return False