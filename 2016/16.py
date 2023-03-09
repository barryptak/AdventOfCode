"""
https://adventofcode.com/2016/day/16
"""
import copy

def generate_data(data, length):
    """
    Generate "dragon curve" patterned data of a specified length from the
    given starting pattern
    """
    data = copy.copy(data)
    while len(data) < length:
        b = ["1" if a == "0" else "0" for a in data[::-1]]
        data.append("0")
        data.extend(b)

    return data[:length]


def calculate_checksum(data):
    """ Calculate the checksum for the provided data """
    while True:
        data = ["1" if a == b else "0" for a, b in zip(data[::2], data[1::2])]
        if len(data) % 2 == 1:
            return data


INPUT_DATA = list("10011111011011001")

# Part 1
# What's the checksum when we generate data that is 272 elements in length?
part1_data = generate_data(INPUT_DATA, 272)
print("".join(calculate_checksum(part1_data)))

# Part 2
# What's the checksum when we need 35651584 elements?
part2_data = generate_data(INPUT_DATA, 35651584)
print("".join(calculate_checksum(part2_data)))
