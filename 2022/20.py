"""
https://adventofcode.com/2022/day/20
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def create_mixed(orig, indices, decryption_key):
    """ Create the final mixed sequence from the processed indices """
    mixed_sequence = [None]*len(indices)
    for i, index in enumerate(indices):
        mixed_sequence[index] = orig[i] * decryption_key
    return mixed_sequence

def wrap_index(i, sequence_length):
    """
    Wrap the supplied array index correctly if it extends past either end of
    the list.
    Note that we mod by len - 1 as when you wrap around you actually step one
    index further than might seem intuitive in order to move between the
    existing entries.
    """
    return i % (sequence_length - 1)

def mix_sequence(orig, num_iterations=1, decryption_key=1):
    """
    Performs the mixing operation on the list of numbers.
    Returns the final mixed sequence.
    """
    # Create a list for keeping track of mixed indices
    indices = [*range(len(orig))]

    for _ in range(num_iterations):
        # For each mixing iteration step through the original list of numbers
        for i, vals in enumerate(zip(orig, indices)):
            num, current_index = vals

            # Determine the new index for the current number
            num *= decryption_key
            new_index = wrap_index(current_index + num, len(orig))

            # Adjust the indices of the other numbers in the sequence
            # Are we moving the number earlier in the sequence?
            if new_index < current_index:
                # We need to change all the indices in
                # range(new_index, current_index) by moving them up by one
                affected_indices = range(new_index, current_index)
                for j, index in enumerate(indices):
                    if index in affected_indices:
                        indices[j] += 1
            # Are we moving the number later in the sequence?
            elif current_index < new_index:
                # We need to change all the indices in
                # range(current_index + 1, new_index + 1) by moving them down
                # by one
                affected_indices = range(current_index + 1, new_index + 1)
                for j, index in enumerate(indices):
                    if index in affected_indices:
                        indices[j] -= 1

            # Move the current number to its new index
            indices[i] = new_index

    return create_mixed(orig, indices, decryption_key)


def calculate_coords(mixed_sequence):
    """
    Calculates the grove coordinates based on the supplied mixed sequence
    """
    # Find the index of number 0
    zero_index = mixed_sequence.index(0)

    # Add the values at (wrapped) indices 1000,2000 & 3000 *after* the index of
    # the entry with value 0
    return sum((mixed_sequence[i % len(mixed_sequence)]
                for i in range(zero_index + 1000, zero_index + 4000, 1000)))


original_sequence = [int(x) for x in data]

# Part 1
mixed = mix_sequence(original_sequence)
print(calculate_coords(mixed))

# Part 2
NUM_ITERATIONS = 10
DECRYPTION_KEY = 811589153
mixed = mix_sequence(original_sequence, NUM_ITERATIONS, DECRYPTION_KEY)
print(calculate_coords(mixed))
