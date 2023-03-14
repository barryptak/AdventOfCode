"""
https://adventofcode.com/2022/day/24
"""

import copy
from utils.data import read_data, add_tuples
from utils.point2d import Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

START_POS = Point2D(1,0)
END_POS = Point2D(len(data[0]) - 2, len(data) - 1)

empty_valley = [[["."]] * len(row) for row in data]
valley = [list(map(list, line)) for line in data]

WEATHER_MOVEMENT = {"<": (-1,  0),
                    ">": ( 1,  0),
                    "^": ( 0, -1),
                    "v": ( 0,  1)}

PLAYER_MOVES = [Point2D(0, -1), Point2D(0, 1), Point2D(-1, 0), Point2D(1, 0), Point2D(0, 0)]

def step_weather(valley_grid):
    """ Simulate the valley weather for a single step """

    new_grid = copy.deepcopy(empty_valley)

    for y, row in enumerate(valley_grid):
        for x, col in enumerate(row):
            # Our grid contains a list for each position since we can have more
            # than one blizzard in the same position at a time.
            # Iterate over all of these and move them independently.
            for entity in col:
                # Nothing to do if it's a valley wall (#) or empty (.) position
                if entity == "#" or entity == ".":
                    continue
                else:
                    # Move this blizzard based on its direction
                    move = WEATHER_MOVEMENT[entity]
                    new_x, new_y = add_tuples((x, y), move)

                    # Wrap around the valley walls
                    if new_x <= 0:
                        new_x = len(row) - 2
                    elif new_x >= len(row) - 1:
                        new_x = 1
                    if new_y <= 0:
                        new_y = len(valley_grid) - 2
                    elif new_y >= len(valley_grid) - 1:
                        new_y = 1

                # If there is no blizzard at this location then replace the
                # empty marker with this blizzard.
                # If there's already a list of blizzards at this location then
                # append this one to the list
                if new_grid[new_y][new_x][0] == ".":
                    new_grid[new_y][new_x] = [entity]
                else:
                    new_grid[new_y][new_x].append(entity)

    return new_grid


def is_valid_position(pos, valley_grid):
    """
    Is this position a valid position to be in?
    Must be in bounds and not contain a blizzard too.
    """

    # Start and end positions are always valid
    if pos == START_POS or pos == END_POS:
        return True

    # Is this position within the x range of the grid?
    if pos.x < 1 or pos.x > len(valley_grid[0]) - 2:
        return False

    # Is this position within the y range of the grid?
    if pos.y < 1 or pos.y > len(valley_grid) - 2:
        return False

    # Is this space currently blizzard free?
    return valley_grid[pos.y][pos.x][0] == "."


def find_path(valley_grid, start_pos, end_pos):
    """
    Finds a path through the valley from start_pos to end_pos.
    Returns the number of steps taken to reach the goal, and the final valley
    layout (since the blizzards have moved around)
    """

    # Because the grid is not static, it makes something like A* not a
    # reasonable approach as the cost heuristic doesn't really make sense.
    # Instead we will just simulate all possible valid moves at any given time
    # all at once and cull those that hit blizzards counting the steps as we go.
    # We'll eventually reach the goal (or have no valid moves to make (but we
    # assume that the puzzle doesn't leave us in this position)).

    step_count = 0
    positions = set()
    positions.add(start_pos)

    # Keep looping until we reach the goal position and return
    while True:
        step_count += 1

        # Simulate the weather for the end of this turn
        new_grid = step_weather(valley_grid)

        # For all positions in our list test if it's possible to move left,
        # right, up, down or stay in the same place.
        # Add all valid new positions to the list.
        new_positions = set()
        for current_pos in positions:
            # Test all of our possible moves from here and keep the valid ones
            # (valid means in bounds and not ending inside a blizzard)
            possible_moves = [current_pos + move for move in PLAYER_MOVES]
            possible_moves = [pos for pos in possible_moves if is_valid_position(pos, new_grid)]

            # Have we reached the goal position?
            if end_pos in possible_moves:
                return step_count, new_grid

            # Add the valid moves from current_pos to the new positions list
            new_positions = new_positions.union(possible_moves)

        # Swap our temp data
        valley_grid = new_grid
        positions = new_positions


# Part 1
# How many steps to get from start to end?
leg1, valley = find_path(valley, START_POS, END_POS)
print(leg1)


# Part 2
# How many steps to get from start to end, back to start (for sandwiches),
# then back to end again?
leg2, valley = find_path(valley, END_POS, START_POS)
leg3, valley = find_path(valley, START_POS, END_POS)
print(leg1 + leg2 + leg3)
