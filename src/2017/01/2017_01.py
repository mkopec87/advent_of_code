from typing import List

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)
    digits = [int(ch) for ch in input_data]

    result_part1 = solve(digits, 1)
    result_part2 = solve(digits, len(digits) // 2)

    submit_or_print(result_part1, result_part2, debug)


def solve(digits: List[int], shift: int) -> int:
    return sum([d for i, d in enumerate(digits) if digits[(i + shift) % len(digits)] == d])


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
