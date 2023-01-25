"""
https://adventofcode.com/2015/day/10
"""
import functools
import itertools

rle_string = "3113322113"

@functools.cache
def get_rle_string(char, run_length):
    """
    Generates the string representing the RLE of char x run_length
    e.g. a, 3 -> 3a
    Uses functools.cache to reduce temp string generation
    """
    return str(run_length) + char

# Parts 1 & 2
# Speak and say / run-length encode the input string over and over and print
# the length of the final string.
# Iterate 40 times for part 1 and then 10 times more to get to 50 iterations
# for part 2
for iters in [40, 10]:
    for _ in range(iters):
        char_runs = [get_rle_string(k, len(list(v))) for k, v in itertools.groupby(rle_string)]
        rle_string = "".join(char_runs)
    print(len(rle_string))
