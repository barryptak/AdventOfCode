"""
https://adventofcode.com/2023/day/1
"""

from utils.data import read_data

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

# This is not the fastest solution as we do process all chars in the string
# even if we don't need to.
# This does keep the code much cleaner though.

STR_NUMS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

total1 = 0
total2 = 0

for line in data:
    nums1 = []
    nums2 = []
    for i, char in enumerate(line):
        # If we find a single digit then add it to the list of parsed values
        # for both part 1 and part 2
        if char.isdigit():
            num = int(char)
            nums1.append(num)
            nums2.append(num)
        # If this wasn't a single digit then check if it's a number in string
        # form instead. If it is then add it to the list of parsed values for
        # part 2 only.
        else:
            for j, num in enumerate(STR_NUMS):
                if line[i:i+len(num)] == num:
                    nums2.append(j + 1)
                    break

    # Calibration values are only ever 2 digits so we know that we can just
    # multiply the first by 10 to get to the correct value.
    total1 += nums1[0]*10 + nums1[-1]
    total2 += nums2[0]*10 + nums2[-1]

print(total1)
print(total2)