"""
https://adventofcode.com/2022/day/5
"""
import copy
from utils import *

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def parse_input(data):
    """
    Parses the input data to read out the starting configuration of crates and stacks
    The output is a list of stacks of crates, and a list of moves (as strings)
    e.g.
    [H]
    [J] [V]
     1   2 

    move 2 from 1 to 2
    move 1 from 2 to 1

    Parses into:
    [[J,H],[V]], ["move 2 from 1 to 2", "move 1 from 2 to 1"]
    """
    stacks = {}
    moves = []
    for i, line in enumerate(data):
        # Exit when we hit a blank line as that signifies the end of the starting configuration
        if line == "":
            # Grab the remaining unparsed data as the list of move instructions
            moves = data[i+1:]
            break

        stack_index = 1
        char_index = 1
        CHAR_STEP = 4

        # Read along the line skipping 4 characters at a time so that we just read the crate letters in each stack
        while char_index < len(line):
            # Read the current character. If it's an alphabetic character then add the crate to the appropriate stack
            char = line[char_index]
            if char.isalpha():
                # Check if the stack exists already and create one if it doesn't
                if stack_index not in stacks:
                    stacks[stack_index] = []
                # Add the crate to the current stack
                stacks[stack_index].append(char)
            
            # Move along to the next stack and see if there's a crate there
            stack_index += 1
            char_index += CHAR_STEP

    # Reverse each stack so that the bottom crate is the beginning of each stack
    for i in range(1, len(stacks) + 1):
        stacks[i].reverse()

    return stacks, moves


def get_top_crates(stack_list):
    """ Given a list of stacks creates a string representing the top crate from each stack and returns it """
    top_crates = ""
    for i in range(1, len(stack_list) + 1):
         top_crates += stack_list[i][-1]
    return top_crates
    

# Parse the initial stack configuration and list of moves
# Take a copy of the stack configuration so that we can run parts 1 & 2 at 
# the same time without interfering with each other
stacks, moves = parse_input(data)
stacks2 = copy.deepcopy(stacks)

for move in moves:
    # move is something like 'move 6 from 4 to 3'
    num_to_move, source_stack, dest_stack = extract_ints(move)
   
    # Part 1 - perform each move one at a time
    for i in range(num_to_move):
        crate = stacks[source_stack].pop()
        stacks[dest_stack].append(crate)

    # Part 2 - perform multiple moves in a single operation
    crates_to_move = stacks2[source_stack][-num_to_move:]
    stacks2[source_stack] = stacks2[source_stack][:-num_to_move]
    stacks2[dest_stack].extend(crates_to_move)

print(get_top_crates(stacks))
print(get_top_crates(stacks2))