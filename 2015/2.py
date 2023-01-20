"""
https://adventofcode.com/2015/day/2
"""
import functools
import math
from utils import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# By sorting the dimensions as we read them in we can make the calculations
# later much simpler since we know that the shortest two sides will be first.
dims = [sorted(extract_ints(line)) for line in data]

def get_paper_needed(dim):
    """
    For a given set of (sorted) present dimensions determine the area of
    paper required to wrap it
    """
    return 3*dim[0]*dim[1] + 2*dim[1]*dim[2] + 2*dim[0]*dim[2]

def get_ribbon_needed(dim):
    """
    For a given set of (sorted) present dimensions determine the length of
    ribbon required to wrap it
    """
    return 2*(dim[0]+dim[1]) + math.prod(dim)

# Part 1
# Calculate the area of paper needed to wrap all of the presents
paper_needed = functools.reduce(lambda a, b: a + b, map(get_paper_needed, dims))
print(paper_needed)


# Part 2
# Calculate the length of ribbon needed to wrap all of the presents
ribbon_needed = functools.reduce(lambda a, b: a + b, map(get_ribbon_needed, dims))
print(ribbon_needed)

# NOTE: I did combine the paper and ribbon functions into one to reduce the
# number of iterations of map/reduce, but it was much uglier to read so I left
# it like this.
