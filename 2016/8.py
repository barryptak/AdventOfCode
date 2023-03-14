"""
https://adventofcode.com/2016/day/8
"""
from itertools import product
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def rotate_right(screen_row, steps):
    """ Rotate the screen row right by steps """
    steps %= len(screen_row)
    return screen_row[-steps:] + screen_row[:-steps]


def rotate_down(screen, col, steps):
    """ Rotate the screen column down by steps """
    columns = list(zip(*screen))
    rotated_column = rotate_right(columns[col], steps)
    columns[col] = rotated_column
    return [list(column) for column in zip(*columns)]


def render_screen(instructions):
    """ Execute the instruction list and return the rendered screen output """
    screen = [[" "]*50]*6
    for line in instructions:
        # Pull the A & B values for the line and then figure out what the
        # instruction is to execute
        a, b = extract_ints(line)
        if line.startswith("rect"):
            for y, x in product(range(b), range(a)):
                screen[y][x] = "#"
        elif line.startswith("rotate row"):
            screen[a] = rotate_right(screen[a], b)
        else: # rotate column
            screen = rotate_down(screen, a, b)

    return screen


display_screen = render_screen(data)

# Part 1
# How many pixels are lit in the end?
print(sum(row.count("#") for row in display_screen))

# Part 2
# What letters are displayed on the screen in the end?
for row in display_screen:
    print("".join(row))
