"""
https://adventofcode.com/2023/day/6
"""

from math import sqrt, ceil, floor, prod
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def calc_ways_to_win(time, record):
    """
    Calculates the total number of ways in which this race can be won.

    Maths:
    dist = (time - press_time) * press_time
    dist = (time * press_time) - press_time^2
    press_time^2 - (total_time * press_time) + dist = 0
    press_time_1 = (total_time + sqrt(total_time^2 - (4 * dist))) / 2
    press_time_2 = (total_time - sqrt(total_time^2 - (4 * dist))) / 2
    """
    root_b_sqr_minus_4ac = sqrt(time*time - 4*(record + 1))
    # Use floor and ceil as partial presses are not valid
    press_time_1 = floor((time + root_b_sqr_minus_4ac) / 2)
    press_time_2 = ceil((time - root_b_sqr_minus_4ac) / 2)
    # Add one as press times are inclusive
    return abs(press_time_1 - press_time_2) + 1

# Part 1
# Determine the product of the counts of the ways that each race can be won.
race_times = extract_ints(data[0])
race_records = extract_ints(data[1])
ways_to_win = [calc_ways_to_win(*race_pair) for race_pair in zip(race_times, race_records)]
print(prod(ways_to_win))

# Part 2
# Determine the number of ways that the race can be won when we interpret the
# input as a single time and distance record.
race_time = extract_ints(data[0].replace(" ", ""))[0]
race_record = extract_ints(data[1].replace(" ", ""))[0]
print(calc_ways_to_win(race_time, race_record))
