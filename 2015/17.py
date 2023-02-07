# """
# https://adventofcode.com/2015/day/17
# """
from itertools import combinations
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def get_combinations(sizes, target_volume):
    """ Get all combinations of sizes that add up to exactly target_volume """
    combos = []
    for i in range(1, len(sizes) + 1):
        combos.extend((combo for combo in combinations(sizes, i) if sum(combo) == target_volume))
    return combos


# Part 1
# How many combinations of our containers can fit exactly 150 litres?
container_sizes = [int(s) for s in data]
size_combinations = get_combinations(container_sizes, 150)
print(len(size_combinations))

# Part 2
# How many combinations of the minimum number of required containers are there?
min_containers = min(len(combo) for combo in size_combinations)
print(sum(1 for combo in size_combinations if len(combo) == min_containers))
