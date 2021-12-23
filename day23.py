"""
Find the least "energy" solution for moving amphipods in a grid into their 
correct rooms. 
A legal move consists a sequence of steps of one amphipod, where the move 
satisfies:
 - the end position isn't directly in front of a room 
 - if the move ends in a room, that must be its final position

"""
from os import stat
from helpers import begin_part_one, begin_part_two, solution, find_adjacent
import numpy as np

# The value for each amphipod is the x position
# of its home. For example, the Amber (A) amphipod
# has its home at x=3, therefore its code value is 3.
# This is useful when determining if an amphipod is at
# a home position
#            A, B, C, D
AMPHIPODS = [3, 5, 7, 9]


def char_to_num(char: str) -> int:
    # Wall
    if char == "#":
        return 1
    # Space
    if char == "." or char == " ":
        return 0
    # AMBER
    if char == "A":
        return 3
    # BRONZE
    if char == "B":
        return 5
    # COPPER
    if char == "C":
        return 7
    # DESERT
    if char == "D":
        return 9
    raise Exception(f"Invalid character {char}")


def get_delta(move):
    if move == "UP":
        return (-1, 0)
    if move == "DOWN":
        return (1, 0)
    if move == "RIGHT":
        return (0, 1)
    if move == "LEFT":
        return (0, -1)
    raise Exception(f"Invalid move {move}")


def pairwise_sum(a: tuple, b: tuple):
    return tuple(map(sum, zip(a, b)))


def get_legal_adjacents(state: np.ndarray, pos: tuple[int]):
    """
    Find all adjacent positions that are legal steps
    """
    next_positions = []
    for new_pos in find_adjacent(pos, state.shape):
        if state[new_pos] == 0:
            next_positions.append(new_pos)
    return next_positions


def is_safely_home(state: np.ndarray, pos: tuple[int], amphipod: int):
    """
    Determines if a position is safe for the amphipod to enter as
    its room
    """
    home_positions = [(2, amphipod), (3, amphipod)]
    return pos in home_positions and all(
        # home positions must either be empty or have the given amphipod in
        [
            (state[home_pos] == 0 or state[home_pos] == amphipod)
            for home_pos in home_positions
        ]
    )


def is_valid_endpoint(state: np.ndarray, pos: tuple[int], amphipod: int):
    """
    A valid ending position for a move is one with:
        walls to the top and bottom
        OR
        a position in the amphipods room, with no different
        amphipods in that room already
    """
    return (
        state[pairwise_sum(pos, get_delta("UP"))] == 1
        and state[pairwise_sum(pos, get_delta("DOWN"))] == 1
    ) or is_safely_home(state, pos, amphipod)


def expand_path(state: np.ndarray, path: list[tuple[int]], visited: list[tuple[int]]):
    new_visits = [
        next_pos
        for next_pos in get_legal_adjacents(state, path[-1])
        if next_pos not in visited
    ]
    new_paths = [path + [next_pos] for next_pos in new_visits]
    return new_paths, new_visits


def get_legal_moves_from(state: np.ndarray, initial_pos: tuple[int]):
    """
    Returns all possible legal moves (or paths) from a given initial
    position, together with the corresponding energy cost.

    A move consists of a sequence of positions with a valid endpoint
    """
    pos = initial_pos
    if state[pos] not in AMPHIPODS:
        raise Exception(
            f"Starting position must be an amphipod, but found value: {state[pos]}"
        )
    legal_paths = []
    visited = []
    paths = [[pos]]
    while True:
        discovered_paths = []
        for path in paths:
            if is_valid_endpoint(state, path[-1], path[0]):
                legal_paths.append(path)
            expanded_paths, new_visits = expand_path(state, path, visited)
            discovered_paths += expanded_paths
            visited += new_visits
        if len(discovered_paths) == 0:
            break
        paths = discovered_paths
    return legal_paths


def get_legal_moves(state: np.ndarray):
    moves = []
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i, j] in AMPHIPODS:
                moves += get_legal_moves_from(state, (i, j))
    return moves


with open("./inputs/day23.txt", "r") as file:
    lines = file.read().split("\n")

# Define a "move"
# A move is a sequence of positions. The initial position must always be the
# position of an amphipod

initial_state = np.array(
    [np.array([char_to_num(char) for char in line]) for line in lines]
)


print(initial_state)

begin_part_one()
moves = get_legal_moves(initial_state)
for move in moves:
    print(move)
solution()

begin_part_two()
solution()
