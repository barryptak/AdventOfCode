"""
2D point class helper for Advent of Code problems.
"""

class Point2D:
    """ 2D integer Point class """

    def __init__(self, x=0, y=0):
        ERROR_STRING = "Point2D constructor requires two ints or a list/tuple of two ints"
        if isinstance(x, int) and isinstance(y, int):
            self.x = x
            self.y = y
        elif (isinstance(x, tuple) or isinstance(x, list)) and y == 0:
            if len(x) == 2 and isinstance(x[0], int) and isinstance(x[1], int):
                self.x = x[0]
                self.y = x[1]
            else:
                raise ValueError(ERROR_STRING)
        else:
            raise ValueError(ERROR_STRING)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, scalar):
        return Point2D(self.x * scalar, self.y * scalar)

    def __hash__(self):
        return hash((self.x, self.y))


def manhattan_distance(pos1, pos2):
    """ Calculates the Manhattan distance between two points """
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

UDLR_OFFSETS = (Point2D(0, -1), Point2D(0, 1), Point2D(-1, 0), Point2D(1, 0))
