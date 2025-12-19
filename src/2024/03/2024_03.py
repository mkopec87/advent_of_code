import re

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)
    result_part1 = 0
    for m in re.finditer(r"mul\((\d+),(\d+)\)", input_data):
        a = int(m.group(1))
        b = int(m.group(2))
        result_part1 += a * b

    result_part2 = 0
    on = True
    for m in re.finditer(
        r"(?P<cmd>do|don't|mul)\(((?P<a>\d+),(?P<b>\d+))?\)", input_data
    ):
        match = m.group("cmd")
        print(match)
        if match == "don't":
            on = False
        elif match == "do":
            on = True
        elif on:
            a = int(m.group("a"))
            b = int(m.group("b"))
            result_part2 += a * b

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
