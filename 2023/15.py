"""
https://adventofcode.com/2023/day/15
"""

from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def get_hash(string_in):
    hash_value = 0
    for char in string_in:
        val = ord(char)
        hash_value += val
        hash_value *= 17
        hash_value %= 256

    return hash_value

init_sequence = data.split(",")

total = 0
for step in init_sequence:
    total += get_hash(step)

print(total)




###########

class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __eq__(self, other):
        if isinstance(other, str):
            return self.label == other
        return self.label == other.label

    def __repr__(self):
        return f"{self.label} {self.focal_length}"


boxes = []
for i in range(256):
    boxes.append([])

for step in init_sequence:

    if step[-1] == "-":
        # remove lens
        label = step[:-1]
        box_id = get_hash(label)
        box = boxes[box_id]
        if label in box:
            box.remove(label)
    else:
        # add lens
        label, focal_length = step.split("=")
        focal_length = int(focal_length)

        if label == "ot" and focal_length == 7:
            pass


        box_id = get_hash(label)
        box = boxes[box_id]
        index = box.index(label) if label in box else None
        if index is not None:
            box[index] = Lens(label, focal_length)
        else:
            box.append(Lens(label, focal_length))


total = 0

for i, box in enumerate(boxes):
    for j, lens in enumerate(box):
        focusing_power = 1 + i
        focusing_power *= j + 1
        focusing_power *= lens.focal_length
        total += focusing_power

print(total)
