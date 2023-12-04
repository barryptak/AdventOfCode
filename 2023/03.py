"""
https://adventofcode.com/2023/day/3
"""

from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def is_symbol(char):
    """
    Is this character a symbol?
    A symbol is any character other than a digit or a full stop.
    """
    return char != '.' and not char.isdigit()

total = 0
adjacent_count = {}
adjacent_prod = {}

# Iterate over every character in the input data by row (y) and column (x)
for y, line in enumerate(data):
    x = 0
    while x < len(line):
        char = line[x]
        if char.isdigit():
            # Determine the span of the current number
            span = 1
            for x2 in range(x+1, len(line)):
                if not line[x2].isdigit():
                    break
                span += 1

            # Walk the area around this number to look for any symbols
            found_symbol = False
            for y2 in range(max(0, y-1), min(len(data), y+2)):
                for x2 in range(max(0, x-1), min(len(line), x+span+1)):
                    if is_symbol(data[y2][x2]):
                        # If we found a symbol then add the value of this number
                        # to the total for part 1, and update the count of
                        # adjacent numbers for part 2.
                        found_symbol = True
                        value = int(line[x:x+span])
                        total += value

                        # For part 2 we are looking for gears.
                        # A gear is any * symbol that is adjacent to exactly
                        # two part numbers.
                        # Store the count of adjacent numbers for each gear,
                        # and the product of the adjacent part numbers.
                        if data[y2][x2] == '*':
                            pos = (y2, x2)
                            adjacent_count[pos] = adjacent_count.get(pos, 0) + 1
                            adjacent_prod[pos] = adjacent_prod.get(pos, 1) * value
                            break

                if found_symbol:
                    break

            # Skip over the rest of this number as we've already processed it
            x += span
            continue

        # Not a number so move on to the next character
        x += 1


# Part 1 - Print the total of all the valid part numbers
print(total)


# Part 2 - Print the sum of the products of the part numbers adjacent to each gear.
total2 = sum(adjacent_prod[pos] for pos, count in adjacent_count.items() if count == 2)
print(total2)