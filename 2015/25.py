"""
https://adventofcode.com/2015/day/25
"""

def triangular_number(num):
    """
    Returns the nth triangular number
    A triangular number is the sum of all previous numbers
    (like factorial but addition rather than multiplication)
    """
    return num * (num + 1) // 2


def num_in_sequence(row, col):
    """ Returns which number in the sequence any given row and column is """

    # Get the column number in the first row that's on the same diagonal as our
    # row + column
    end_of_diagonal_col = col + (row - 1)

    # Get the sequence number for the column in row 1 that we calcaulated above
    # and from there we can easily get the sequence number for our row +
    # column by subtracting how many rows away we are from row 1
    return triangular_number(end_of_diagonal_col) - row + 1


def modular_exponentiation(start, multiplier, divisor, exponent):
    """
    Performs the equivalent of (start*multiplier)%divisor repeated
    exponent times without needing exponent iterations.
    This approach results in a O(log(n)) cost instead.
    """
    result = start

    # Keep going until we've completed the iterations/exponent required
    while exponent > 0:
        # If the current exponent is odd then apply a single step of the
        # mul / mod operation
        if exponent % 2 == 1:
            result = (result * multiplier) % divisor

        # Reduce the exponent / num iterations by two and square the multiplier
        # (then mod it). This massively reduces the number of steps we need to
        # perform to get to the same final answer.
        exponent = exponent // 2
        multiplier = (multiplier * multiplier) % divisor

    return result


ROW = 2947
COLUMN = 3029
MUL = 252533
MOD = 33554393
START_VALUE = 20151125

seq_num = num_in_sequence(ROW, COLUMN)
code = modular_exponentiation(START_VALUE, MUL, MOD, seq_num - 1)
print(code)
