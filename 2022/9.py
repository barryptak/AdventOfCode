"""
https://adventofcode.com/2022/day/9
"""
from utils import read_data, Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

MOVE = {"U": Point2D(0, 1), "D": Point2D(0, -1), "L": Point2D(-1, 0), "R": Point2D(1, 0)}

def follow(knot, other):
    """ Return the new position of knot after following other """

    # Get the diff between the two knots
    delta = other - knot

    # Are the knots touching? If so, do nothing.
    if abs(delta.x) <= 1 and abs(delta.y) <= 1:
        return knot

    move = (0, 0)

    # Knots are in the same row - move horizontally only
    if delta.y == 0:
        dist = abs(delta.x)
        if dist == 2:
            move = MOVE["R"] if delta.x > 0 else MOVE["L"]
    # Knots are in the same solumn - move vertically only
    elif delta.x == 0:
        dist = abs(delta.y)
        if dist == 2:
            move = MOVE["U"] if delta.y > 0 else MOVE["D"]
    # Knots are in different columns and rows - move diagonally
    else:
        move = MOVE["R"] if delta.x > 0 else MOVE["L"]
        move2 = MOVE["U"] if delta.y > 0 else MOVE["D"]
        move = move + move2

    # Apply the correct movement to the knot and return the result
    return knot + move


# Initialise the rope so that all knots are at the start position
NUM_SEGMENTS = 10
START_POS = Point2D(0, 0)
rope = [START_POS for _ in range(NUM_SEGMENTS)]

# Use sets for the tail history to only record unique positions
tail_history1 = {Point2D(0, 0)}
tail_history2 = {Point2D(0, 0)}

# Iterate over all of the movement instructions in the input data
for line in data:
    direction, steps = line.split()

    # Apply the number of move steps for the current move direction
    for i in range(int(steps)):
        # Move the head
        rope[0] = rope[0] + MOVE[direction]

        # Update all of the remaining segments to follow their predecessor
        for i in range(1, NUM_SEGMENTS):
            rope[i] = follow(rope[i], rope[i-1])

        # Record the position of the 2nd knot (for part 1) and the last knot
        # (for part 2)
        tail_history1.add(rope[1])
        tail_history2.add(rope[-1])

print(len(tail_history1))
print(len(tail_history2))
