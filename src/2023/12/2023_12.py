import functools
import re
from typing import Any, Callable, List, Tuple

from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def parse_input(line: str, repeats: int = 1) -> Tuple[str, List[int]]:
    spl = line.split(" ")
    row = "?".join([spl[0]] * repeats).strip(".")
    groups = [int(x) for x in spl[1].split(",")]
    groups = groups * repeats
    return row, groups


def calc_groups(row: str) -> List[int]:
    groups = []
    group_len: int = 0
    prev_char = "."
    for r in row:
        if r == "#":
            group_len += 1
        else:
            if prev_char == "#":
                groups.append(group_len)
                group_len = 0
        prev_char = r
    if group_len > 0:
        groups.append(group_len)
    return groups


def lists_to_tuples(func: Callable) -> Any:
    @functools.wraps(func)
    def lists_to_tuples_wrapper(*args: Any, **kwargs: Any) -> bool:
        args = [tuple(x) if type(x) == list else x for x in args]
        return func(*args, **kwargs)

    return lists_to_tuples_wrapper


def tuples_to_lists(func: Callable) -> Any:
    @functools.wraps(func)
    def lists_to_tuples_wrapper(*args: Any, **kwargs: Any) -> bool:
        args = [list(x) if type(x) == tuple else x for x in args]
        return func(*args, **kwargs)

    return lists_to_tuples_wrapper


@lists_to_tuples
@functools.lru_cache(maxsize=100_000)
@tuples_to_lists
def arrangements(row: str, groups: List[int]) -> int:
    row = row.lstrip(".")
    if "?" not in row:
        expected_groups = calc_groups(row)
        if expected_groups != groups:
            return 0
        return 1

    first_unk_index = row.index("?")
    total = 0
    for opt in [".", "#"]:
        new_row = row[:first_unk_index] + opt + row[first_unk_index + 1 :]
        new_row = new_row.lstrip(".")

        # try dropping initial seq of hashes
        if m := re.match(r"(#+)\.", row):
            group_len = len(m.group(1))
            if not groups or groups[0] != group_len:
                continue  # not a valid solution
            total += arrangements(new_row[group_len:], groups[1:])
        else:
            total += arrangements(new_row, groups)

    return total


def main(debug: bool) -> None:
    input_data = load_data(debug)

    total = 0
    for line in tqdm(input_data.splitlines()):
        row, groups = parse_input(line)
        total += arrangements(row, groups)
    result_part1 = total

    total = 0
    for line in tqdm(input_data.splitlines()):
        row, groups = parse_input(line, 5)
        total += arrangements(row, groups)
    result_part2 = total

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
