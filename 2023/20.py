"""
https://adventofcode.com/2023/day/19
"""
import collections
import copy
import math
from math import prod
from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

ON = True
OFF = False
LOW = False
HIGH = True

modules = {}
inputs = {}
states = {}
for line in data:
    module_name, outputs = line.split(' -> ')
    module_type = None
    if module_name[0] in '%&':
        module_type = {"%": "FlipFlop", "&": "Conjunction"}[module_name[0]]
        module_name = module_name[1:]
    elif module_name == "broadcaster":
        module_type = "Broadcast"

    outputs = outputs.split(', ')
    modules[module_name] = {"type": module_type, "outputs": outputs}

    for output in outputs:
        if output not in inputs:
            inputs[output] = set()
        inputs[output].add(module_name)
        if output not in modules:
            modules[output] = {"type": None, "outputs": []}

    if module_type == "FlipFlop":
        states[module_name] = OFF

for module_name, module_info in modules.items():
    if module_info["type"] == "Conjunction":
        states[module_name] = {input: LOW for input in inputs[module_name]}


def press_button(count):

    pulses_sent = {LOW: 0, HIGH: 0}

    # For part 2 we want to determine when rx receives a LOW pulse.
    # This is going to take way too long to do by brute force.
    # Instead, looking at the input data we can see that rx received a LOW
    # pulse when df receives all HIGH pulses from its inputs xl, ln, xp & gp.
    # They are all single input conjunctions (i.e. inverters) and so we want to
    # know when they all received a LOW pulse.
    # By recording their cycles we can find the lowest common multiple of their
    # cycles lengths and find how long it will take for them to all line up.
    part_2_modules = {"xl": [], "ln": [], "xp": [], "gp": []}

    cycle = 0
    while True:
        if cycle >= count:
            break

        queue = collections.deque()
        queue.append((LOW, "button", ["broadcaster"]))

        while len(queue) > 0:
            (pulse, sender, outputs) = queue.popleft()
            for output in outputs:
                pulses_sent[pulse] += 1
                output_module = modules[output]
                output_module_type = output_module["type"]

                if pulse == LOW and output in part_2_modules:
                    part_2_modules[output].append(cycle)
                    if all(len(cycles) >= 2 for cycles in part_2_modules.values()):
                        cycle_lengths = [cycles[-1] - cycles[-2] for cycles in part_2_modules.values()]
                        return None, math.lcm(*cycle_lengths)

                if output_module_type == "Broadcast":
                    queue.append((pulse, output, output_module["outputs"]))
                elif output_module_type == "FlipFlop":
                    if pulse == LOW:
                        states[output] = not states[output]
                        new_pulse = HIGH if states[output] == ON else LOW
                        queue.append((new_pulse, output, output_module["outputs"]))
                elif output_module_type == "Conjunction":
                    states[output][sender] = pulse
                    new_pulse = LOW if all(states[output].values()) else HIGH
                    queue.append((new_pulse, output, output_module["outputs"]))

        cycle += 1

    return prod(pulses_sent.values()), None



states2 = copy.deepcopy(states)

result, _ = press_button(1000)
print(result)

_, result2 = press_button(math.inf)
print(result2)
