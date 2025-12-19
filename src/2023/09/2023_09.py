from collections.abc import Callable

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    seqs = parse_input(input_data)

    result_part1 = solve(seqs, score_part1)
    result_part2 = solve(seqs, score_part2)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> list[list[int]]:
    lines = input_data.splitlines()
    seqs = [[int(s) for s in l.split(" ")] for l in lines]
    return seqs


def solve(
    seqs: list[list[int]], scoring_function: Callable[[list[list[int]]], int]
) -> int:
    total = 0
    for seq in seqs:
        rows = []
        row = seq
        while not all([n == 0 for n in row]):
            rows.append(row)
            row = [(v[1] - v[0]) for v in zip(row, row[1:])]
        total += scoring_function(rows)
    return total


def score_part1(rows: list[list[int]]) -> int:
    inc = 0
    for row in reversed(rows):
        row.append(row[-1] + inc)
        inc = row[-1]
    return rows[0][-1]


def score_part2(rows: list[list[int]]) -> int:
    inc = 0
    for row in reversed(rows):
        row.insert(0, (row[0] - inc))
        inc = row[0]
    return rows[0][0]


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
