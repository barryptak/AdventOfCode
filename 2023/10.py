"""
https://adventofcode.com/2023/day/10
"""

from utils.data import read_data
from utils.point2d import Point2D


USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

grid = [list(line) for line in data]

start = None

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "S":
            start = Point2D(x, y)
            break
    if start:
        break

NEIGHBOURS = {
    "|": [Point2D(0, -1), Point2D(0, 1)],
    "-": [Point2D(-1, 0), Point2D(1, 0)],
    "L": [Point2D(0, -1), Point2D(1, 0)],
    "J": [Point2D(0, -1), Point2D(-1, 0)],
    "7": [Point2D(0, 1), Point2D(-1, 0)],
    "F": [Point2D(0, 1), Point2D(1, 0)],
}

def get_neighbours(grid, pos):
    value = grid[pos.y][pos.x]

    if value == "S":
        neighbours = []
        value_above = grid[pos.y - 1][pos.x] if pos.y > 0 else None
        if value_above in ["|", "F", "7"]:
            neighbours.append(pos + Point2D(0, -1))

        value_below = grid[pos.y + 1][pos.x] if pos.y < len(grid) - 1 else None
        if value_below in ["|", "L", "J"]:
            neighbours.append(pos + Point2D(0, 1))

        value_left = grid[pos.y][pos.x - 1] if pos.x > 0 else None
        if value_left in ["-", "L", "F"]:
            neighbours.append(pos + Point2D(-1, 0))

        value_right = grid[pos.y][pos.x + 1] if pos.x < len(grid[0]) - 1 else None
        if value_right in ["-", "J", "7"]:
            neighbours.append(pos + Point2D(1, 0))

        assert(len(neighbours) == 2)
        return neighbours
    else:
        return [pos + neighbour for neighbour in NEIGHBOURS[value]]


def walk_grid(grid, start, distances):
    dist = 1
    queue = [start]
    next_queue = []

    while True:
        while len(queue) > 0:
            pos = queue.pop(0)
            a, b = get_neighbours(grid, pos)

            if a not in distances or dist < distances[a]:
                distances[a] = dist
                next_queue.append(a)

            if b not in distances or dist < distances[b]:
                distances[b] = dist
                next_queue.append(b)


        if len(next_queue) == 0:
            break

        dist += 1
        queue = next_queue
        next_queue = []


distances = {start: 0}
walk_grid(grid, start, distances)
max_val = max(distances.values())
print(max_val)
