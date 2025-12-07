import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    result_part1 = solve_part1(input_data)
    result_part2 = solve_part2(input_data)

    submit_or_print(result_part1, result_part2, debug)


def solve_part1(input_data: str) -> int:
    grid = np.array([list(line) for line in input_data.splitlines()])

    result = 0
    for row_nr in range(1, grid.shape[0]):  # start from 2nd row
        for col_nr in range(grid.shape[1]):
            prev = grid[row_nr - 1, col_nr]
            if prev not in {"|", "S"}:
                continue
            curr = grid[row_nr, col_nr]
            match curr:
                case ".":
                    grid[row_nr, col_nr] = "|"
                case "^":
                    grid[row_nr, col_nr + 1] = "|"
                    grid[row_nr, col_nr - 1] = "|"
                    result += 1
                case "|":
                    pass
    return result


def solve_part2(input_data: str) -> int:
    rows = []
    for line in input_data.splitlines():
        row = []
        for ch in line:
            match ch:
                case ".":
                    row.append(0)
                case "S":
                    row.append(1)
                case "^":
                    row.append(-1)
        rows.append(row)
    grid = np.array(rows)

    for row_nr in range(1, grid.shape[0]):
        for col_nr in range(grid.shape[1]):
            prev = grid[row_nr - 1, col_nr]
            if prev < 1:
                continue
            curr = grid[row_nr, col_nr]
            if curr == -1:
                grid[row_nr, col_nr - 1] = grid[row_nr, col_nr - 1] + prev
                grid[row_nr, col_nr + 1] = grid[row_nr, col_nr + 1] + prev
            else:
                grid[row_nr, col_nr] = grid[row_nr, col_nr] + prev

    return sum(grid[-1, :])


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
