""" Knot hash shared code """

from functools import reduce

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

def get_knot_hash(key):
    """
    Returns the knot hash of the given key.
    """
    lengths = [ord(char) for char in key] + [17, 31, 73, 47, 23]
    numbers = [i for i in range(256)]
    position = 0
    skip_size = 0

    # Perform all 64 passes
    for i in range(64):
        numbers, position, skip_size = perform_hash_pass(lengths, numbers, position, skip_size)

    # Generate the dense hash
    dense_hash = []
    for i in range(16):
        dense_hash.append(reduce(lambda a, b: a ^ b, numbers[i*16:i*16+16]))

    return dense_hash
