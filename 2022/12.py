"""
https://adventofcode.com/2022/day/12
"""
import math
from utils import read_data, Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = True

data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)
heightmap = [[ord(x) for x in line] for line in data]
heightmap_height = len(heightmap)
heightmap_width = len(heightmap[0])

MIN_HEIGHT = ord("a")
MAX_HEIGHT = ord("z")
START = ord("S")
END = ord("E")


def find_endpoints(grid, start_value):
    """
    Find all of the valid starting positions in the grid plus the one valid
    end position
    """
    start_list = []
    end_pos = None

    # Iterate over all cells in the map/grid looking for start and end points
    for row_id, row in enumerate(grid):
        for column_id, cell_height in enumerate(row):
            # Is this a valid starting point?
            if cell_height == start_value:
                grid[row_id][column_id] = MIN_HEIGHT
                start_list.append(Point2D(column_id, row_id))
            # Is this the end point?
            elif cell_height == END:
                grid[row_id][column_id] = MAX_HEIGHT
                end_pos = Point2D(column_id, row_id)

    return start_list, end_pos


def get_neighbour_coords_1(pos):
    """
    Get a list of all valid neighbour positions for the given position for
    part 1.
    Valid means in bounds AND no more than one higher than the current height.
    """
    neighbours = []
    max_height = heightmap[pos.y][pos.x] + 1

    # Iterate through the four positions adjacent to pos
    neighbour_offsets = [Point2D(-1, 0), Point2D(1, 0), Point2D(0, -1), Point2D(0, 1)]
    for neighbour in map(lambda offset: pos + offset, neighbour_offsets):
        # Is the position within the grid/map bounds?
        if 0 <= neighbour.y < heightmap_height and 0 <= neighbour.x < heightmap_width:
            #Is the height a valid one that we can move to?
            if heightmap[neighbour.y][neighbour.x] <= max_height:
                neighbours.append(neighbour)

    return neighbours

def get_neighbour_coords_2(pos):
    """
    Get a list of all valid neighbour positions for the given position for
    part 2.
    Valid means in bounds AND no more than one higher than the current height.
    """
    # Small optimisation to ignore MIN_HEIGHT cells as they are already all
    # added as starting points so moving to one cannot be a shorter path than
    # another path that we're already evaluating.
    return [n for n in get_neighbour_coords_1(pos) if heightmap[n.y][n.x] != MIN_HEIGHT]


def astar_path_length(start_list, goal, dist_heuristic, get_neighbours):
    """
    Returns the shortest path length from any start pos to the end pos.
    Implements A*
    """
    open_set = set(start_list)
    came_from = {}
    g = {s : 0 for s in start_list}
    f = {s : dist_heuristic(s, goal) for s in start_list}

    while len(open_set) > 0:
        # Pull the pos from the open set that we think is closest to the goal
        pos = sorted(open_set, key = lambda p: f[p])[0]

        # Have we reached the goal?
        if pos == goal:
            # Calculate the length of this path and return it
            path_length = 0
            # Walk backwards from pos pulling out the previous position that
            # got us here. Keep going until we've completed the path backwards
            # so that there's no predecessor left.
            while pos in came_from:
                pos = came_from[pos]
                path_length += 1
            return path_length

        open_set.remove(pos)

        # Examine all of the valid neighbours of pos
        for neighbour in get_neighbours(pos):
            # Is the path from pos to neighbour the cheapest one so far?
            tentative_g = g[pos] + 1
            neighbour_g = g[neighbour] if neighbour in g else math.inf
            if tentative_g < neighbour_g:
                # Pos -> neighbour is the cheapest path we've found to neigbour
                # so far.
                # Update come_from to indicate that the best path to neighbour
                # is from pos.
                # Update the heuristic scores for neighbour and add it to the
                # open set.
                came_from[neighbour] = pos
                g[neighbour] = tentative_g
                f[neighbour] = tentative_g + dist_heuristic(neighbour, goal)
                if neighbour not in open_set:
                    open_set.add(neighbour)

    # No path found :(
    return None


def manhattan_dist(pos1, pos2):
    """ Return the Manhattan distance between two points """
    diff = pos1 - pos2
    return abs(diff.x) + abs(diff.y)


# Part 1
# Find the shortest path from START to END
startList, end = find_endpoints(heightmap, START)
print(astar_path_length(startList, end, manhattan_dist, get_neighbour_coords_1))

# Part 2
# Find the shortest path from any position of MIN_HEIGHT to END
startList, _ = find_endpoints(heightmap, MIN_HEIGHT)
print(astar_path_length(startList, end, manhattan_dist, get_neighbour_coords_2))
