"""
https://adventofcode.com/2017/day/4
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
passphrases = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

valid_count_1 = 0
valid_count_2 = 0
for passphrase in passphrases:
    words = passphrase.split()
    num_words = len(words)

    # Valid passphrases do not include repeated words
    valid_count_1 += 1 if len(set(words)) == num_words else 0

    # Valid passphrases do not include anagrams of other words
    sorted_words = set("".join(sorted(word)) for word in words)
    valid_count_2 += 1 if len(sorted_words) == num_words else 0

print(valid_count_1)
print(valid_count_2)
