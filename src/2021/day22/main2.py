import itertools
import math
from dataclasses import dataclass

import numpy as np
from tqdm import tqdm

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"
# INPUT_TXT = "input-smaller.txt"


@dataclass
class Step:
    on: bool
    ranges: list[tuple[int, ...]]


def parse_step(line: str) -> Step:
    spl = line.split(" ")
    on = spl[0] == "on"
    ranges = []
    spl2 = spl[1].split(",")
    for s in spl2:
        vals = s.split("=")[1].split("..")
        ranges.append(tuple(map(int, vals)))
    return Step(on=on, ranges=ranges)


def parse_steps(lines: list[str]) -> list[Step]:
    return [parse_step(line) for line in lines]


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    steps = parse_steps(lines)

    result_part1 = part1(steps)
    result_part2 = part2(steps)

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


def part2(steps):
    distinct_coords = [set() for _ in steps[0].ranges]
    for step in steps:
        for i, r in enumerate(step.ranges):
            distinct_coords[i].update([r[0], r[1] + 1])

    distinct_coords = [sorted(s) for s in distinct_coords]

    shape = tuple(len(x) - 1 for x in distinct_coords)
    print("Shape:", shape)

    board = np.zeros(shape=shape)

    for step in tqdm(steps):
        indices = []
        for i, r in enumerate(step.ranges):
            r_min = r[0]
            r_max = r[1]
            indices.append(
                list(
                    range(
                        distinct_coords[i].index(r_min),
                        distinct_coords[i].index(r_max + 1),
                    )
                )
            )
        for coords in itertools.product(*indices):
            board[coords] = step.on

    s = 0
    for x, y, z in tqdm(np.ndindex(*shape), total=math.prod(shape)):
        if board[x, y, z]:
            lengths = [
                distinct_coords[i][v + 1] - distinct_coords[i][v]
                for i, v in enumerate([x, y, z])
            ]
            area = math.prod(lengths)
            s += area
    return s


def part1(steps):
    def within_range(step):
        for r in step.ranges:
            for v in r:
                if v > 50 or v < -50:
                    return False
        return True

    steps = list(filter(within_range, steps))
    return part2(steps)


if __name__ == "__main__":
    main()
