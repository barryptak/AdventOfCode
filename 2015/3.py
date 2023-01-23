"""
https://adventofcode.com/2015/day/3
"""

from utils import read_data, Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

MOVES = {"^": Point2D(0, 1),
         "v": Point2D(0, -1),
         "<": Point2D(-1, 0),
         ">": Point2D(1, 0)}

def visit_houses(directions):
    """
    Follow the provided directions and return a list of the unique house
    positions visited
    """
    pos = Point2D(0,0)
    positions = {pos}

    for direction in directions:
        pos = pos + MOVES[direction]
        positions.add(pos)

    return positions


# Part 1
# Santa working alone
visited_houses = visit_houses(data)
print(len(visited_houses))

# Part 2
# Santa working with Robo-Santa; following every second direction each
visited_houses = visit_houses(data[::2]) | visit_houses(data[1::2])
print(len(visited_houses))
