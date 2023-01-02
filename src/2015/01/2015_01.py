from collections import Counter

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    c = Counter(input_data)
    result_part1 = c["("] - c[")"]

    floor = 0
    result_part2 = None
    for position, ch in enumerate(input_data, start=1):
        floor += 1 if ch == "(" else -1
        if floor == -1:
            result_part2 = position
            break

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
