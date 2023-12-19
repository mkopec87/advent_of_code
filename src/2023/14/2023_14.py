from typing import Tuple

import numpy as np
from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print

N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)


def main(debug: bool) -> None:
    input_data = load_data(debug)

    # part 1
    grid = parse_input(input_data)
    roll(grid, N)
    result_part1 = measure_load(grid)

    # part 2
    grid = parse_input(input_data)

    iters = 1000000000
    known = {}
    for step in tqdm(range(iters)):
        grid_str = grid_to_str(grid)
        if grid_str in known:
            prefix_len = known[grid_str]
            cycle_len = step - prefix_len
            iters -= prefix_len
            iters = iters % cycle_len
            break
        known[grid_str] = step
        roll_cycle(grid)
    for _ in range(iters):
        roll_cycle(grid)
    result_part2 = measure_load(grid)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> np.array:
    rows = []
    for line in input_data.splitlines():
        rows.append(["#"] + list(line) + ["#"])
    rows.insert(0, ["#" for _ in range(len(rows[0]))])
    rows.append(["#" for _ in range(len(rows[0]))])
    return np.array(rows)


def roll(grid: np.array, direction: Tuple[int, int]) -> None:
    changed = True
    while changed:
        changed = False
        if direction == N:
            for x in range(grid.shape[0]):
                for y in range(grid.shape[1]):
                    if grid[x, y] == "O" and grid[x - 1, y] == ".":
                        grid[x - 1, y] = "O"
                        grid[x, y] = "."
                        changed = True
        elif direction == S:
            for x in reversed(range(grid.shape[0])):
                for y in range(grid.shape[1]):
                    if grid[x, y] == "O" and grid[x + 1, y] == ".":
                        grid[x + 1, y] = "O"
                        grid[x, y] = "."
                        changed = True
        elif direction == E:
            for y in range(grid.shape[1]):
                for x in range(grid.shape[0]):
                    if grid[x, y] == "O" and grid[x, y + 1] == ".":
                        grid[x, y + 1] = "O"
                        grid[x, y] = "."
                        changed = True
        elif direction == W:
            for y in reversed(range(grid.shape[1])):
                for x in range(grid.shape[0]):
                    if grid[x, y] == "O" and grid[x, y - 1] == ".":
                        grid[x, y - 1] = "O"
                        grid[x, y] = "."
                        changed = True


def roll_cycle(grid: np.array) -> None:
    for direction in [N, W, S, E]:
        roll(grid, direction)


def grid_to_str(grid: np.array) -> str:
    s = ""
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            s += grid[x, y]
        s += "\n"
    return s


def measure_load(grid: np.array) -> int:
    total = 0
    for x in range(grid.shape[0]):
        rocks_in_row = (grid[x, :] == "O").sum()
        total += rocks_in_row * (grid.shape[0] - x - 1)
    return total


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
