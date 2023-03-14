"""
https://adventofcode.com/2022/day/10
"""
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

KEY_CYCLE_START = 20
KEY_CYCLE_END = 220
KEY_CYCLE_STEP = 40


def get_signal_strength(cycle_num, reg_value):
    """ REturns the signal strength for the current cycle and reg value """
    if cycle_num <= KEY_CYCLE_END and cycle_num % KEY_CYCLE_STEP == KEY_CYCLE_START:
        return cycle_num * reg_value
    return 0


def sprite_present(cycle_num, reg_value):
    """ Is a sprite present at the current location? """
    column = (cycle_num - 1) % 40
    diff = abs(reg_value - column)
    return diff <= 1


def do_render(reg_value, current_scanline):
    """ Render the output for the current cycle """

    cycle_num = len(current_scanline) + 1

    # Add the correct character to the scanline
    sprite = "#" if sprite_present(cycle_num, reg_value) else "."
    current_scanline += sprite

    # If the scanline is full then print it to the screen and reset it
    if cycle_num == 40:
        print(current_scanline)
        current_scanline = ""

    return current_scanline


# Parts 1 and 2
# We can execute both at the same time while only iterating over the data once

reg = 1
cycle = 1
signal_strength = 0
scanline = ""

for line in data:
    # Get next instruction
    instruction = line.split()
    # nop instructions take one cycle to execute
    # addx instructions take two cycles to execute
    # This handily matches the number of parts in each instruction...
    execution_cycles = len(instruction)

    # Accumulate signal strength if this is one of the key cycles
    signal_strength += get_signal_strength(cycle, reg)

    # Update the render output
    scanline = do_render(reg, scanline)

    # If the current instruction takes two cycles to execute (i.e. it's an addx)
    # then render again for the extra cycle, and execute the addx instruction
    if execution_cycles == 2:
        signal_strength += get_signal_strength(cycle + 1, reg)
        scanline = do_render(reg, scanline)
        reg += int(instruction[1])

    # Step the cycle count
    cycle += execution_cycles

# Part 1 gets printed last as we print part 2 out as we execute
print(signal_strength)
