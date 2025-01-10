"""
https://adventofcode.com/2023/day/19
"""

import copy
from math import prod
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

workflows_data, parts = data.split("\n\n")
workflows = {}
parts = parts.split("\n")

for workflow in workflows_data.split("\n"):
    rules = []

    name, rules_data = workflow.split("{")
    for rule in rules_data[:-1].split(","):
        rule_parts = rule.split(":")
        if len(rule_parts) == 1:
            rules.append(("True", rule_parts[0]))
        else:
            rules.append(tuple(rule_parts))
    workflows[name] = rules



parts = [{"x": x, "m": m, "a": a, "s": s} for x,m,a,s in [extract_ints(part) for part in parts]]


accepted = []
rejected = []
accepted_total = 0

for part in parts:
    workflow = workflows["in"]
    finished = False
    while not finished:
        for rule in workflow:
            x = part["x"]
            m = part["m"]
            a = part["a"]
            s = part["s"]
            if eval(rule[0]):
                next_workflow = rule[1]
                if next_workflow == "A":
                    accepted.append(part)
                    accepted_total += sum(part.values())
                    finished = True
                    break
                elif next_workflow == "R":
                    rejected.append(part)
                    finished = True
                    break
                else:
                    workflow = workflows[next_workflow]
                    break

print(accepted_total)



def walk_workflow(workflow, rule_index, part_ranges):
    total = 0
    rule = workflow[rule_index]
    letter = ""
    if "<" in rule[0]:
        letter, value = rule[0].split("<")
        value = int(value)
        true_range = range(part_ranges[letter].start, value)
        false_range = range(value, part_ranges[letter].stop)
    elif ">" in rule[0]:
        letter, value = rule[0].split(">")
        value = int(value)
        true_range = range(value + 1, part_ranges[letter].stop)
        false_range = range(part_ranges[letter].start, value + 1)
    else:
        assert(rule[0] == "True")
        if rule[1] == "R":
            return total

        if rule[1] == "A":
            total += prod(len(letter_range) for letter_range in part_ranges.values())
        elif rule[1] != "R":
            total += walk_workflow(workflows[rule[1]], 0, part_ranges)
        return total

    true_ranges = copy.deepcopy(part_ranges)
    true_ranges[letter] = true_range
    false_ranges = copy.deepcopy(part_ranges)
    false_ranges[letter] = false_range

    if rule[1] == "A":
        total += prod(len(letter_range) for letter_range in true_ranges.values())
    elif rule[1] != "R":
        total += walk_workflow(workflows[rule[1]], 0, true_ranges)

    total += walk_workflow(workflow, rule_index + 1, false_ranges)
    return total


result = walk_workflow(workflows["in"], 0, {"x": range(1, 4001), "m": range(1, 4001), "a": range(1, 4001), "s": range(1, 4001), })
print(result)