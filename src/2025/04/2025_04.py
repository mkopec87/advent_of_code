from itertools import repeat, product

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    grid = parse_input(input_data)

    result_part1 = solve_part1(grid)
    result_part2 = solve_part2(grid)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> np.ndarray:
    rows = [list(line) for line in input_data.splitlines()]
    # add guards
    for row in rows:
        row.insert(0, ".")
        row.append(".")
    rows.insert(0, list(repeat(".", len(rows[0]))))
    rows.append(list(repeat(".", len(rows[0]))))

    return np.array(rows)


def solve_part1(grid: np.ndarray) -> int:
    result = 0
    it = np.nditer(grid, flags=["multi_index"])
    for elem in it:
        if elem == "@":
            x, y = it.multi_index
            neighboring_rolls = 0
            for xd, yd in product([-1, 0, 1], [-1, 0, 1]):
                if xd == yd == 0:
                    continue
                if grid[x + xd, y + yd] == "@":
                    neighboring_rolls += 1
            if neighboring_rolls < 4:
                result += 1
    return result


def solve_part2(grid: np.ndarray) -> int:
    result = 0
    while True:
        removed = False
        it = np.nditer(grid, flags=["multi_index"])
        for elem in it:
            if elem == "@":
                x, y = it.multi_index
                neighboring_rolls = 0
                for xd, yd in product([-1, 0, 1], [-1, 0, 1]):
                    if xd == yd == 0:
                        continue
                    if grid[x + xd, y + yd] == "@":
                        neighboring_rolls += 1
                if neighboring_rolls < 4:
                    grid[x, y] = "."
                    result += 1
                    removed = True
        if not removed:
            break
    return result


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
