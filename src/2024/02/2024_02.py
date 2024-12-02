from dataclasses import dataclass
from typing import List

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Report:
    levels: List[int]


def main(debug: bool) -> None:
    input_data = load_data(debug)

    reports = parse_input(input_data)

    result_part1 = 0
    for report in reports:
        if safe(report.levels):
            result_part1 += 1

    result_part2 = 0
    for report in reports:
        has_safe_version = False
        for excluded_index in range(len(report.levels)):
            levels_with_exclusion = (
                report.levels[:excluded_index] + report.levels[excluded_index + 1 :]
            )
            if safe(levels_with_exclusion):
                has_safe_version = True
                break
        if has_safe_version:
            result_part2 += 1

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> List[Report]:
    reports = []
    for line in input_data.splitlines():
        levels = [int(s) for s in line.split(" ")]
        reports.append(Report(levels))
    return reports


def safe(levels: List[int]) -> bool:
    pairs = list(zip(levels, levels[1:]))
    diffs = list(map(lambda p: p[0] - p[1], pairs))
    signs = {d > 0 for d in diffs}
    if len(signs) > 1:
        return False
    if any([abs(diff) > 3 for diff in diffs]):
        return False
    if 0 in diffs:
        return False
    return True


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
