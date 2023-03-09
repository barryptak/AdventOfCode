"""
https://adventofcode.com/2016/day/17
"""

import hashlib
from collections import deque
from utils import Point2D


def get_door_states(path):
    """ Get the door states for the given path """
    passcode = "qtetzkpl" + "".join(path)
    hash_value = hashlib.md5(passcode.encode()).hexdigest()
    return [l in "bcdef" for l in hash_value[:4]]


def find_path(start, goal, find_shortest):
    """
    Finds the path from start to goal navigating through the doors between each
    position.
    find_shortest indicates whether to return the shortest path (True) or the
    length of the longest path (False).
    """

    # Moves and symbols for U, D, L & R
    MOVES = [Point2D(0, -1), Point2D(0, 1), Point2D(-1, 0), Point2D(1, 0)]
    SYMBOLS = "UDLR"

    # Initialise a queue of positions and paths to process
    paths_queue = deque()
    paths_queue.append((start, []))
    longest_path_length = 0

    # Perform a breadth first search to find valid paths
    while len(paths_queue) > 0:
        # Pop the next position and path to process from the queue
        position, path = paths_queue.popleft()

        # Get whether each door is open or closed based on our previous path
        doors = get_door_states(path)
        for i, door_open in enumerate(doors):
            # We're only interested in open doors
            if door_open:
                # Does going through this door move us to the goal position?
                pos2 = position + MOVES[i]
                if pos2 == goal:
                    if find_shortest:
                        return "".join(path) + SYMBOLS[i]
                    else:
                        longest_path_length = max(longest_path_length, len(path) + 1)
                # We're not at the goal position.
                # Check that the new position is valid before adding it to the
                # queue.
                elif 0 <= pos2.x <= 3 and 0 <= pos2.y <= 3:
                    path2 = path + [SYMBOLS[i]]
                    paths_queue.append((pos2, path2))

    return longest_path_length if not find_shortest else ""


START_POSITION = Point2D(0, 0)
GOAL_POSITION = Point2D(3, 3)

# Part 1
# What's the shortest path through the rooms?
print(find_path(START_POSITION, GOAL_POSITION, True))

# Part 2
# What's the length of the longest path through the rooms?
print(find_path(START_POSITION, GOAL_POSITION, False))
