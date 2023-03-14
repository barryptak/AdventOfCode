"""
https://adventofcode.com/2016/day/20
"""
import functools
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def sort_ranges(range1, range2):
    """ Sorting helper that sorts ranges by the starting value of the range """
    if range1.start < range2.start:
        return -1
    elif range1.start == range2.start:
        return 0
    return 1


def collapse_ranges(ranges):
    """
    Takes a list of ranges and collapses them into as short a list as
    possible by throwing away ranges completely contained by others, and
    by joining together overlapping ranges into one.
    """

    # Sort the ranges by start value
    ranges.sort(key=functools.cmp_to_key(sort_ranges))

    # Collapse ranges together when they overlap

    collapsed_ranges = []
    starting_range = ranges[0]
    start_x = starting_range.start
    end_x = starting_range.stop
    for next_range in ranges[1:]:
        # is next_range entirely contained in the current one?
        if next_range.stop <= end_x:
            # Continue to the next range. We don't need to do anything
            # with this one as it's already covered by current.
            continue
        # does next_range overlap and extend the current range?
        elif next_range.start <= end_x:
            # Extend the end of the current window to match next_range
            end_x = next_range.stop
        # no overlap
        else:
            # There's no overlap at all so add the current window and start a new one
            collapsed_ranges.append(range(start_x, end_x))
            start_x = next_range.start
            end_x = next_range.stop

    # Don't forget to capture the currently open window when we reach the end of the ranges
    collapsed_ranges.append(range(start_x, end_x))
    return collapsed_ranges


# Read in the list of ranges from the input file
range_list = []
for line in data:
    ints = line.split("-")
    start = int(ints[0])
    end = int(ints[1])
    range_list.append(range(start, end + 1))

# Collapse the ranges to produce a minimal list
range_list = collapse_ranges(range_list)


# Part 1
# Find the lowest unblocked IP

# Check to see if the first range starts at 0 or not.
# If not then 0 is our first unblocked IP.
# Otherwise just find where the first range ends and that will be the first
# unblocked IP.
first_unblocked_ip = range_list[0].stop if range_list[0].start == 0 else 0
print(first_unblocked_ip)


# Part 2
# How many unblocked IPs are there in total?
total = sum(r2.start - r1.stop for r1, r2 in zip(range_list, range_list[1:]))
print(total)
