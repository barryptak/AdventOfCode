"""
https://adventofcode.com/2022/day/8
"""
from utils import read_data, Point2D

USE_TEST_DATA = False
SPLIT_BY_LINE = True
trees = read_data(USE_TEST_DATA, SPLIT_BY_LINE, "8.txt")

grid_height = len(trees)
grid_width = len(trees[0])

DIRS = [Point2D(-1, 0), Point2D(1, 0), Point2D(0, -1), Point2D(0, 1)]

def is_visible(pos):
    """ Is the specified tree visible from outside the grid? """

    tree_height = trees[pos.y][pos.x]

    # Walk in each cardinal direction checking if we find a tree the same height
    # or taller than the current one.
    # If we do then this tree is not visible from the outside in that
    # direction.
    for delta in DIRS:
        pos2 = pos + delta
        visible_for_this_direction = True

        # Keep stepping in the same direction until we reach the edge of the
        # tree grid
        while pos2.y in range(grid_height) and pos2.x in range(grid_width):
            # If the tree we're testing is the same height or taller than our
            # tree then our tree is not visible in this direction.
            if trees[pos2.y][pos2.x] >= tree_height:
                visible_for_this_direction = False
                break

            # Step to the next tree to test
            pos2.add(delta)

        # As soon as we're visible from one direction then we're visible overall
        if visible_for_this_direction:
            return True

    return False

def calculate_scenic_score(pos):
    """ Calculates the scenic score for the supplied position """

    # If the location is on the edge of the grid then there must be at least
    # one direction in which we can see zero trees.
    # This means that the scenic score for this location will be zero so we can
    # ignore it.
    if pos.y == 0 or pos.y == (grid_height - 1):
        return 0
    if pos.x == 0 or pos.x == (grid_width - 1):
        return 0

    tree_height = trees[pos.y][pos.x]
    score = 1

    # Walk in each cardinal direction checking if we find a tree the same height
    # or taller than the current one.
    # If we do then we've gone as far as we can see.
    for delta in DIRS:
        pos2 = pos + delta
        count = 0

        # Keep stepping in the same direction until we reach the edge of the
        # tree grid
        while pos2.y in range(grid_height) and pos2.x in range(grid_width):
            count += 1
            # If the tree we're testing is the same height or taller than our
            # tree then that's the last one we'll be able to see.
            if trees[pos2.y][pos2.x] >= tree_height:
                break

            # Step to the next tree to test
            pos2.add(delta)

        # multiply the running scenic score by the score for the current
        # cardinal direction
        score *= count

    return score


visible_count = 0
highest_score = 0

# Iterate over every tree and check if it's visible from the outside and the
# scenic score for it
for row in range(grid_height):
    for col in range(grid_width):
        point = Point2D(col, row)
        if is_visible(point):
            visible_count += 1
        highest_score = max(highest_score, calculate_scenic_score(point))

print(visible_count)
print(highest_score)
