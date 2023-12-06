"""
https://adventofcode.com/2017/day/10
"""
from knot_hash import perform_hash_pass, get_knot_hash
from utils.data import extract_ints, read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# Part 1
# Perform a single pass of the hash algorithm then print the product of the
# first two numbers in the output.
input_lengths = extract_ints(data)
hashed_numbers, _, _ = perform_hash_pass(input_lengths, [i for i in range(256)], 0, 0)
print(hashed_numbers[0] * hashed_numbers[1])

# Part 2
# Interpret the input as a list of ASCII codes then append the standard suffix.
# Perform 64 passes of the hash algorithm then reduce the resulting list of
# numbers into a dense hash before printing it out as a hex string.
hash_string = "".join("{:02x}".format(i) for i in get_knot_hash(data))
print(hash_string)
