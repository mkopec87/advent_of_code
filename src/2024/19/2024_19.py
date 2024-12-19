import functools
from typing import List, Set, Tuple

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    towels, designs = parse_input(input_data)

    @functools.lru_cache()
    def possible(design: str) -> bool:
        if not design:
            # no more colors to match
            return True
        for towel in towels:
            if design[: len(towel)] == towel:
                # Use towel, try if the rest is possible
                if possible(design[len(towel) :]):
                    return True
        return False

    result_part1 = sum([1 if possible(design) else 0 for design in designs])

    @functools.lru_cache()
    def ways_possible(design: str) -> int:
        if not design:
            # one way to make empty design
            return 1
        ways = 0
        for towel in towels:
            if design[: len(towel)] == towel:
                # Use towel, add possible ways count to do the rest
                ways += ways_possible(design[len(towel) :])
        return ways

    result_part2 = sum([ways_possible(design) for design in designs])

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> Tuple[Set[str], List[str]]:
    spl = input_data.split("\n\n")
    towels = set(spl[0].split(", "))
    designs = spl[1].splitlines()
    print(len(towels), "towels")
    print(len(designs), "designs")
    print("Max design length:", max([len(design) for design in designs]))
    return towels, designs


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
