import re
from functools import reduce

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print

from operator import mul, add


def main(debug: bool) -> None:
    input_data = load_data(debug)

    result_part1 = solve_part1(input_data)
    result_part2 = solve_part2(input_data)

    submit_or_print(result_part1, result_part2, debug)


def solve_part1(input_data: str) -> int:
    rows = [re.split(r" +", line.strip()) for line in input_data.splitlines()]
    matrix = np.array(rows).transpose()
    result = 0
    for row in matrix:
        row = row.tolist()
        numbers = list(map(int, row[:-1]))
        op = mul if row[-1] == "*" else add
        result += reduce(op, numbers)
    return result


def solve_part2(input_data: str) -> int:
    matrix = np.array([list(line) for line in input_data.splitlines()])
    division_cols = [i for i, v in enumerate(matrix[-1, :]) if v in {"*", "+"}]
    division_cols.append(matrix.shape[1] + 1)

    result = 0
    for start_pos, end_pos in zip(division_cols, division_cols[1:]):
        result += solve_part2_problem(matrix[:, start_pos : end_pos - 1])
    return result


def solve_part2_problem(submatrix: np.ndarray) -> int:
    op = mul if submatrix[-1, 0] == "*" else add
    numbers = []
    for i in range(submatrix.shape[1]):
        col = submatrix[:, i]
        num = int("".join([c for c in col if re.match(r"[0-9]", c)]))
        numbers.append(num)
    return reduce(op, numbers)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
