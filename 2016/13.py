"""
https://adventofcode.com/2016/day/13
"""
import functools
from utils import astar_path_length, manhattan_distance, Point2D


@functools.cache
def is_open(pos):
    """ Is the specified position open (True) or a wall (False)? """
    value = pos.x*(pos.x + 3 + 2*pos.y) + pos.y*(1 + pos.y) + 1362
    bits = value.bit_count()
    return bits % 2 == 0


def get_neighbour_coords(pos):
    """
    Get a list of all valid neighbour positions for the given position for
    part 1.
    Valid means in bounds AND not a wall.
    """
    neighbours = []

    # Iterate through the four positions adjacent to pos
    neighbour_offsets = [Point2D(-1, 0), Point2D(1, 0), Point2D(0, -1), Point2D(0, 1)]
    for neighbour in map(lambda offset: pos + offset, neighbour_offsets):
        # Is the position within the grid/map bounds?
        if neighbour.x >= 0 and neighbour.y >= 0:
            # Is the position open or a wall?
            if is_open(neighbour):
                neighbours.append(neighbour)

    return neighbours


# Part 1
# How many steps does it take to get from 1,1 to 31,39?
start = Point2D(1, 1)
goal = Point2D(31, 39)
print(astar_path_length([start], goal, manhattan_distance, get_neighbour_coords))


# Part 2
# How many unique positions can we reach in 50 steps or fewer?
visited = set()
queue = {Point2D(1, 1)}

for _ in range(51):
    new_positions = set()
    for position in queue:
        if position not in visited:
            visited.add(position)
            new_positions.update(get_neighbour_coords(position))

    queue = new_positions

print(len(visited))
