"""
https://adventofcode.com/2017/day/7
"""
from utils.data import extract_ints, read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def read_programs(data_in):
    """
    Parse the input data into a more useful structure.
    Returns a dictionary with the program name as key, with "weight" and
    "children" fields in the value's dict.
    """
    programs = {}
    for line in data_in:
        strs = line.split(" ")
        name = strs[0]
        weight = extract_ints(strs[1])[0]
        children = [s.rstrip(",") for s in strs[3:]] if len(strs) > 2 else None
        programs[name] = {"weight": weight, "children": children}
    return programs


def get_bottom_program(programs):
    """ Return the name of the bottom program. """
    # Look through all programs for one that doesn't appear in another's list of children.
    # This one is the bottom program.
    for prog in programs.keys():
        found = False
        for p in programs.values():
            if p["children"] and prog in p["children"]:
                found = True
                break
        if not found:
            return prog
    return None


def find_unique_value(values):
    """ From a list of numbers find the one that doesn't match the specific value """
    common_value = -1
    if values.count(values[0]) > 1:
        common_value = values[0]
    else:
        for v in values:
            if v != values[0]:
                common_value = v
                break

    for i, v in enumerate(values):
        if v != common_value:
            return i, v, common_value
    return -1, None


# Used to terminate the recursive search
unbalance_found = False

def find_unbalanced_weight(programs, program):
    """
    Recursive function for finding an unbalanced level in our stack / tower.
    When the unbalanced level is found we print the weight the program at
    that level would need to be to balance the tower and then exit.
    """
    global unbalance_found

    # Find the weights of all children balancing on this level
    child_total_weights = []
    if programs[program]["children"] is not None:
        for child in programs[program]["children"]:
            child_weight = programs[child]["weight"]
            child_carried_weight = find_unbalanced_weight(programs, child)
            child_total_weights.append(child_weight + child_carried_weight)

        # Exit if the unbalanced level has been found inside a leaf call
        if unbalance_found:
            return 0

        # Is there an imbalance a this level?
        if any(x != child_total_weights[0] for x in child_total_weights):
            index, value, target_weight = find_unique_value(child_total_weights)
            child = programs[program]["children"][index]
            needed_weight = programs[child]["weight"] - (value - target_weight)
            print(needed_weight)
            unbalance_found = True

    # Return the weight carried by this level
    carried_weight = sum(child_total_weights)
    return carried_weight


# Part 1
# Which program is at the bottom of the stack / tower?
progs = read_programs(data)
bottom_program = get_bottom_program(progs)
print(bottom_program)

# Part 2
# When we find an unbalanced level in the tower, what weight does the invalid
# program have to be to balance it?
find_unbalanced_weight(progs, bottom_program)
