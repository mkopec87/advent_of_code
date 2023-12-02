from typing import Any, Optional

from aocd import submit


def submit_or_print(
    result_part1: Optional[Any], result_part2: Optional[Any], debug: bool
):
    print("Result part 1:", result_part1)
    print("Result part 2:", result_part2)
    if not debug:
        if result_part1 is not None:
            submit(result_part1, part="a")
        if result_part2 is not None:
            submit(result_part2, part="b")
