"""
https://adventofcode.com/2022/day/19
"""

# NOTE: This solution here is really slow.
# It highly likely that you could use a solver for this like sympy or z3 to
# make this considerably faster. I'm not veryfamiliar with this approach though
# so I'll save it for a learning exercise in future.

import copy
from utils import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def get_max_geodes(robot_build_costs, time):
    """
    Determine the maximum number of geodes that we can mine given the
    robot_build_costs and time supplied
    """

    initial_state = {
        "ore_robots": 1,
        "clay_robots": 0,
        "obsidian_robots": 0,
        "geode_robots": 0,
        "ore": 0,
        "clay": 0,
        "obsidian": 0,
        "geodes": 0,
        "time": time}
    max_geodes = 0

    state_queue = []
    state_queue.append(initial_state)
    processed = set()

    # Determine the maximum ore, clay and obsidian needed in any single step
    # Once we have enough robots to produce that much ore, clay and obsidian
    # per step then there's no need to build any more as it won't help us any
    # further
    max_ore_needed_per_step = max([robot["ore"] for robot in robot_build_costs.values()])
    max_clay_needed_per_step = robot_build_costs["obsidian"]["clay"]
    max_obsidian_needed_per_step = robot_build_costs["geode"]["obsidian"]

    # Pop states to process from the queue until there aren't any left and
    # we've exhausted all permustations
    while len(state_queue) > 0:
        state = state_queue.pop()

        # If we've seen this exact state before then we don't need to process
        # it again as we'd just be pushing new states that we've already seen
        # on the queue again
        if tuple(state.values()) in processed:
            continue
        else:
            processed.add(tuple(state.values()))

        # Has this state produced a new max number of geodes?
        max_geodes = max(max_geodes, state["geodes"])

        # We're out of time so no point creating new states to process
        time = state["time"]
        if time <= 0:
            continue

        # Need to do some pruning - there are way too many permutations here
        # for just naively brute forcing the whole thing.
        # Let's try throwing away states that seem unlikely to beat the current
        # max_geodes.
        # The maximum number of geodes that any state can generate is
        # (num geode robots * time) + (time*(time - 1) // 2)
        max_geodes_mineable = (state["geode_robots"] * time) + (time*(time - 1)//2)
        if state["geodes"] + max_geodes_mineable <= max_geodes:
            continue

        # Step the current state forward and accumulate mined ore, clay, etc..
        new_state = copy.deepcopy(state)
        new_state["ore"] += new_state["ore_robots"]
        new_state["clay"] += new_state["clay_robots"]
        new_state["obsidian"] += new_state["obsidian_robots"]
        new_state["geodes"] += new_state["geode_robots"]
        new_state["time"] -= 1

        # Create all of the permutations we can from here:
        # 1 - do nothing
        # 2 - build an ore robot
        # 3 - build a clay robot
        # 4 - build an obsidian robot
        # 5 - build a geode robot

        # 1 - don't do anything
        if tuple(new_state.values()) not in processed:
            state_queue.append(new_state)

        # 2 - build an ore robot if we can and it's worth it
        total_ore_from_current_robots = new_state["time"] * new_state["ore_robots"]
        total_ore_that_could_be_needed = max_ore_needed_per_step * new_state["time"]
        if total_ore_from_current_robots < total_ore_that_could_be_needed:
            if (robot_build_costs["ore"]["ore"] <= state["ore"] and
                new_state["ore_robots"] < max_ore_needed_per_step):

                new_state2 = copy.deepcopy(new_state)
                new_state2["ore"] -= robot_build_costs["ore"]["ore"]
                new_state2["ore_robots"] += 1
                state_queue.append(new_state2)

        # 2 - build a clay robot if we can and it's worth it
        total_clay_from_current_robots = new_state["time"] * new_state["clay_robots"]
        total_clay_that_could_be_needed = max_clay_needed_per_step * new_state["time"]
        if total_clay_from_current_robots < total_clay_that_could_be_needed:
            if (robot_build_costs["clay"]["ore"] <= state["ore"]
                and new_state["clay_robots"] < max_clay_needed_per_step):

                new_state2 = copy.deepcopy(new_state)
                new_state2["ore"] -= robot_build_costs["clay"]["ore"]
                new_state2["clay_robots"] += 1
                state_queue.append(new_state2)

        # 3 - build an obsidian robot if we can and it's worth it
        total_obsidian_from_current_robots = new_state["time"] * new_state["obsidian_robots"]
        total_obsidian_that_could_be_needed = max_obsidian_needed_per_step * new_state["time"]
        if total_obsidian_from_current_robots < total_obsidian_that_could_be_needed:
            if (robot_build_costs["obsidian"]["ore"] <= state["ore"] and
                robot_build_costs["obsidian"]["clay"] <= state["clay"] and
                new_state["obsidian_robots"] < max_obsidian_needed_per_step):

                new_state2 = copy.deepcopy(new_state)
                new_state2["ore"] -= robot_build_costs["obsidian"]["ore"]
                new_state2["clay"] -= robot_build_costs["obsidian"]["clay"]
                new_state2["obsidian_robots"] += 1
                state_queue.append(new_state2)

        # 4 - build a geode robot if we can
        if (robot_build_costs["geode"]["ore"] <= state["ore"] and
            robot_build_costs["geode"]["obsidian"] <= state["obsidian"]):

            new_state2 = copy.deepcopy(new_state)
            new_state2["ore"] -= robot_build_costs["geode"]["ore"]
            new_state2["obsidian"] -= robot_build_costs["geode"]["obsidian"]
            new_state2["geode_robots"] += 1
            state_queue.append(new_state2)

    return max_geodes


total_quality = 0
maximum_geodes = 1
for i, line in enumerate(data):

    # Read the blueprint data in
    ints = extract_ints(line)
    blueprint_id = ints[0]
    ore_robot_cost = {"ore": ints[1]}
    clay_robot_cost = {"ore": ints[2]}
    obsidian_robot_cost = {"ore": ints[3], "clay": ints[4]}
    geode_robot_cost = {"ore": ints[5], "obsidian": ints[6]}

    robot_costs = {"ore": ore_robot_cost,
                   "clay": clay_robot_cost,
                   "obsidian": obsidian_robot_cost,
                   "geode": geode_robot_cost}

    # Part 1
    # Sum the max geodes * blueprint id for each blueprint
    total_quality += blueprint_id * get_max_geodes(robot_costs, 24)

    # Part 2
    # For the first 3 blueprints only calculate the product of max geodes from
    # all 3 blueprints
    if i < 3:
        maximum_geodes *= get_max_geodes(robot_costs, 32)

print(total_quality)
print(maximum_geodes)
