import math

class Point:
    id: int
    x: float
    y: float

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def dist(self, point):
        """Returns the euclidian distance from this point to the given point"""
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)