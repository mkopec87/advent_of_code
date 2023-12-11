import itertools
from typing import List, Tuple

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    galaxies, empty_xs, empty_ys = parse_input(input_data)

    result_part1 = solve(galaxies, empty_xs, empty_ys, 2)
    result_part2 = solve(galaxies, empty_xs, empty_ys, 1_000_000)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
    rows = []
    for line in input_data.splitlines():
        row = [ch for ch in line]
        rows.append(row)
    grid = np.matrix(rows)
    print(f"Galaxy shape: {grid.shape}")

    empty_xs = [x for x in range(grid.shape[0]) if (grid[x, :] == ".").all()]
    empty_ys = [y for y in range(grid.shape[1]) if (grid[:, y] == ".").all()]
    print(f"{len(empty_xs)} empty rows")
    print(f"{len(empty_ys)} empty cols")

    galaxies = []
    for x, y in np.ndindex(grid.shape):
        if grid[x, y] == "#":
            galaxies.append((x, y))
    print(len(galaxies), "galaxies")

    return galaxies, empty_xs, empty_ys


def solve(
    galaxies: List[Tuple[int, int]],
    empty_xs: List[int],
    empty_ys: List[int],
    multiplier=2,
) -> int:
    total = 0
    for g1, g2 in itertools.combinations(galaxies, 2):
        dx = abs(g1[0] - g2[0])
        dy = abs(g1[1] - g2[1])

        xs = sorted([g1[0], g2[0]])
        expanded_xs = [x for x in empty_xs if xs[0] < x < xs[1]]
        dx += len(expanded_xs) * (multiplier - 1)

        ys = sorted([g1[1], g2[1]])
        expanded_ys = [y for y in empty_ys if ys[0] < y < ys[1]]
        dy += len(expanded_ys) * (multiplier - 1)

        total += dx + dy

    return total


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
