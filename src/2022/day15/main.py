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

    ys = set()
    xs = set()
    sensors = []
    for line in lines:
        m = re.match(
            r"Sensor at x=(-?\d+), y=(-?\d+): "
            r"closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        sensor = int(m.group(2)), int(m.group(1))  # switch x and y for viz
        beacon = int(m.group(4)), int(m.group(3))  # switch x and y for viz

        d = manhattan(sensor, beacon)
        xs.update({sensor[0] - d, sensor[0] + d})
        ys.update({sensor[1] - d, sensor[1] + d})
        sensors.append(Sensor(sensor, beacon))

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    print("x range: ", min_x, max_x)
    print("y range: ", min_y, max_y)
    for sensor in sensors:
        sensor.pos = sensor.pos[0] - min_x, sensor.pos[1] - min_y
        sensor.beacon = sensor.beacon[0] - min_x, sensor.beacon[1] - min_y

    x_target = 2_000_000
    result_part1 = solve(min_x, sensors, x_target)

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")

    # part 1 small: 26
    # part 1: 5240818
    # part 2 small: 56000011
    # part 2: 13213086906101


def solve(min_x, sensors, x_target):
    x_target = x_target - min_x

    beacons_in_line = set()
    intervals = set()
    for sensor in tqdm(sensors):
        d = sensor.dist()
        x_diff = abs(sensor.pos[0] - x_target)
        r = d - x_diff
        if r >= 0:
            interval = pd.Interval(sensor.pos[1] - r, sensor.pos[1] + r, closed="both")
            intervals.add(interval)

        if sensor.beacon[0] == x_target:
            beacons_in_line.add(sensor.beacon[1])
    print(beacons_in_line)
    for i in sorted(intervals):
        print(i)
    print("")
    intervals = merge(intervals)
    for i in sorted(intervals):
        print(i, i.length + 1)
    result_part1 = sum([i.length + 1 for i in intervals]) - len(beacons_in_line)
    return result_part1


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
