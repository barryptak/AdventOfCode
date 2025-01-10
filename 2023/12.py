"""
https://adventofcode.com/2023/day/12
"""

from utils.data import read_data


USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def walk_springs(springs, broken_runs, spring_index=0, broken_run_index=0, broken_count=0):

    if spring_index == len(springs):
        if broken_run_index == len(broken_runs) and broken_count == 0:
            return 1
        elif broken_run_index == len(broken_runs) - 1 and broken_count == broken_runs[broken_run_index]:
            return 1
        else:
            return 0

    result = 0
    spring = springs[spring_index]
    if spring == ".":
        if broken_count > 0:
            if broken_run_index < len(broken_runs) and broken_count == broken_runs[broken_run_index]:
                result += walk_springs(springs, broken_runs, spring_index + 1, broken_run_index + 1, 0)
        else:
            result += walk_springs(springs, broken_runs, spring_index + 1, broken_run_index, 0)
    elif spring == "#":
        if broken_run_index < len(broken_runs) and broken_count < broken_runs[broken_run_index]:
            result += walk_springs(springs, broken_runs, spring_index + 1, broken_run_index, broken_count + 1)
    else:
        # As if this spring is a '#'
        if broken_run_index < len(broken_runs) and broken_count < broken_runs[broken_run_index]:
            result += walk_springs(springs, broken_runs, spring_index + 1, broken_run_index, broken_count + 1)

        # As if this spring is a '.'
        if broken_count > 0:
            if broken_run_index < len(broken_runs) and broken_count == broken_runs[broken_run_index]:
                result += walk_springs(springs, broken_runs, spring_index + 1, broken_run_index + 1, 0)
        else:
            result += walk_springs(springs, broken_runs, spring_index + 1, broken_run_index, 0)

    return result


total = 0
for line in data:
    springs, broken_runs = line.split(" ")
    broken_runs = [int(count) for count in broken_runs.split(",")]

    total += walk_springs(springs, broken_runs)

print(total)

total = 0
for line in data:
    springs, broken_runs = line.split(" ")
    springs = "?".join([springs]*5)
    broken_runs = ",".join([broken_runs]*5)
    broken_runs = [int(count) for count in broken_runs.split(",")]

    total += walk_springs(springs, broken_runs)

print(total)











# def matches_broken_runs(spring_states, broken_spring_runs):

#     # if all(spring_state == pattern for spring_state, pattern in zip(spring_states, [False, True, False, True, False, False, False])):
#     #     print("stop")

#     broken_count = 0
#     run_index = 0
#     for spring in spring_states:
#         if spring == ".":
#             if broken_count > 0:
#                 if run_index >= len(broken_spring_runs) or broken_count != broken_spring_runs[run_index]:
#                     return False
#                 run_index += 1
#                 broken_count = 0
#         else:
#             broken_count += 1

#     if broken_count > 0:
#         if run_index >= len(broken_spring_runs) or broken_count != broken_spring_runs[run_index]:
#             return False
#         run_index += 1

#     if run_index < len(broken_spring_runs):
#         return False

#     return True


# def generate_permutations(input_string):
#     # Count the number of '?' characters in the input string
#     num_question_marks = input_string.count('?')

#     # Generate all permutations where '?' can be '.' or '#'
#     permutations = product(['.', '#'], repeat=num_question_marks)

#     # Replace each '?' in the input string with each permutation
#     for permutation in permutations:
#         temp_string = input_string
#         for char in permutation:
#             temp_string = temp_string.replace('?', char, 1)
#         yield temp_string

# total = 0
# for line in data:
#     springs, broken_runs = line.split(" ")
#     broken_runs = [int(count) for count in broken_runs.split(",")]

#     count = 0
#     for permutation in generate_permutations(springs):
#         if matches_broken_runs(permutation, broken_runs):
#             count += 1

#     total += count

# print(total)
