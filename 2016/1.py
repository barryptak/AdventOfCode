"""
https://adventofcode.com/2016/day/1
"""
from utils import read_data, Point2D, manhattan_distance

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

#region CONSTANTS

FACE_RIGHT = Point2D(1, 0)
FACE_LEFT = Point2D(-1, 0)
FACE_UP = Point2D(0, -1)
FACE_DOWN = Point2D(0, 1)

TURN = {
        FACE_RIGHT: {
            "L": FACE_UP,
            "R": FACE_DOWN
        },
        FACE_LEFT: {
            "L": FACE_DOWN,
            "R": FACE_UP
        },
        FACE_UP: {
            "L": FACE_LEFT,
            "R": FACE_RIGHT
        },
        FACE_DOWN: {
            "L": FACE_RIGHT,
            "R": FACE_LEFT
        }
}

#endregion

def get_new_facing(current_facing, turn_direction):
    """
    What's the new facing direction after applying the turn direction to the
    current facing?
    """
    return TURN[current_facing][turn_direction]


def follow_directions(input_data):
    """
    Follow the input directions and return the final position, and the first
    position visited twice
    """
    position = Point2D(0, 0)
    facing = FACE_UP
    visited = {position}
    visited_twice = None

    # Step through all of the input directions
    directions = input_data.split(", ")
    for direction in directions:
        # Face the correct way
        facing = get_new_facing(facing, direction[0])

        # If we haven't found
        # We iterate over the number of steps to take in a given direction rather
        # than do them all in one go so that we can tell if we've visited any
        # location more than once
        num_steps = int(direction[1:])
        if visited_twice is None:
            for _ in range(num_steps):
                position = position + facing
                if visited_twice is None:
                    if position in visited:
                        visited_twice = position
                    else:
                        visited.add(position)
        else:
            position = position + (facing * num_steps)

    return position, visited_twice


pos1, pos2 = follow_directions(data)

# Part 1
# Find the Manhattan distance from the starting position to the end position
# after following all instructions
print(manhattan_distance(Point2D(), pos1))

# Part 2
# Find hte Manhattan distance from the starting position to the first location
# that we visit twice
print(manhattan_distance(Point2D(), pos2))
