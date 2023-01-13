"""
https://adventofcode.com/2022/day/13
"""
import functools
import math
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def compare_ints(left, right):
    """
    Compares two ints and returns -1, 0, 1 depending on whether left < right.
    Used for sorting.
    """
    if left < right:
        return -1
    elif left > right:
        return 1
    return 0

def compare(left, right):
    """
    Compares a pair of items which can either be ints, or lists of ints, or
    lists of lists of ints, etc..
    Ints are compared on value.
    Lists are compared on the first non-matching item or length if all values
    are equal.
    """

    # If left and right are different types then make them both lists
    # XOR are the item types different?
    if isinstance(left, int) ^ isinstance(right, int):
        # If one is a list and the other is an int then convert the int to a
        # list with a single int in it
        if isinstance(left, int):
            left = [left]
        else:
            right = [right]

    # Are we comparing ints?
    if isinstance(left, int):
        return compare_ints(left, right)
    # Are we comparing lists of ints?
    else:
        left_len = len(left)
        right_len = len(right)

        # Iterate over the lists looking for the first non-matching item to
        # give us our result
        for i in range(min(left_len, right_len)):
            res = compare(left[i], right[i])
            if res != 0:
                return res

        # List contents match up to the last item in the shortest list.
        # Now compare the lengths of the lists.
        return compare_ints(left_len, right_len)

# Part 1
# Add up the indices of the pairs that are already in the correct order
pairs = data.split("\n\n")
correct_order_count = 0
packets = []
for index, pair in enumerate(pairs, 1):
    first, second = pair.split("\n")

    # The input is already in a valid python form so we can just eval it
    first = eval(first)
    second = eval(second)

    # Add the packets to the packets list for part 2 to save us parsing them
    # again later
    packets.append(first)
    packets.append(second)

    # Are the elements in the right order?
    # If so then accumulate the current pair index
    if compare(first, second) == -1:
        correct_order_count += index

print(correct_order_count)


# Part 2
# Put all packets into the correct order (plus the extra divider packets) then
# find the final positions of the divider packers and use their indices to
# calculate the decoder key

# Add the two divider packets and sort all packets
DIVIDER_PACKETS = [[[2]], [[6]]]
packets.extend(DIVIDER_PACKETS)
sort_key = functools.cmp_to_key(compare)
packets = sorted(packets, key = sort_key)

# Find the two divider packets and determine the product of their indices
decoder_key = math.prod([index for index, packet in enumerate(packets, 1) 
                         if packet in DIVIDER_PACKETS])
print(decoder_key)
