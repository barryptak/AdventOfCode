"""
https://adventofcode.com/2017/day/11
"""
from utils.data import read_data
from utils.point2d import Point2D
from copy import copy

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

moves = data.split(",")

# 2D representation of hexagonal grid:
# N  | NE |
# NW | o  | SE
#    | SW | S
OFFSETS = {"n": Point2D(-1, 1), "ne": Point2D(0, 1),
           "nw": Point2D(-1, 0), "se": Point2D(1, 0),
           "sw": Point2D(0, -1), "s": Point2D(1, -1)}

def follow_path(start, path):
    """
    Follow the hex path and return the final position and the maximum
    distance ever reached from the start position.
    """
    max_dist = 0
    pos = copy(start)
    for move in path:
        pos += OFFSETS[move]
        diff = pos - start
        max_dist = max(max(abs(diff.x), abs(diff.y)), max_dist)
    return pos, max_dist


start_pos = Point2D(0, 0)
final_pos, max_dist = follow_path(start_pos, moves)

# Part 1 - distance from start to final position
diff = final_pos - start_pos
dist = max(abs(diff.x), abs(diff.y)) # We can move diagonally so can't just use manhattan distance
print(dist)

# Part 2 - max distance ever reached
print(max_dist)

