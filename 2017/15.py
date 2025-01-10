"""
https://adventofcode.com/2017/day/15
"""

from copy import copy
from itertools import islice

USE_TEST_DATA = True

GENERATOR_START = [65, 8921] if USE_TEST_DATA else [277, 349]
GENERATOR_FACTOR = [16807, 48271]
# GENERATOR_A_START = 65 if USE_TEST_DATA else 277
# GENERATOR_B_START = 8921 if USE_TEST_DATA else 349
# GENERATOR_A_FACTOR = 16807
# GENERATOR_B_FACTOR = 48271


def get_next_value(prev_value, factor, multiple):
    """ Returns the next value in the sequence """
    # Avoid the loop and extra mod when possible
    if multiple == 1:
        return (prev_value * factor) % 2147483647

    # Keep looping through the sequence until we find a value that is a multiple
    while True:
        new_value = (prev_value * factor) % 2147483647
        if new_value % multiple == 0:
            return new_value
        prev_value = new_value


def count_sequence_matches(iterations, multiples):
    """
    Returns the number of times the generators produce the same value
    (in the lowest 16 bits)
    """
    values = copy(GENERATOR_START)
    # a = GENERATOR_A_START
    # b = GENERATOR_B_START
    count = 0
    for _ in range(iterations):
        values = [get_next_value(value, factor, multiple) for value, factor, multiple in zip(values, GENERATOR_FACTOR, multiples)]
        # a = get_next_value(a, GENERATOR_A_FACTOR, multiples[0])
        # b = get_next_value(b, GENERATOR_B_FACTOR, multiples[1])

        # Compare the lowest 16 bits only
        if all(value & 0xffff == values[0] & 0xffff for value in values):
        #if a & 0xffff == b & 0xffff:
            count += 1

    return count


# Part 1
# How many times do the lowest 16 bits of the generators match?
print(count_sequence_matches(40_000_000, (1, 1)))

# Part 2
# How many times do the lowest 16 bits of the generators match when the
# generators are more picky?
print(count_sequence_matches(5_000_000, (4, 8)))

# def get_value(start_value, factor, multiple):
#     prev_value = start_value
#     while True:
#         new_value = (prev_value * factor) % 2147483647
#         if multiple == 1 or new_value % multiple == 0:
#             yield new_value & 0xffff
#         prev_value = new_value

# values = [islice(get_value(start, factor, 1), 40_000_000) for start, factor in zip(GENERATOR_START, GENERATOR_FACTOR)]

# count = 0
# for a, b in zip(values[0], values[1]):
#     if a == b:
#         count += 1

# print(count)

# count1 = sum(a == b for a, b in islice(zip(get_value(GENERATOR_A_START, GENERATOR_A_FACTOR, 1), get_value(GENERATOR_B_START, GENERATOR_B_FACTOR, 1)), 40_000_000))
# print(count1)


# count2 = sum(a == b for a, b in islice(zip(get_value(GENERATOR_A_START, GENERATOR_A_FACTOR, 4), get_value(GENERATOR_B_START, GENERATOR_B_FACTOR, 8)), 5_000_000))
# print(count2)
