"""
https://adventofcode.com/2017/day/10
"""
from utils.data import extract_ints, read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

numbers = [i for i in range(256)]
position = 0
skip_size = 0
lengths = extract_ints(data)

for length in lengths:

    if position + length > len(numbers):
        remainder = position + length - len(numbers)
        sequence = numbers[position:] + numbers[:remainder]
        sequence.reverse()
        numbers[position:] = sequence[:len(numbers) - remainder]
        numbers[:remainder] = sequence[-remainder:]
    else:
        numbers[position:position + length] = reversed(numbers[position:position + length])

    position = (position + length + skip_size) % len(numbers)
    skip_size += 1

print(numbers[0] * numbers[1])

# Need to run test cases