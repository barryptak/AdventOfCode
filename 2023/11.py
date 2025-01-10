"""
https://adventofcode.com/2023/day/11
"""

from utils.data import read_data
from utils.point2d import Point2D, manhattan_distance


USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


galaxies = []
empty_rows = []
for y, row in enumerate(data):
    new_galaxies = [Point2D(x, y) for x, cell in enumerate(row) if cell == "#"]
    if len(new_galaxies) == 0:
        empty_rows.append(y)
    else:
        galaxies.extend(new_galaxies)

empty_cols = []
for x in range(len(data[0])):
    is_empty = True
    for row in data:
        if row[x] != ".":
            is_empty = False
            break

    if is_empty:
        empty_cols.append(x)


expansion_rate = 1000000
total = 0
for i, galaxy1 in enumerate(galaxies):
    for galaxy2 in galaxies[i + 1:]:
        x_range = range(min(galaxy1.x, galaxy2.x), max(galaxy1.x, galaxy2.x) + 1)
        y_range = range(min(galaxy1.y, galaxy2.y), max(galaxy1.y, galaxy2.y) + 1)
        dist = manhattan_distance(galaxy1, galaxy2)
        for empty_row in empty_rows:
            if empty_row in y_range:
                dist += (expansion_rate - 1)

        for empty_col in empty_cols:
            if empty_col in x_range:
                dist += (expansion_rate - 1)

        total += dist

print(total)