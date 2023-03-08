"""
https://adventofcode.com/2016/day/11
"""

import re
from bisect import insort
from itertools import chain
from utils import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


class Floor:
    """
    Class representing the contents of a single floor
    """
    def __init__(self, generators=None, microchips=None):
        # We presume that the lists are already sorted!
        self.generators = generators or []
        self.microchips = microchips or []

    def is_good(self):
        """
        Is the configuration of this floor good/safe (True) or will it cause a
        microchip to become fried?
        """
        return not any(chip not in self.generators
                       for chip in self.microchips if len(self.generators) > 0)

    def clone(self):
        """ Creates a clone of this Floor. This is faster than deepcopy. """
        return Floor(list(self.generators), list(self.microchips))

    def __eq__(self, other):
        return self.generators == other.generators and self.microchips == other.microchips

    def __hash__(self):
        return hash((tuple(self.generators), tuple(self.microchips)))


class State:
    """
    Class representing the entire building state including elevator position
    and the contents of each floor
    """
    def __init__(self, elevator, floors):
        self.elevator = elevator
        self.floors = floors

    def get_score(self):
        """
        Score is how far we are from goal state (lower is better)
        Goal is all items on floor index 3.
        """
        score = 0
        for i, floor in enumerate(self.floors[:3]):
            score += (3 - i) * (len(floor.generators) + len(floor.microchips))
        return score

    def is_goal_state(self):
        """ Is this the goal state where all floors other than 3 are empty? """
        return self.get_score() == 0

    def clone(self):
        """ Creates a clone of this State. This is faster than deepcopy. """
        return State(self.elevator, [floor.clone() for floor in self.floors])

    def __eq__(self, other):
        return self.elevator == other.elevator and self.floors == other.floors

    def __lt__(self, other):
        return self.get_score() < other.get_score()

    def __hash__(self):
        return hash((self.elevator, *map(hash, self.floors)))


def parse_data(input_data):
    """ Parses the input data to create the initial building/floor layout """
    floors = []

    for line in input_data:
        generators = re.findall(r" (\w+) generator", line)
        microchips = re.findall(r" (\w+)-compatible", line)
        floors.append(Floor(sorted(generators), sorted(microchips)))

    return State(0, floors)


def move_item(state, current_floor_num, next_floor_num, item, is_gen, new_states, max_score):
    """ Moves the supplied item from the current floor to the next floor """

    # Clone the current state
    new_state = state.clone()
    new_state.elevator = next_floor_num
    current_floor = new_state.floors[current_floor_num]
    next_floor = new_state.floors[next_floor_num]

    # Move the item to/from either the generators or microchips lists depending
    # on its type
    current_item_list = current_floor.generators if is_gen else current_floor.microchips
    next_item_list = next_floor.generators if is_gen else next_floor.microchips
    current_item_list.remove(item)
    insort(next_item_list, item)

    # If the new configuration is valid (no chips are fried) and it meets the
    # score bar then add it to to the list of new states
    if current_floor.is_good() and next_floor.is_good() and new_state.get_score() < max_score:
        new_states.append(new_state)

    return new_state


def generate_next_valid_states(state, max_score):
    """
    Returns a list of all of the valid states (those that don't fry any chips)
    that can be moved to from the passed in state.
    States with a score worse than max_score are also discarded.
    """
    new_states = []
    floor_num = state.elevator
    floors = state.floors
    current_floor = floors[floor_num]
    generators = current_floor.generators
    microchips = current_floor.microchips

    # Iterate over all of the valid floors to move from here
    floor_nums = [f for f in [floor_num - 1, floor_num + 1] if 0 <= f <= 3]
    for next_floor_num in floor_nums:
        # Iterate over a combined list of all generators and microchips on the
        # current floor. We're going to pick out one to move and then iterate
        # over the remaining items and pick one of those to also move too.
        for index, item in enumerate(chain(generators, microchips)):
            # Move the first picked item
            # Moving an item will add the new state to new_states IF this new
            # state is valid (won't fry a chip)
            item_is_gen = index < len(generators)
            new_state = move_item(state, floor_num, next_floor_num,
                                  item, item_is_gen, new_states, max_score)

            # Create an iterator that will walk over the remaining generators
            # and microchips from the current floor
            remaining_items_it = chain(generators[index + 1:],
                                       microchips[index - len(generators) + 1:])
            for index2, item2 in enumerate(remaining_items_it):
                # Move the second picked item
                item2_is_gen = item_is_gen and (index2 + index + 1) < len(generators)
                move_item(new_state, floor_num, next_floor_num,
                          item2, item2_is_gen, new_states, max_score)

    return new_states


def find_min_steps(starting_state):
    """
    Returns the minimum number of steps needed to move all generators and
    microchips to the top floor
    """
    visited = set()
    count = 0
    states = [starting_state]
    max_score = starting_state.get_score()

    # Keep going while we have valid states to check
    while len(states) > 0:
        new_states = []
        curr_max_score = 0
        # Iterate over all of the valid states for the current step number
        for state in states:
            # Check if we've seen this state before.
            # If we have then we can skip it - no point processing it again.
            state_hash = hash(state)
            if state_hash in visited:
                continue
            visited.add(state_hash)

            # Have we reached our goal state?
            if state.is_goal_state():
                return count

            #max_score = min(max_score, state.get_score()) + 4

            # Add the new states that you can move to from the current one to a
            # list for processing next time round the outer loop
            new_states.extend(generate_next_valid_states(state, max_score))

            # Optimisation - dont consider any states that have a worse score
            # than the worst score from the previous round
            curr_max_score = max(curr_max_score, state.get_score())

        max_score = curr_max_score
        states = new_states
        count += 1

    # No solution
    return -1


# Part 1
# What is the minimum number of steps needed to move all generators and
# microchips to the top floor?
initial_state = parse_data(data)
print(find_min_steps(initial_state))

# Part 2
# How many steps does it take if we add a further two generators and microchips
# to the bottom floor?
# NOTE: This is pretty slow. I presume that there's some trick I'm missing.
first_floor = initial_state.floors[0]
insort(first_floor.generators, "dilithium")
insort(first_floor.generators, "elerium")
insort(first_floor.microchips, "dilithium")
insort(first_floor.microchips, "elerium")
print(find_min_steps(initial_state))
