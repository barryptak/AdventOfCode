"""
https://adventofcode.com/2015/day/24
"""
import math
from itertools import combinations
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)
weights = [int(line) for line in data]


def subtract_lists(list1, list2):
    """
    Helper function to perform a set-style subtraction on two lists.
    This returns a list with each element in list1 removed for each time that
    it occurs in list2.
    e.g. [1,2,3,4,4,4], [1,2,4] -> [3,4,4]
    """
    list2_copy = list(list2)
    result = []
    for item in list1:
        if item in list2_copy:
            list2_copy.remove(item)
        else:
            result.append(item)
    return result


def find_equal_groups(packages, num_groups):
    """
    Returns the list of groups of the shortest length that result in a valid
    balancing of package weights in num_groups groups
    NOTE: We call this method recursively to make sure that we can correctly
    split the packages by weight into all sub-groups. This is a general
    solution. In the case of this puzzle we could skip the recursive part
    entirely as all the solutions for the smallest group are valid without
    needing the deeper check. This would be considerably faster, but I've left
    the correct general solution here anyway in order to be proper.
    """

    total_weight = sum(packages)
    group_weight = total_weight // num_groups

    # Start trying out groups of length 1 and then test groups of increasing
    # length until we've reached the maximum length that our smallest group can
    # be. In this case there's no point searching groups greater than the
    # number of packages / number of groups as any group larger than that would
    # have a smaller group paired with it anyway.
    max_group_length = math.ceil(len(packages) / num_groups)
    for group_length in range(1, max_group_length + 1):
        smallest_groups = set()
        for group in combinations(packages, group_length):
            if sum(group) == group_weight:
                # If we are trying to split into more than two groups then
                # call find_equal_groups on the remaining packages to see if
                # they divide up equally too. We need to do this as it's
                # possible to have group one being the correct weight but it
                # not be possible to create the remaining groups at the same
                # weight.
                if num_groups > 2:
                    remaining_packages = subtract_lists(packages, group)
                    sub_groups = find_equal_groups(remaining_packages, num_groups - 1)
                    # If we were able to correctly split up the remaining
                    # packages then we have a good overall combination.
                    # Add the first group to the list of candidate smallest
                    # groups.
                    if len(sub_groups) > 0:
                        smallest_groups.add(group)
                # If we are trying to split in just 2 then being able to find a
                # valid first group guarantees that the remaining packages also
                # form a valid group. No need to check further.
                elif num_groups == 2:
                    smallest_groups.add(group)

        # We found at least one group of length group_length that results in
        # num_groups groupings. Return this set of groups
        if len(smallest_groups) > 0:
            return smallest_groups

    return set()


# Part 1
# Find the minimum quantum entanglement for the smallest group that results in
# a balanced load

# The minimum quantum entanglement is the smallest product of groups returned
# from find_equal_groups
min_qe = min([math.prod(g) for g in find_equal_groups(weights, 3)])
print(min_qe)


# Part 2
# Same as above but we need 4 groups now instead
min_qe = min([math.prod(g) for g in find_equal_groups(weights, 4)])
print(min_qe)
