"""
https://adventofcode.com/2016/day/2
"""
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

#region CONSTANTS

BUTTONS = [["1", "2", "3"],
           ["4", "5", "6"],
           ["7", "8", "9"]]

BUTTONS2 = [[None, None, "1", None, None],
            [None, "2", "3", "4", None],
            ["5", "6", "7", "8", "9"],
            [None, "A", "B", "C", None],
            [None, None, "D", None, None]]

MOVE = {"L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1)}

#endregion

def calculate_code(input_data, buttons, start_row, start_col):
    """ Follow the input instructions to determine the keypad code """
    button_row = start_row
    button_col = start_col
    code = ""
    for line in input_data:
        # Iterate over each character in the input line
        for step in line:
            # Determine the new row and column to move to (and clamp it to the keypad dimensions)
            move = MOVE[step]
            new_row = min(max(0, button_row + move[1]), len(buttons) - 1)
            new_col = min(max(0, button_col + move[0]), len(buttons[button_row]) - 1)

            # If this is valid key then make the move
            if buttons[new_row][new_col] is not None:
                button_row = new_row
                button_col = new_col

        # We've reached the end of the current line of instructions so we need
        # to press this key to form the code
        code += buttons[button_row][button_col]

    return code


# Part 1
# What's the code for a standard keypad layout?
print(calculate_code(data, BUTTONS, 1, 1))

# Part 2
# What's the code for the actual keypad layout?
print(calculate_code(data, BUTTONS2, 2, 0))
