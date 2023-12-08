"""
https://adventofcode.com/2023/day/8
"""

from math import lcm

from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

instructions = data[0]
node_network = {line[:3]: {"L": line[7:10], "R": line[12:15]} for line in data[2:]}

def num_steps_to_end(locations, is_end_node):
    """ Returns the number of steps required to get to all end nodes """
    ip = 0
    step_count = 0
    end_matches = {}
    while True:
        step_count += 1
        for i, location in enumerate(locations):
            locations[i] = node_network[location][instructions[ip]]

            # We can't realistically brute force the solution when navigating
            # multiple nodes in parallel, so instead we look for repetitions in
            # the node paths and then find the least common multiple of the
            # path periods to find the time at which all paths will complete
            # their cycle at the same time.
            if is_end_node(locations[i]) and i not in end_matches:
                end_matches[i] = step_count

        # When we have entries in end_matches for all paths then we can
        # stop iterating and do the maths to determine the least common
        # multiple to get the final answer.
        if len(end_matches) == len(locations):
            return lcm(*end_matches.values())

        ip += 1
        if ip >= len(instructions):
            ip = 0


# Part 1
# How many steps to get from AAA to ZZZ?
print(num_steps_to_end(["AAA"], lambda node: node == "ZZZ"))

# Part 2
# How many steps for all **A paths to be on **Z at the same time?
print(num_steps_to_end([node for node in node_network.keys() if node[2] == "A"],
                       lambda node: node[2] == "Z"))
