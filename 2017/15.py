"""
https://adventofcode.com/2017/day/15
"""

USE_TEST_DATA = False

GENERATOR_A_START = 277
GENERATOR_B_START = 349
if USE_TEST_DATA:
    GENERATOR_A_START = 65
    GENERATOR_B_START = 8921

GENERATOR_A_FACTOR = 16807
GENERATOR_B_FACTOR = 48271
MASK = 0xffff

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
    a = GENERATOR_A_START
    b = GENERATOR_B_START
    count = 0
    for _ in range(iterations):
        a = get_next_value(a, GENERATOR_A_FACTOR, multiples[0])
        b = get_next_value(b, GENERATOR_B_FACTOR, multiples[1])

        # Compare the lowest 16 bits only
        if a & MASK == b & MASK:
            count += 1

    return count


# Part 1
# How many times do the lowest 16 bits of the generators match?
print(count_sequence_matches(40_000_000, (1, 1)))

# Part 1
# How many times do the lowest 16 bits of the generators match when the
# generators are more picky?
print(count_sequence_matches(5_000_000, (4, 8)))
