"""
https://adventofcode.com/2023/day/16
"""
import sys
from utils.data import read_data
from utils.point2d import Point2D
USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

sys.setrecursionlimit(6000)

grid_data = [list(line) for line in data]
visited_cells = {}

UP = Point2D(0, -1)
DOWN = Point2D(0, 1)
LEFT = Point2D(-1, 0)
RIGHT = Point2D(1, 0)

NEW_DIRECTIONS = {UP: {"\\": [LEFT], "/": [RIGHT], "|": [UP], "-": [LEFT, RIGHT], ".": [UP]},
                  DOWN: {"\\": [RIGHT], "/": [LEFT], "|": [DOWN], "-": [LEFT, RIGHT], ".": [DOWN]},
                  LEFT: {"\\": [UP], "/": [DOWN], "|": [UP, DOWN], "-": [LEFT], ".": [LEFT]},
                  RIGHT: {"\\": [DOWN], "/": [UP], "|": [UP, DOWN], "-": [RIGHT], ".": [RIGHT]}}

def walk_beam(position, direction, grid, visited):
    if position not in visited:
        visited[position] = [direction]
    else:
        if direction in visited[position]:
            return
        visited[position].append(direction)

    new_directions = NEW_DIRECTIONS[direction][grid[position.y][position.x]]
    for new_direction in new_directions:
        new_position = position + new_direction
        if new_position.x >= 0 and new_position.x < len(grid[0]) and new_position.y >= 0 and new_position.y < len(grid):
            walk_beam(new_position, new_direction, grid, visited)

walk_beam(Point2D(0, 0), RIGHT, grid_data, visited_cells)
print(len(visited_cells))


entry_candidates = [(Point2D(0, y), RIGHT) for y in range(len(grid_data))]
entry_candidates.extend([(Point2D(len(grid_data[0]) - 1, y), LEFT) for y in range(len(grid_data))])
entry_candidates.extend([(Point2D(x, 0), DOWN) for x in range(len(grid_data[0]))])
entry_candidates.extend([(Point2D(x, len(grid_data) - 1), UP) for x in range(len(grid_data[0]))])

max_energy = 0
for candidate in entry_candidates:
    visited_cells.clear()
    walk_beam(candidate[0], candidate[1], grid_data, visited_cells)
    max_energy = max(max_energy, len(visited_cells))

print(max_energy)

# TODO: Works but could probably be faster / better using a queue rather than recursion