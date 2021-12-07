from helpers import read_input, begin_part_one, begin_part_two, solution
import numpy as np


def compute_fuel(positions, point):
    return np.sum(np.abs(positions - point))


def solve(positions: np.ndarray, radius=500):
    mean = int(np.round(np.mean(positions)))
    print("mean =", mean)
    min_fuel = compute_fuel(positions, mean)
    for i in range(radius):
        if i < mean:
            fuel_left = compute_fuel(positions, mean - i)
            if fuel_left < min_fuel:
                min_fuel = fuel_left
        fuel_right = compute_fuel(positions, mean + i)
        if fuel_right < min_fuel:
            min_fuel = fuel_right
    return min_fuel


input = read_input("./inputs/day7.txt", splitlines=False)
crabmarines = np.array([int(x) for x in input.split(",")], dtype=int)
# crabmarines = np.array([16,1,2,0,4,2,7,1,2,14], dtype=int)

begin_part_one()
solution(solve(crabmarines))
begin_part_two()
solution()