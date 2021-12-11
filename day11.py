from helpers import read_input, begin_part_one, begin_part_two, solution

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def increment_at(password, back_index):
    if back_index == 1:
        # next letter
        i_next = (ALPHABET.index(password[-back_index]) + 1) % len(ALPHABET)
    else:
        # next letter IF one place forward just hit "a"
        if password[-back_index + 1] == "a":
            i_next = (ALPHABET.index(password[-back_index]) + 1) % len(ALPHABET)
        else:
            i_next = ALPHABET.index(password[-back_index]) % len(ALPHABET)
    new_password = list(password)
    new_password[-back_index] = ALPHABET[i_next]
    new_password = "".join(new_password)
    if i_next == 0:
        return increment_at(new_password, back_index + 1)
    else:
        return new_password


def force_increment_at(password, index):
    i_next = (ALPHABET.index(password[index]) + 1) % len(ALPHABET)
    new_password = list(password)
    new_password[index] = ALPHABET[i_next]
    if index < len(password) - 1:
        new_password[index + 1 :] = list("a" * (len(password) - index - 1))
    new_password = "".join(new_password)
    # print(f"Force increment from {password} to {new_password}")
    return new_password


def increment(password):
    return increment_at(password, 1)


def includes_straight(password: str):
    straight = [password[0]]
    for i in range(1, len(password)):
        if ALPHABET.index(password[i]) == ALPHABET.index(password[i - 1]) + 1:
            straight.append(password[i])
        else:
            straight = [password[i]]
        if len(straight) >= 3:
            return True
    return False


def contains_bad_chars(password: str):
    return ("i" in password) or ("o" in password) or ("l" in password)


def find_bad_char(password: str):
    min = 999
    for bad in ["i", "o", "l"]:
        try:
            bad_i = password.index(bad)
            if bad_i < min:
                min = bad_i
        except ValueError:
            continue
    return min


def contains_two_pairs(password: str):
    pairs = []
    for i in range(1, len(password)):
        if ALPHABET.index(password[i]) == ALPHABET.index(password[i - 1]):
            if password[i] not in pairs:
                pairs.append(password[i])
    if len(pairs) >= 2:
        # print(f"Found pairs {pairs} in {password}")
        return True
    else:
        return False


def is_valid(password: str):
    return (
        includes_straight(password)
        and contains_two_pairs(password)
        and not contains_bad_chars(password)
    )


input = "cqjxjnds"

begin_part_one()
valid = False
password = input
while not valid:
    if contains_bad_chars(password):
        password = force_increment_at(password, find_bad_char(password))
    else:
        password = increment(password)
    valid = is_valid(password)
solution(password)
begin_part_two()
solution()
