"""
https://adventofcode.com/2022/day/4
"""
from utils import *

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def range_is_contained(range, superset_range):
    """ Returns whether the first range is entirely contained within superset_range """
    return range[0] >= superset_range[0] and range[1] <= superset_range[1]

def ranges_contained(range1, range2):
    """ Returns whether the either supplied range is entirely contained within the other """
    return range_is_contained(range1, range2) or range_is_contained(range2, range1)

def ranges_overlap(range1, range2):
    """ Returns whether the supplied ranges overlap at all """
    return range1[0] <= range2[1] and range1[1] >= range2[0]

contained_count = 0
overlapped_count = 0
for line in data:
    # Convert the string input ("A-B,C-D") into a list of int pairs (in a list) ([[A,B], [C,D]])
    ranges = [list(map(int, range.split("-"))) for range in line.split(",")]

    if ranges_overlap(ranges[0], ranges[1]):
        overlapped_count += 1
        # If the ranges don't overlap then they can't contain each other either so we can do this test inside the overlap True case 
        if ranges_contained(ranges[0], ranges[1]):
            contained_count += 1

print(contained_count)
print(overlapped_count)