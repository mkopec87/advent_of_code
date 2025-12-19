import re

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    rows = []
    for line in input_data.splitlines():
        row = [ch for ch in line]
        rows.append(row)
    matrix = np.array(rows)
    shape = np.shape(matrix)
    print(shape)

    result_part1 = 0

    # horizontal
    for x in range(shape[0]):
        row = "".join(matrix[x, :].tolist())
        result_part1 += count_xmas(row)

    # vertical
    for y in range(shape[1]):
        row = "".join(matrix[:, y].tolist())
        result_part1 += count_xmas(row)

    # diagonal right-down
    for x in range(shape[0]):
        row = []
        y = 0
        while x < shape[0] and y < shape[1]:
            row.append(matrix[x, y])
            x += 1
            y += 1
        row = "".join(row)
        result_part1 += count_xmas(row)
    for y in range(1, shape[1]):
        row = []
        x = 0
        while x < shape[0] and y < shape[1]:
            row.append(matrix[x, y])
            x += 1
            y += 1
        row = "".join(row)
        result_part1 += count_xmas(row)

    # diagonal left-down
    for x in range(shape[0]):
        row = []
        y = shape[1] - 1
        while x < shape[0] and 0 <= y < shape[1]:
            row.append(matrix[x, y])
            x += 1
            y -= 1
        row = "".join(row)
        result_part1 += count_xmas(row)

    for y in range(shape[1] - 1):
        row = []
        x = 0
        while x < shape[0] and 0 <= y < shape[1]:
            row.append(matrix[x, y])
            x += 1
            y -= 1
        row = "".join(row)
        result_part1 += count_xmas(row)

    result_part2 = 0
    for start_x, start_y in np.ndindex(matrix.shape):
        diag1 = []
        x = start_x
        y = start_y
        while len(diag1) < 3 and x < shape[0] and y < shape[1]:
            diag1.append(matrix[x, y])
            x += 1
            y += 1
        diag2 = []
        x = start_x
        y = start_y + 2
        while len(diag2) < 3 and within_range(shape, x, y):
            diag2.append(matrix[x, y])
            x += 1
            y -= 1

        if len(diag1) != 3 or len(diag2) != 3:
            continue
        diag1 = "".join(diag1)
        diag2 = "".join(diag2)
        print(diag1, diag2)
        if count_mas(diag1) == 1 and count_mas(diag2) == 1:
            result_part2 += 1

    submit_or_print(result_part1, result_part2, debug)


def within_range(shape, x, y):
    return 0 <= x < shape[0] and 0 <= y < shape[1]


def count_xmas(row):
    return len(re.findall("XMAS", row)) + len(re.findall("XMAS", row[::-1]))


def count_mas(row):
    return len(re.findall("MAS", row)) + len(re.findall("MAS", row[::-1]))


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
