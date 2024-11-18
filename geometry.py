import math

class Geometry:
    EPSILON = 1e-7

    @staticmethod
    def closer_to(to, v1, v2):
        d1 = Geometry.dist_squared(to, v1)
        d2 = Geometry.dist_squared(to, v2)
        return v1 if d1 < d2 else v2

    @staticmethod
    def cross_product(v1, v2, v3):
        return (v2.x - v1.x) * (v3.y - v1.y) - (v2.y - v1.y) * (v3.x - v1.x)

    @staticmethod
    def distance(v1, v2):
        return math.sqrt(Geometry.dist_squared(v1, v2))

    @staticmethod
    def dist_squared(v1, v2):
        return (v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2