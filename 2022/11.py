"""
https://adventofcode.com/2022/day/11
"""
import copy
import math
from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = False
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)


class Operation:
    """ A multiply add (madd) operation used by Monkey objects """

    def __init__(self, mul, add):
        self.mul = mul
        self.add = add

    def execute(self, src):
        """ Executes this operation using the supplied rh value """
        mul = int(self.mul) if not self.mul == "old" else src
        add = int(self.add) if not self.add == "old" else src

        return (src * mul) + add


class Monkey:
    """
    Monkey object.
    Represents the monkey's worry and destination monkey logic
    """
    def __init__(self, items, operation, divisor, true, false):
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.true = true
        self.false = false
        self.inspections = 0

    def get_dest_monkey(self, item_worry):
        """ Gets the destination monkey (id) to pass the supplied item to """
        return self.true if item_worry % self.divisor == 0 else self.false


def parse_operation(operation_string):
    """ Parses the input string to generate a madd operation object """
    parts = operation_string.split()
    operator = parts[3]
    other = parts[4]

    mul = other if operator == "*" else 1
    add = other if operator == "+" else 0

    return Operation(mul, add)


def parse_monkeys(monkey_data):
    """
    Parses the raw input data and generates the list of Monkey objects it
    represents
    """
    monkey_list = []
    for monkey in monkey_data.split("\n\n"):
        lines = monkey.split("\n")
        items = extract_ints(lines[1])
        operation = parse_operation(lines[2][13:])
        test_divisor = extract_ints(lines[3])[0]
        true_monkey = extract_ints(lines[4])[0]
        false_monkey = extract_ints(lines[5])[0]

        monkey_list.append(
            Monkey(items, operation, test_divisor, true_monkey, false_monkey))

    return monkey_list


def run_rounds(num_rounds, monkeys, lcf=None):
    """
    Runs the monkey item passing algorithm for the supplied number of runs.
    If lcf is supplied then we use it to keep the maths within sensible bounds.
    Returns the final monkey business score for the rounds.
    """

    for _ in range(num_rounds):
        for monkey in monkeys:
            for item in monkey.items:
                # Transform the worry value for this item using the monkey's
                # operation
                new_item = monkey.operation.execute(item)

                # If a lowest common factor was provided (part 2) then mod
                # the worry value by this in order to keep within sensible maths
                # limits. lcf has every monkey's divisor as a factor of it, so
                # it's safe to divide by it without breaking any of our % maths
                # tests.
                # If no lcf is provided (part 1) then we need to divide the
                # worry value by 3 instead as per the instructions.
                new_item = new_item % lcf if lcf else new_item // 3

                # Pass the item to the appropriate new monkey
                dest_monkey = monkey.get_dest_monkey(new_item)
                monkeys[dest_monkey].items.append(new_item)

            # Accumulate the number of inspections performed by this monkey
            # and reset their item list since we've finished with it for this
            # round.
            monkey.inspections += len(monkey.items)
            monkey.items = []

    # Get the largest two inspection counts and multiply them together to get
    # the monkey business score
    inspections = [monkey.inspections for monkey in monkeys]
    inspections = sorted(inspections, reverse=True)
    monkey_business = inspections[0] * inspections[1]
    return monkey_business

# Parse the data in
monkeys1 = parse_monkeys(data)
monkeys2 = copy.deepcopy(monkeys1)

# Part 1
# Score for 20 rounds
monkey_business_1 = run_rounds(20, monkeys1)
print(monkey_business_1)

# Part 2
# Score for 10000 rounds

# Determine the lowest value that all divisors can safely divide into by
# multiplying them all together. We use this to % the item worry values to keep
# the values within sensible limits without breaking the % tests that we
# perform to determine the monkey to pass to. 
lowest_common_factor = math.prod([monkey.divisor for monkey in monkeys2])
monkey_business_2 = run_rounds(10000, monkeys2, lowest_common_factor)
print(monkey_business_2)