from dataclasses import dataclass
from math import prod

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Slope:
    right: int
    down: int


def main(debug: bool) -> None:
    input_data = load_data(debug)
    lines = input_data.splitlines()

    result_part1 = score_slope(lines, Slope(3, 1))

    slopes = [Slope(1, 1), Slope(3, 1), Slope(5, 1), Slope(7, 1), Slope(1, 2)]
    scores = [score_slope(lines, slope) for slope in slopes]
    result_part2 = prod(scores)

    submit_or_print(result_part1, result_part2, debug)


def score_slope(lines, slope):
    tree_count = 0
    column = 0
    row = 0
    while row < len(lines):
        if lines[row][column] == "#":
            tree_count += 1
        column = (column + slope.right) % len(lines[0])
        row += slope.down
    return tree_count


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
