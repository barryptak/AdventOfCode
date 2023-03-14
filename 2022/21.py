"""
https://adventofcode.com/2022/day/21
"""
import copy
import sympy
from sympy.parsing.sympy_parser import parse_expr
from utils.data import read_data

# NOTE: I'm still nto very familiar with sympy, but this is my attempt at using
# it to resolve a series of equations down to figuring out the missing value.
# Seemed similar to the problem I used it for in
# https://cs50.harvard.edu/ai/2020/

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def parse_data(input_data):
    """
    Read our data into two dictionaries: unknown values, and known values
    """
    unknown = {}
    known = {}

    for line in input_data:
        name, equation = line.split(": ")

        # If the value is a number (rather than an expression/equation) then we
        # can put it directly into the known list.
        if equation.isdigit():
            known[name] = int(equation)
        else:
            unknown[name] = equation.split()

    return unknown, known

def basic_solve(unknown, known):
    """
    Performs a trivial iterative resolve over the supplied data set.
    For each entry in unknown we check if both of the symbols required are now
    in the known set.
    If so then we can calculate the final value for the entry and add it to the
    known set itself.
    We repeat this until we can resolve no further unknown equations.
    """
    new_unknown = copy.deepcopy(unknown)
    new_known = copy.copy(known)

    # Loop until we can't resolve any further
    while True:
        del_list = []
        for name, equation in new_unknown.items():
            # If both symbols in the equation (e.g. 'abcd' and 'efgh') have
            # known values then create a valid python expression using the
            # known values and evaluate it.
            if equation[0] in new_known and equation[2] in new_known:
                eq_str = f"new_known['{equation[0]}'] {equation[1]} new_known['{equation[2]}']"
                new_known[name] = eval(eq_str)
                del_list.append(name)

        # Delete any now known entries from the unknown list
        for name in del_list:
            del new_unknown[name]

        # If we were not able to resolve any entries on this iteration then
        # we're done
        if len(del_list) == 0:
            break

    # Return the new known and unknown dictionaries once we've resolved as much
    # as we can
    return new_unknown, new_known


def sym_to_str(symbol, known):
    """
    Returns the resolved string representation of the supplied symbol.
    If the value is known then (the string of) this value is returned,
    otherwise the original symbol is return untouched.
    """
    return str(known.get(symbol, symbol))


def eq_to_expr(equation, known):
    """
    Creates a sympy expression from the supplied string equation.
    If the values of either symbol in the expression are known then the correct
    value is substituted in.
    """
    expr_str = f"{sym_to_str(equation[0], known)} {equation[1]} {sym_to_str(equation[2], known)}"
    return parse_expr(expr_str)


# Get our starting set of known and unknown values
unknown_values, known_values = parse_data(data)

# Part 1
# Calculate what root will eventually yell
_, known_values_1 = basic_solve(unknown_values, known_values)
print(int(known_values_1['root']))


# Part 2
# What does humn need to yell so that root's equality check passes?

# Remove the root and humn entries from the unknown list as they're not valid
# in the second part of the puzzle
root_eq = unknown_values["root"]
del unknown_values["root"]
del known_values["humn"]

# Solve as far as we can trivially
unknown_values_2, known_values_2 = basic_solve(unknown_values, known_values)

# Now use sympy to solve the remaining linear equations

# Create sympy equality expressions for every unknown value
equations = [sympy.Eq(eq_to_expr(equation, known_values_2), parse_expr(name))
                for name, equation in unknown_values_2.items()]

# Crete a sympy equality expression for root
# (the new operation for part 2 should be ==)
equations.append(sympy.Eq(parse_expr(sym_to_str(root_eq[0], known_values_2)),
                          parse_expr(sym_to_str(root_eq[2], known_values_2))))

# Now we just let sympy solve everything for us!
solution = sympy.solve(equations)
print(int(solution[sympy.symbols("humn")]))
