from typing import Set

from aocd import data, submit
from itertools import combinations
from math import prod


def solve(numbers: Set[int], numbers_count: int, target_sum: int) -> int:
    sets = combinations(numbers, numbers_count)
    matching_sets = list(filter(lambda s: sum(s) == target_sum, sets))
    assert len(matching_sets) == 1
    matching_set = matching_sets[0]
    return prod(matching_set)


def main() -> None:
    numbers = set(int(line) for line in data.splitlines())
    print(len(numbers), "unique numbers read")

    submit(solve(numbers, 2, 2020), part="a")
    submit(solve(numbers, 3, 2020), part="b")


if __name__ == "__main__":
    main()
