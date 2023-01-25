"""
https://adventofcode.com/2015/day/8
"""
import re
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Part 1
# How many 'code'-only characters are there in the input strings?
# We could do this in a single list comprehension, but it looks a bit gnarly.
# Doing it like this makes the commenting easier too.
total_diff = 0
for line in data:
    # Find all (non-overlapping) matches in the input string for either:
    # \\, \" or \x00
    matches = re.findall(r"(\\\\)|(\\\")|(\\x(?:[a-z]|[0-9]){2})", line)
    # Diff between in-memory string and code string is:
    # 2 (for the start and end quotes)
    total_diff += 2
    # + 1 for each \\ or \" match (2 code chars down to 1 mem char)
    total_diff += len(matches)
    # + 3 for each \x00 match (4 code chars down to 1 mem char)
    # Note that we count 1 for each \x00 match in len(matches) already so we
    # only need to add another 2 for each \x00 match to our calculation.
    total_diff += 2 * len([match for match in matches if match[2] != ""])

print(total_diff)


# Part 2
# Fully encode the input strings and count how many extra characters we add to
# the code representation.

# For each character we need to escape we add 1 to our extra character count.
# For each line we must also add a further 2 to the extra character count to
# account for the two new enclosing double quotes we need to add.
total_added = sum([2 + len([char for char in line if char in ["\"", "\\"]]) for line in data])
print(total_added)
