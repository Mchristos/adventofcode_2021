def begin_part_one():
    print("--- Part One ---")


def begin_part_two():
    print("--- Part Two ---")


def solution(value=""):
    print(f"Solution: {value}")


def read_input(path: str) -> list[str]:
    with open(path, "r") as file:
        return file.read().split("\n")