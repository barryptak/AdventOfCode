"""
https://adventofcode.com/2023/day/9
"""

from utils.data import read_data, extract_ints

USE_TEST_DATA = False
SPLIT_BY_LINE = True
data = read_data(USE_TEST_DATA, SPLIT_BY_LINE)

def generate_diffs(nums):
    return [b - a for a, b in zip(nums, nums[1:])]

total = 0
for line in data:
    nums = extract_ints(line)
    nums_list = [nums]

    while not all(num == 0 for num in nums_list[-1]):
        nums_list.append(generate_diffs(nums_list[-1]))

    nums_list[-1].append(0)
    nums_list.reverse()

    for nums1, nums2 in zip(nums_list, nums_list[1:]):
        nums2.append(nums1[-1] + nums2[-1])

    total += nums_list[-1][-1]

print(total)


total2 = 0
for line in data:
    nums = extract_ints(line)
    nums_list = [nums]

    while not all(num == 0 for num in nums_list[-1]):
        nums_list.append(generate_diffs(nums_list[-1]))

    nums_list[-1].append(0)
    nums_list.reverse()

    for nums1, nums2 in zip(nums_list, nums_list[1:]):
        nums2.insert(0, nums2[0] - nums1[0])

    total2 += nums_list[-1][0]

print(total2)
