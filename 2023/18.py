"""
https://adventofcode.com/2023/day/18
"""
import collections
import math
from utils.data import read_data
from utils.point2d import Point2D


USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

dig_instructions = []
for line in data:
    dir, count, colour = line.split(" ")
    count = int(count)
    colour = colour[2:-1]
    dig_instructions.append((dir, count, colour))

OFFSETS = {"U": Point2D(0, -1), "D": Point2D(0, 1), "L": Point2D(-1, 0), "R": Point2D(1, 0),
           "3": Point2D(0, -1), "1": Point2D(0, 1), "2": Point2D(-1, 0), "0": Point2D(1, 0)}


# We can use Gauss' area formula to find the area of the dug out trench
def calculate_polygon_area(vertices):
    n = len(vertices)
    # Initialize sums for left and right sides of the formula
    left_sum = sum(vertices[i].x * vertices[(i + 1) % n].y for i in range(n))
    right_sum = sum(vertices[i].y * vertices[(i + 1) % n].x for i in range(n))
    area = abs(left_sum - right_sum) / 2
    return area





vertices = [Point2D(0, 0)]
for instruction in dig_instructions:
    vertices.append(vertices[-1] + OFFSETS[instruction[0]] * instruction[1])


area = calculate_polygon_area(vertices)
# We need to account for the fact that the trench has a width of 1.
# Only half of the trench is included in the calculated area.
# We still need to add 1/2 for each outer edge of the trench.
# Then an extra 1/4 for each corner of the trench.
extra_area = sum(dist for _, dist, _ in dig_instructions) // 2
print(int(area) + extra_area + 1)





new_instructions = []
for line in data:
    _, hex = line.split("#")
    hex = hex[:-1]
    distance = int(hex[:-1], 16)
    dir = hex[-1]
    new_instructions.append((dir, distance, ""))

vertices = [Point2D(0, 0)]
for instruction in new_instructions:
    vertices.append(vertices[-1] + OFFSETS[instruction[0]] * instruction[1])

area = calculate_polygon_area(vertices)
# We need to account for the fact that the trench has a width of 1.
# Only half of the trench is included in the calculated area.
# We still need to add 1/2 for each outer edge of the trench.
# Then an extra 1/4 for each corner of the trench.
extra_area = sum(dist for _, dist, _ in new_instructions) // 2
print(int(area) + extra_area + 1)




