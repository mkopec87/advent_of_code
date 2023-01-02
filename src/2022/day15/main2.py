import re
from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from tqdm import tqdm


def manhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


@dataclass
class Sensor:
    pos: Tuple[int, ...]
    beacon: Tuple[int, ...]

    def dist(self):
        return manhattan(self.pos, self.beacon)


class Matrix:
    def __init__(self, shape, fill):
        self.shape = shape
        self.fill = fill
        self.key2val = {}

    def __setitem__(self, key, value):
        self.key2val[key] = value

    def __getitem__(self, item):
        return self.key2val.get(item, self.fill)


def print_board(board):
    print()
    for x in range(board.shape[0]):
        print(str(x).ljust(3), end="")
        for y in range(board.shape[1]):
            print(board[x, y], end="")
        print()
    print()


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")

    sensors = []
    for line in lines:
        m = re.match(
            r"Sensor at x=(-?\d+), y=(-?\d+): "
            r"closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        sensor = int(m.group(2)), int(m.group(1))  # switch x and y for viz
        beacon = int(m.group(4)), int(m.group(3))  # switch x and y for viz
        sensors.append(Sensor(sensor, beacon))

    m = 4_000_000
    result_part2 = solve(sensors, m, m)

    print()
    print("##########")
    print(f"Result part 2: {result_part2}")


def solve(sensors, x_target, y_target):
    for x in tqdm(range(x_target + 1)):
        intervals = set()
        for sensor in sensors:
            d = sensor.dist()
            x_diff = abs(sensor.pos[0] - x)
            r = d - x_diff
            if r >= 0:
                start = max(sensor.pos[1] - r, 0)
                end = min(sensor.pos[1] + r, y_target)
                if end >= start:
                    interval = pd.Interval(start, end, closed="both")
                    intervals.add(interval)
        intervals = merge(intervals)
        if len(intervals) == 2:
            solution_x = x
            solution_y = sorted(intervals)[0].right + 1
            return solution_y * 4_000_000 + solution_x


def merge(intervals):
    new_intervals = set()
    s = sorted(intervals)
    i = 0
    while i < len(s):
        current_min = s[i].left
        current_max = s[i].right
        while i + 1 < len(s) and s[i + 1].overlaps(
            pd.Interval(current_min, current_max, closed="both")
        ):
            current_max = max(s[i + 1].right, current_max)
            i += 1
        new_interval = pd.Interval(current_min, current_max, closed="both")
        new_intervals.add(new_interval)
        i += 1
    return new_intervals


if __name__ == "__main__":
    main()
