"""
https://adventofcode.com/2022/day/12
"""
from utils.data import read_data
from utils.path_finding import astar_path_length
from utils.point2d import Point2D, manhattan_distance

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


# Part 1
# Find the shortest path from START to END
startList, end = find_endpoints(heightmap, START)
print(astar_path_length(startList, end, manhattan_distance, get_neighbour_coords_1))

# Part 2
# Find the shortest path from any position of MIN_HEIGHT to END
startList, _ = find_endpoints(heightmap, MIN_HEIGHT)
print(astar_path_length(startList, end, manhattan_distance, get_neighbour_coords_2))
