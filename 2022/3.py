"""
https://adventofcode.com/2022/day/3
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

LOWER_A_ORD = ord("a")
LOWER_Z_ORD = ord("z")
UPPER_A_ORD = ord("A")


def get_priority(item):
    """ Gets the priority score for the supplied rucksack item """
    item_ord = ord(item)
    if LOWER_A_ORD <= item_ord <= LOWER_Z_ORD:
        return item_ord - LOWER_A_ORD + 1
    else:
        return item_ord - UPPER_A_ORD + 27


# Part 1
# Find the item that is common between the two halves of each rucksack
priority_sum = 0
for items in data:
    # Figure out how many items are in each compartment and pull out one of the
    # compartments
    num_items_per_compartment = len(items) // 2
    compartment1 = items[:num_items_per_compartment]

    # Iterate over all items in compartment 2 and find the one that is also in
    # compartment 1
    for i in range(num_items_per_compartment, len(items)):
        item = items[i]
        if item in compartment1:
            priority_sum += get_priority(item)
            break

print(priority_sum)

# Part 2
# Find the item that is common between three consecutive rucksacks
i = 0
priority_sum = 0
while i < len(data):
    rucksack1 = data[i]
    rucksack2 = data[i + 1]
    rucksack3 = data[i + 2]

    for item in rucksack1:
        if item in rucksack2 and item in rucksack3:
            priority_sum += get_priority(item)
            break

    i += 3

print(priority_sum)
