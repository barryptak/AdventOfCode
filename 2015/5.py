"""
https://adventofcode.com/2015/day/5
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def vowel_count(input_string):
    """ Return the number of vowels in the input string """
    return len([char for char in input_string if char in "aeiou"])


def contains_repeated_letter(input_string):
    """ Does the input string have any letter repeated twice in a row? """
    for i, char in enumerate(input_string[1:]):
        if char == input_string[i]:
            return True
    return False


def contains_phrase(input_string, phrases):
    """
    Does the input string contain any of the substrings/phrases provided?
    """
    for phrase in phrases:
        if phrase in input_string:
            return True
    return False


def contains_repeated_pair(input_string):
    """
    Does the input string contain a pair of characters repeated more than once
    anywhere in the string?
    """
    for i in range(0, len(input_string) - 3):
        first_pair = input_string[i:i+2]
        for j in range(i+2, len(input_string) - 1):
            if first_pair == input_string[j:j+2]:
                return True
    return False


def contains_repeated_letter_2(input_string):
    """
    Does the input string contain the same character repeated with any other
    character between?
    """
    for i in range(0, len(input_string) - 2):
        if input_string[i] == input_string[i+2]:
            return True
    return False


# Parts 1 & 2 together
# What are the count of naughty letters when applying each set of rules?

BAD_PHRASES = ["ab", "cd", "pq", "xy"]
nice_count_1 = 0
nice_count_2 = 0

for line in data:
    if (vowel_count(line) >= 3 and
        contains_repeated_letter(line) and
        not contains_phrase(line, BAD_PHRASES)):
        nice_count_1 += 1

    if (contains_repeated_letter_2(line) and
        contains_repeated_pair(line)):
        nice_count_2 += 1

print(nice_count_1)
print(nice_count_2)
