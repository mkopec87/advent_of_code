from dataclasses import dataclass
from typing import List, Tuple

from tqdm import tqdm

INPUT_TXT = "input.txt"
INPUT_TXT = "input-small.txt"
INPUT_TXT = "input-smaller.txt"


@dataclass
class Step:
    on: bool
    ranges: List[Tuple[int, ...]]

    def within_range(self):
        for r in self.ranges:
            for v in r:
                if v > 50 or v < -50:
                    return False
        return True


def parse_step(line: str) -> Step:
    spl = line.split(" ")
    on = spl[0] == "on"
    ranges = []
    spl2 = spl[1].split(",")
    for s in spl2:
        vals = s.split("=")[1].split("..")
        ranges.append(tuple(map(int, vals)))
    return Step(on=on, ranges=ranges)


def parse_steps(lines: List[str]) -> List[Step]:
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


def part1(steps):
    class SparseMatrix:
        def __init__(self):
            self.elements = {}

        def set_value(self, tuple, value):
            if value == 0:
                if tuple in self.elements:
                    del self.elements[tuple]
            else:
                self.elements[tuple] = value

        def sum(self):
            return len(self.elements)

    steps = list(filter(Step.within_range, steps))
    space = SparseMatrix()
    for step in tqdm(steps):
        for x in range(step.ranges[0][0], step.ranges[0][1] + 1):
            for y in range(step.ranges[1][0], step.ranges[1][1] + 1):
                for z in range(step.ranges[2][0], step.ranges[2][1] + 1):
                    space.set_value((x, y, z), 1 if step.on else 0)

    result_part1 = space.sum()
    return result_part1


def find_shape_and_shift(steps):
    maxes = [0, 0, 0]
    mins = [0, 0, 0]
    for step in steps:
        for i, r in enumerate(step.ranges):
            maxes[i] = max(maxes[i], r[1])
            mins[i] = min(mins[i], r[0])
    shape = tuple(a[1] - a[0] + 1 for a in zip(mins, maxes))
    shifts = tuple(abs(m) for m in mins)
    return shape, shifts


def part2(steps):
    steps = list(filter(Step.within_range, steps))  # TODO: drop later

    return 0


if __name__ == "__main__":
    main()
