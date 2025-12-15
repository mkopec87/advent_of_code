from itertools import combinations
from math import prod

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def solve(numbers: set[int], numbers_count: int, target_sum: int) -> int:
    sets = combinations(numbers, numbers_count)
    matching_sets = list(filter(lambda s: sum(s) == target_sum, sets))
    assert len(matching_sets) == 1
    matching_set = matching_sets[0]
    return prod(matching_set)


def main(debug: bool) -> None:
    input_data = load_data(debug)

    numbers = {int(line) for line in input_data.splitlines()}

    result_part1 = solve(numbers, 2, 2020)
    result_part2 = solve(numbers, 3, 2020)

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
