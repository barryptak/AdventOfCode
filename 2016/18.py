"""
https://adventofcode.com/2016/day/1
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def generate_row(previous_row):
    """ Generates the pattern for a row given the previous row """

    TRAP_PATTERNS = (('^', '^', '.'), ('.', '^', '^'), ('^', '.', '.'), ('.', '.', '^'))
    LEFT_TRAP_PATTERNS = ("^^", ".^")
    RIGHT_TRAP_PATTERNS = ("^^", "^.")

    # Determine the tiles for  the new row (except the first and last)
    new_tiles = [
        "^" if pair in TRAP_PATTERNS else "."
        for pair in zip(previous_row, previous_row[1:], previous_row[2:])
    ]

    # Determine the new first tile
    first_tile = "^" if previous_row[:2] in LEFT_TRAP_PATTERNS else "."

    # Determine the new last tile
    last_tile = "^" if previous_row[-2:] in RIGHT_TRAP_PATTERNS else "."

    # Combine all tiles to create the new row
    return first_tile + "".join(new_tiles) + last_tile


# Part 1
# How many safe tiles are there in the first 40 rows?
row = data
safe_count = row.count(".")
for i in range(39):
    row = generate_row(row)
    safe_count += row.count(".")

print(safe_count)


# Part 2
# How many safe tiles are there in the first 400000 rows?
for i in range(400000-40):
    row = generate_row(row)
    safe_count += row.count(".")

print(safe_count)
