"""
https://adventofcode.com/2023/day/17
"""
import collections
import math
from utils.data import read_data
from utils.point2d import Point2D, manhattan_distance


USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

grid = [[int(cell) for cell in list(line)] for line in data]

print(len(grid[0]), len(grid))

UP = Point2D(0, -1)
DOWN = Point2D(0, 1)
LEFT = Point2D(-1, 0)
RIGHT = Point2D(1, 0)

VALID_DIRECTIONS = {UP: [UP, LEFT, RIGHT], DOWN: [DOWN, LEFT, RIGHT], LEFT: [UP, DOWN, LEFT], RIGHT: [UP, DOWN, RIGHT]}

def in_bounds(pos):
    return pos.x >= 0 and pos.x < len(grid[0]) and pos.y >= 0 and pos.y < len(grid)

def get_neighbours_1(node):
    dirs = [d for d in VALID_DIRECTIONS[node.dir] if d != node.dir or node.count < 3]
    return [PathNode(node.pos + d, d, node.count + 1 if d == node.dir else 0, node.cost + grid[(node.pos + d).y][(node.pos + d).x]) for d in dirs if in_bounds(node.pos + d)]

def get_baseline_cost():
    cost = 0
    pos = Point2D(0, 0)
    goal = Point2D(len(grid[0]) - 1, len(grid) - 1)
    while pos != goal:
        cost += grid[pos.y][pos.x + 1]
        cost += grid[pos.y + 1][pos.x]
        pos += Point2D(1, 1)

    return cost

print(get_baseline_cost())

class PathNode:
    def __init__(self, pos, direction, count, cost):
        self.pos = pos
        self.dir = direction
        self.count = count
        self.cost = cost

    def __eq__(self, other):
        # ignore cost for this so that w can use it for the distances index
        return self.pos == other.pos and self.dir == other.dir# and self.count == other.count

    def __hash__(self):
        return hash((self.pos, self.dir))#, self.count))

def walk_grid(get_neighbours):

    start_node = PathNode(Point2D(0, 0), RIGHT, 0, grid[0][0])
    goal_position = Point2D(len(grid[0]) - 1, len(grid) - 1)
    best_cost = get_baseline_cost()

    incomplete_paths = [start_node]
    complete_paths = []

    visited = {}

    while len(incomplete_paths) > 0:
        incomplete_paths.sort(key=lambda x: x.cost + manhattan_distance(x.pos, goal_position)*5)
        current_path = incomplete_paths.pop(0)
        if current_path.cost > best_cost:
            continue

        if current_path in visited:
            if visited[current_path].cost <= current_path.cost:
                continue

        visited[current_path] = current_path

        for neighbour in get_neighbours(current_path):
            if neighbour.pos == goal_position:
                best_cost = min(best_cost, neighbour.cost)
                complete_paths.append(neighbour)
            else:
                incomplete_paths.append(neighbour)

    return best_cost


print(walk_grid(get_neighbours_1))