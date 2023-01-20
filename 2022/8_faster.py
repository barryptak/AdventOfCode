"""
https://adventofcode.com/2022/day/8
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
trees = read_data(USE_TEST_DATA, SPLIT_BY_LINE, input_file_name="8.txt")
grid_height = len(trees)
grid_width = len(trees[0])

# Part 1 - Count num trees visible from the outside

def check_visibility(grid, visibility, y, x, max_height):
    """
    Mark this tree visibile if it's taller than the current max_height.
    Return the new max_height so that we can use it for the next tree along.
    """
    tree_height = grid[y][x]
    if tree_height > max_height:
        visibility[y][x] = True
        return tree_height
    return max_height


def walk_horizontally(grid, visibility, y):
    """
    Walk along row y determining if each tree is visible from the side
    """
    max_height1 = "-1"
    max_height2 = "-1"
    for x1, x2 in enumerate(reversed(range(len(grid[y])))):
        max_height1 = check_visibility(grid, visibility, y, x1, max_height1)
        max_height2 = check_visibility(grid, visibility, y, x2, max_height2)


def walk_vertically(grid, visibility, x):
    """
    Walk along column x determining if each tree is visible from the top or
    bottom
    """
    max_height1 = "-1"
    max_height2 = "-1"
    for y1, y2 in enumerate(reversed(range(len(grid)))):
        max_height1 = check_visibility(grid, visibility, y1, x, max_height1)
        max_height2 = check_visibility(grid, visibility, y2, x, max_height2)


# Initialise visibilty data
tree_visibility = []
for row in range(grid_height):
    tree_visibility.append([False] * grid_width)

# Iterate over each row and walk it horizontally calculating visibility for
# each tree in the row
for i in range(grid_height):
    walk_horizontally(trees, tree_visibility, i)

# Iterate over each column and walk it vertically calculating visibility for
# each tree in the column
for i in range(grid_width):
    walk_vertically(trees, tree_visibility, i)

# Get the number of visible trees on each horizontal row and sum them up for
# our total
visible_tree_counts = [len([tree for tree in row if tree]) for row in tree_visibility]
visible_count = sum(visible_tree_counts)

print(visible_count)


# Part 2 - Find the tree with the highest scenic score

def calculate_scenic_score(x, y):
    """
    Calculate the scenic score for the given tree by checking how many trees it
    can see in each direction and multiplying those together.
    """

    # If the location is on the edge of the grid then there must be at least
    # one direction in which we can see zero trees.
    # This means that the scenic score for this location will be zero so we can
    # ignore it.
    if y == 0 or y == (grid_height - 1):
        return 0
    if x == 0 or x == (grid_width - 1):
        return 0

    tree_height = trees[y][x]

    # Walk left until we can't see any more trees because there's a tall one in
    # the way OR we've reached the edge of the grid
    left_count = 0
    for x2 in reversed(range(x)):
        left_count += 1
        left_tree_height = trees[y][x2]
        if left_tree_height >= tree_height:
            break

    # Walk right
    right_count = 0
    for x2 in range(x + 1, grid_width):
        right_count += 1
        right_tree_height = trees[y][x2]
        if right_tree_height >= tree_height:
            break

    # Walk up
    up_count = 0
    for y2 in reversed(range(y)):
        up_count += 1
        up_tree_height = trees[y2][x]
        if up_tree_height >= tree_height:
            break

    # Walk down
    down_count = 0
    for y2 in range(y + 1, grid_height):
        down_count += 1
        down_tree_height = trees[y2][x]
        if down_tree_height >= tree_height:
            break

    # Return final scenic score by multiplying the number of trees visible in
    # each direction
    return left_count * right_count * up_count * down_count


# Iterate over all trees and find the highest scenic score
highest_score = 0
for row in range(grid_height):
    for column in range(grid_width):
        highest_score = max(highest_score, calculate_scenic_score(column, row))

print(highest_score)
