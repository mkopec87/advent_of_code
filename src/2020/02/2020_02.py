import re
from collections import Counter
from typing import Any

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def parse_input(input_data: str) -> list[tuple[Any, ...]]:
    result = []
    for line in input_data.splitlines():
        m = re.match(r"(\d+)-(\d+) ([a-z]): ([a-z]+)", line)
        first_number = int(m.group(1))
        second_number = int(m.group(2))
        character = m.group(3)
        password = m.group(4)
        result.append((first_number, second_number, character, password))
    return result


def main(debug: bool) -> None:
    input_data = load_data(debug)

    lines = parse_input(input_data)

    def correct_part1(line: tuple[Any, ...]):
        first_number, second_number, character, password = line
        c = Counter(password)
        return first_number <= c[character] <= second_number

    result_part1 = len(list(filter(correct_part1, lines)))

    def correct_part2(line: tuple[Any, ...]):
        first_number, second_number, character, password = line
        password = " " + password  # make indexing 1-based
        return (password[first_number] == character) ^ (
            password[second_number] == character
        )

    result_part2 = len(list(filter(correct_part2, lines)))

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
