"""
https://adventofcode.com/2015/day/4
"""
import hashlib

candidate_num = 1
five_zeros_num = 0
six_zeros_num = 0

while True:
    string_to_hash = "iwrupvqb" + str(candidate_num)
    result = hashlib.md5(string_to_hash.encode()).hexdigest()

    if not five_zeros_num and result.startswith("00000"):
        five_zeros_num = candidate_num

    if not six_zeros_num and result.startswith("000000"):
        six_zeros_num = candidate_num
        break

    candidate_num += 1

print(five_zeros_num)
print(six_zeros_num)
