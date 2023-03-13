"""
https://adventofcode.com/2016/day/24
"""
import functools
import math
from itertools import permutations
from utils import astar_path_length, manhattan_distance, Point2D, read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def find_all_points_of_interest(grid):
    """
    Extract all of the points of interest (including the start) from the input
    data.
    Returns start_position, [points_of_interest]
    """
    start = None
    points = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.isdigit():
                pos = Point2D(x, y)
                if cell == "0":
                    start = pos
                else:
                    points.append(pos)

    return start, points


def get_neighbours(pos):
    """
    Used in A* path finding. Returns a list of valid positions that can be
    moved to from the supplied position.
    """
    neighbours = []
    offsets = [Point2D(0, -1), Point2D(0, 1), Point2D(-1, 0), Point2D(1, 0)]
    for offset in offsets:
        neighbour_pos = pos + offset
        # Check that the new position is within the grid/map
        if 0 <= neighbour_pos.y < len(data) and 0 <= neighbour_pos.x < len(data[0]):
            # Check that the new position is not a wall
            if data[neighbour_pos.y][neighbour_pos.x] != "#":
                neighbours.append(neighbour_pos)

    return neighbours


@functools.cache
def get_dist(point1, point2):
    """
    Memoised function that returns the length of the shortest path between the
    two given points.
    """
    return astar_path_length([point1], point2, manhattan_distance, get_neighbours)


def get_shortest_path_length(start, points, return_to_start=False):
    """
    Calculates the shortest path that begins at start and visits all points of
    interest at least once. Can optionally be required to return back to the
    start position again.
    """
    shortest_path = math.inf

    # Generate all possible paths through the points of interest (not including
    # start).
    possible_paths = permutations(points)

    # Iterate over all paths and calculate the total length beginning at start
    # (and optionally returning back to start at the end).
    for path in possible_paths:
        # Add start to the front of the path
        path = [start] + list(path)
        # Add start to the end of the path if required
        if return_to_start:
            path += [start]

        # Iterate over each pair of points and get the distance between them
        dist = 0
        for points in zip(path, path[1:]):
            # We sort the two points as order doesn't change the distance but
            # it does mean that we don't need to perform as many A* searches
            # by making sure that B -> A is requested the same as A -> B.
            points = sorted(points, key=lambda k: [k.y, k.x])
            dist += get_dist(points[0], points[1])

        shortest_path = min(shortest_path, dist)

    return shortest_path


# Get the start and points of interest from the input data
start_position, points_of_interest = find_all_points_of_interest(data)

# Part 1
# What's the length of the shortest path through all points of interest?
print(get_shortest_path_length(start_position, points_of_interest))

# Path 2
# what's the length of the shortest path if we have to return to start?
print(get_shortest_path_length(start_position, points_of_interest, True))
