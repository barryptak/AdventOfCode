"""
https://adventofcode.com/2022/day/14
"""
import copy
from utils.data import read_data
from utils.point2d import Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)



def parse_cave(rock_paths):
    """
    Parse the layout of rocks from the input data and construct the cave
    representation
    """
    cave = {}
    low_point = 0
    for rock_path in rock_paths:
        waypoints = [eval(w) for w in rock_path.split(" -> ")]
        for i in range(len(waypoints) - 1):
            pos1 = Point2D(waypoints[i])
            pos2 = Point2D(waypoints[i+1])
            delta = pos2 - pos1

            if delta.x == 0:
                delta.y //= abs(delta.y)
            else:
                delta.x //= abs(delta.x)

            pos = pos1
            cave[pos] = '#'
            while pos.x != pos2.x or pos.y != pos2.y:
                pos = pos + delta
                cave[pos] = '#'

            low_point = max([pos1.y, pos2.y, low_point])
    return cave, low_point


def blocked(cave, pos, hard_floor = None):
    """ Is the current position blocked or not? """
    if hard_floor is not None and pos.y == hard_floor:
        return True
    else:
        return pos in cave


def simulate_sand(initial_cave_configuration, hard_floor = None):
    """
    Simulate sand falling into the cave until it reaches the abyss then
    return the final cave configuration
    """

    SAND_START_POS = Point2D(500, 0)
    DOWN = Point2D(0, 1)
    DOWN_AND_LEFT = Point2D(-1, 1)
    DOWN_AND_RIGHT = Point2D(1, 1)

    cave = copy.deepcopy(initial_cave_configuration)

    # Keep simulating until we reach the end condition of flowing into the
    # abyss or blocking the source location
    finished = False
    while not finished:
        sand_pos = SAND_START_POS
        # Simulate one unit of sand
        while True:
            # Can we move straight down?
            candidate_pos = sand_pos + DOWN
            if not blocked(cave, candidate_pos, hard_floor):
                sand_pos = candidate_pos

                # Has this unit fallen into the abyss?
                if hard_floor is None and sand_pos.y > lowest_point:
                    finished = True
                    break
            else:
                # There's something in the cave directly below us

                # Can we go diagonally left?
                candidate_pos = sand_pos + DOWN_AND_LEFT
                if not blocked(cave, candidate_pos, hard_floor):
                    sand_pos = candidate_pos
                else:
                    # Can we go diagonally right?
                    candidate_pos = sand_pos + DOWN_AND_RIGHT
                    if not blocked(cave, candidate_pos, hard_floor):
                        sand_pos = candidate_pos
                    else:
                        # We can't flow anywhere - settle here
                        cave[sand_pos] = "o"

                        # Have we blocked the source point?
                        if sand_pos == SAND_START_POS:
                            finished = True

                        break
    return cave

# Read in the cave configuration
cave_configuration, lowest_point = parse_cave(data)

# Part 1
# Simulate until a unit of sand falls into the abyss
cave1 = simulate_sand(cave_configuration)
settled_sand_count_1 = len([o for o in cave1.values() if o == "o"])
print(settled_sand_count_1)

# Part 2
# Simulate with a hard floor until the source location becomes blocked
cave2 = simulate_sand(cave_configuration, lowest_point + 2)
settled_sand_count_2 = len([o for o in cave2.values() if o == "o"])
print(settled_sand_count_2)
