"""
https://adventofcode.com/2017/day/10
"""
from utils.data import extract_ints, read_data
from functools import reduce

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def perform_hash_pass(lengths, numbers, position, skip_size):
    """
    Performs a single pass of the hash algorithm.
    Returns the updated numbers, position and skip_size.
    """
    for length in lengths:
        # If we need to wrap around the end of the list we need special
        # handling to construct the sequence then split it back up in two parts.
        if position + length > len(numbers):
            remainder = position + length - len(numbers)
            sequence = numbers[position:] + numbers[:remainder]
            sequence.reverse()
            numbers[position:] = sequence[:length - remainder]
            numbers[:remainder] = sequence[-remainder:]
        # No wrapping so this is straight forward.
        else:
            numbers[position:position + length] = reversed(numbers[position:position + length])

        # Update position and skip_size accounting for wrapping.
        position = (position + length + skip_size) % len(numbers)
        skip_size += 1
    return numbers, position, skip_size


# Part 1
# Perform a single pass of the hash algorithm then print the product of the
# first two numbers in the output.
lengths = extract_ints(data)
numbers, _, _ = perform_hash_pass(lengths, [i for i in range(256)], 0, 0)
print(numbers[0] * numbers[1])

# Part 2
# Interpret the input as a list of ASCII codes then append the standard suffix.
# Perform 64 passes of the hash algorithm then reduce the resulting list of
# numbers into a dense hash before printing it out as a hex string.

lengths2 = [ord(char) for char in data] + [17, 31, 73, 47, 23]
numbers = [i for i in range(256)]
position = 0
skip_size = 0

# Perform all 64 passes
for i in range(64):
    numbers, position, skip_size = perform_hash_pass(lengths2, numbers, position, skip_size)

# Generate the dense hash
dense_hash = []
for i in range(16):
    dense_hash.append(reduce(lambda a, b: a ^ b, numbers[i*16:i*16+16]))

# Print the dense hash as a hex string
hash_string = "".join("{:02x}".format(i) for i in dense_hash)
print(hash_string)
