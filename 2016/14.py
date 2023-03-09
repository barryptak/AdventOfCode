"""
https://adventofcode.com/2016/day/4
"""
import functools
import hashlib
import re

@functools.cache
def get_hash(candidate, part2=False):
    """ Get the hash for the candidate index """
    string_to_hash = "ngcjuoqr" + str(candidate)
    for _ in range(2017 if part2 else 1):
        string_to_hash = hashlib.md5(string_to_hash.encode()).hexdigest()

    return string_to_hash

@functools.cache
def contains(candidate, sub_string, part2=False):
    """ Does the hash for the candidate index contain the substring? """
    return get_hash(candidate, part2).find(sub_string) != -1


def get_index_of_64th_key(part2):
    """ Get the index that generates the 64th valid pad key """
    candidate_num = 0
    count = 0

    while count < 64:
        hashed_string = get_hash(candidate_num, part2)
        match = re.search(r"(.)\1{2}", hashed_string)
        if match:
            num = hashed_string[match.start()]
            num_str = num*5

            for i in range(candidate_num + 1, candidate_num + 1001):
                if contains(i, num_str, part2):
                    count += 1
                    break

        candidate_num += 1

    return candidate_num - 1


# Part 1
# Get the 64th index that generates a key using standard hashing
print(get_index_of_64th_key(False))

# Part 1
# Get the 64th index that generates a key using stretched hashing
print(get_index_of_64th_key(True))
