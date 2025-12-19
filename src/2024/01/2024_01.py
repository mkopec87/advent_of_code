import re
from collections import Counter

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)
    first, second = parse_lists(input_data)

    first = sorted(first)
    second = sorted(second)
    result_part1 = sum([abs(x[0] - x[1]) for x in zip(first, second)])

    counter = Counter(second)
    result_part2 = sum([f * counter[f] for f in first])

    submit_or_print(result_part1, result_part2, debug)


def parse_lists(input_data: str) -> tuple[list[int], list[int]]:
    first = []
    second = []
    for l in input_data.splitlines():
        spl = list(map(int, re.findall(r"\d+", l)))
        assert len(spl) == 2
        first.append(int(spl[0]))
        second.append(int(spl[1]))
    return first, second


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
