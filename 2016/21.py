"""
https://adventofcode.com/2016/day/21
"""
from utils import read_data, rotate_string

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


def swap_position(string, index1, index2):
    """ Swap the characters at the specified indices """
    chars = list(string)
    chars[index1], chars[index2] = chars[index2], chars[index1]
    return "".join(chars)


def swap_letter(string, l1, l2):
    """ Swap the specified letters around """
    chars = [l2 if letter == l1 else l1 if letter == l2 else letter for letter in string]
    return "".join(chars)


def get_num_rotations(index, length):
    """
    Helper function for rotate_on_letter and reverse_rotate_on_letter to
    determine the number of times to rotate a string based on the index of a
    letter.
    """
    num_rotations = index + 1
    if index >= 4:
        num_rotations += 1
    return num_rotations % length


def rotate_on_letter(string, letter):
    """
    Rotate the string to the right on the location of letter.
    Num rotations = 1 + letter index. Plus another 1 if index >= 4.
    """
    return rotate_string(string, get_num_rotations(string.index(letter), len(string)))


def reverse_rotate_on_letter(string, letter):
    """
    Perform the reverse of rotate_on_letter.
    There will be a much nicer way of doing this, but I've just brute forced
    it to find the original index of the letter in question then from that
    determine the number of left rotations to perform to get back to the
    previous string.
    """
    current_index = string.index(letter)
    length = len(string)
    for i in range(length):
        new_index = (i + get_num_rotations(i, length)) % length
        if new_index == current_index:
            prev_index = i
            diff = prev_index - current_index
            return rotate_string(string, diff)


def reverse_substring(string, start, end):
    """
    Reverse the substring between indices start (inclusive) and end (exclusive)
    """
    return string[:start] + string[start:end][::-1] + string[end:]


def move_character(string, index1, index2):
    """ Move the character at index 1 to index 2 """

    # Remove the character store it in a variable
    char = string[index1]
    string = string[:index1] + string[index1+1:]

    # Insert the character and return the final string
    return string[:index2] + char + string[index2:]


def scramble_password(password, unscramble=False):
    """
    Scramble the provided password using the scrambling instructions from the
    input file.
    If unscramble is True then we unscramble (reverse the process) instead.
    """
    direction = -1 if unscramble else 1
    for line in data[::direction]:
        parts = line.split()

        if parts[0] == "swap":
            # swap position x with position y
            if parts[1] == "position":
                password = swap_position(password, int(parts[2]), int(parts[5]))
            # swap letter x with letter y
            else:
                password = swap_letter(password, parts[2], parts[5])
        elif parts[0] == "rotate":
            # rotate left x steps
            if parts[1] == "left":
                password = rotate_string(password, -int(parts[2])*direction)
            # rotate right x steps
            elif parts[1] == "right":
                password = rotate_string(password, int(parts[2])*direction)
            # rotate based on position of letter x
            else:
                if unscramble:
                    password = reverse_rotate_on_letter(password, parts[6])
                else:
                    password = rotate_on_letter(password, parts[6])
        # reverse positions x through y
        elif parts[0] == "reverse":
            password = reverse_substring(password, int(parts[2]), int(parts[4])+1)
        # move position x to position y
        else:
            if unscramble:
                password = move_character(password, int(parts[5]), int(parts[2]))
            else:
                password = move_character(password, int(parts[2]), int(parts[5]))

    return password


# Part 1
# Scramble our password
print(scramble_password("abcdefgh"))

# Part 2
# Unscramble an existing password
print(scramble_password("fbgdceah", True))
