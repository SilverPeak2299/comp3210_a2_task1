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
        """
        Returns the euclidian distance from this point to the given point
        
        Args:
            point (Point): The point to calculate the distance to
        
        Returns:
            float: The euclidian distance between the two points
        """
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
    
    def dist_from_coords(self, x, y):
        """
        Returns the euclidian distance from this point to the given coordinates
        
        Args:
            x (float): The x-coordinate of the point to calculate the distance to
            y (float): The y-coordinate of the point to calculate the distance to
        
        Returns:
            float: The euclidian distance between the two points
        """
        return math.hypot(self.x - x, self.y - y)
