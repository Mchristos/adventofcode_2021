import numpy as np
from helpers import read_input, begin_part_one, begin_part_two, solution

n_window = 3


def np_count_increases(numbers):
    return np.sum(np.diff(numbers) > 0)


def count_increases(numbers):
    count = 0
    for (i, number) in enumerate(numbers):
        if i == 0:
            continue
        if number > numbers[i - 1]:
            count += 1
    return count


input = read_input("./inputs/day1.txt")
numbers = [int(x) for x in input]

begin_part_one()
solution(np_count_increases(numbers))

begin_part_two()
window_values = []
for i in range(len(numbers) - n_window + 1):
    window = numbers[i : i + n_window]
    value = sum(numbers[i : i + n_window])
    window_values.append(value)
solution(np_count_increases(window_values))
