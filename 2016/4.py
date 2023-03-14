"""
https://adventofcode.com/2016/day/4
"""
import re
from collections import Counter
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def sum_sector_ids(room_data):
    """ Returns the sum of the sector ids of all real rooms """

    sector_id_sum = 0
    for room in room_data:
        # Extract the name (minus the dashes) and the checksum from the input data
        parts = re.split(r"-|\[|\]", room)
        room_name = "".join(parts[:-3])
        checksum = parts[-2]

        # Count the number of instances of each character and sort by character
        # count and then alphabetical order
        char_counts = Counter(room_name)
        results = sorted(char_counts.items(), key=lambda x: (-x[1], x[0]))

        # Calculate the checksum for this name & sector id and test against the
        # checksum from the input. If they match then the room is real.
        calculated_checksum = "".join([r[0] for r in results[:5]])
        if calculated_checksum == checksum:
            sector_id_sum += int(parts[-3])

    return sector_id_sum


def rotate_letter(letter, amount):
    """
    Rotate the given letter by amount steps (wrapping around to a when stepping
    past z)
    """
    # Dashes convert to spaces
    if letter == "-":
        return " "

    # Increment to the new letter and wrap around to stay within a-z
    new_letter = ord(letter) + (amount % 26)
    while new_letter > ord("z"):
        new_letter -= 26

    return chr(new_letter)


def decipher_name(encrypted_name, sector_id):
    """
    Deciphers the encrypted name and sector id into the decrypted room name
    """
    return "".join([rotate_letter(l, sector_id) for l in encrypted_name])


def get_north_pole_object_room_id(room_data):
    """ Gets the sector id of the room used for storing north pole objects """

    for room in room_data:
        parts = re.split(r"-|\[|\]", room)
        room_name = "-".join(parts[:-3])
        sector_id = int(parts[-3])

        # Decipher the room name and check for our keywords
        deciphered_name = decipher_name(room_name, sector_id)
        if all(s in deciphered_name for s in ["north", "pole", "object"]):
            return sector_id


# Part 1
# What's the sum of the sector ids of all of the real rooms?
print(sum_sector_ids(data))

# Part 2
# What's the sector id for room where the north pole objects are stored?
print(get_north_pole_object_room_id(data))
