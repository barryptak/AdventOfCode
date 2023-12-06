"""
https://adventofcode.com/2017/day/14
"""

from knot_hash import get_knot_hash

USE_TEST_DATA = False
KEY = "stpzcrnm" if not USE_TEST_DATA else "flqrgnkx"


def visit_region(row, col, visited):
    """
    Recursively visit all grid locations adjacent to this one.
    If the location is used and not part of a previously visited region then
    return 1.
    """
    if (row, col) in visited:
        return 0

    visited.add((row, col))

    if grid[row][col] == "1":
        for (dy, dx) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (0 <= row + dy < 128) and (0 <= col + dx < 128):
                visit_region(row + dy, col + dx, visited)
        return 1
    else:
        return 0


grid = ["".join([format(value, '08b')
        for value in get_knot_hash(KEY + "-" + str(row))])
        for row in range(128)]

# Part 1
# Count the number of used squares in the entire grid
print(sum([row.count("1") for row in grid]))

# Part 2
# Count the number of distinct regions in the grid
visited_regions = set()
print(sum([visit_region(row, col, visited_regions) for row in range(128) for col in range(128)]))
