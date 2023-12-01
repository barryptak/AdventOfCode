"""
https://adventofcode.com/2017/day/6
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)
banks = [int(x) for x in data.split("\t")]

def run_cycle(memory_banks):
    """ Runs a single cycle of redistributing memory blocks """
    index, value = max(enumerate(memory_banks), key=lambda x: x[1])

    # Zero the bank we've read from
    memory_banks[index] = 0

    # Distribute the values across the other banks starting at the next one
    for _ in range(value):
        index = (index + 1) % len(memory_banks)
        memory_banks[index] += 1


def find_infinite_loop(memory_banks):
    """ Performs memory redistribution cycles until we find a loop """
    cycle_count = 0
    seen = {}
    while True:
        run_cycle(memory_banks)
        cycle_count += 1

        # Check to see if we've seen this distribution of memory before.
        # If we have then we've found a loop.
        banks_id = f"{memory_banks}"
        if banks_id in seen:
            return cycle_count, cycle_count - seen[banks_id]

        # Store this distribution and its cycle count so that we can use it
        # later to check for loops
        seen[banks_id] = cycle_count


# Parts 1 & 2
# Find the number of cycles until we find a loop, and the number of cycles in
# the loop.
for cycles in find_infinite_loop(banks):
    print(cycles)
