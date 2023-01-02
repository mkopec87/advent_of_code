from typing import Tuple

import pandas as pd


def parse_line(line: str) -> Tuple[pd.Interval]:
    spl = line.split(",")
    return tuple(parse_interval(i) for i in spl)


def parse_interval(interval: str) -> pd.Interval:
    spl = interval.split("-")
    return pd.Interval(int(spl[0]), int(spl[1]), closed="both")


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")

    intervals = [parse_line(line) for line in lines]

    part1, part2 = 0, 0
    for interval1, interval2 in intervals:
        if interval1 in interval2 or interval2 in interval1:
            part1 += 1
        if interval1.overlaps(interval2) or interval2.overlaps(interval1):
            part2 += 1
    print(f"Result part 1: {part1}")
    print(f"Result part 1: {part2}")


if __name__ == "__main__":
    main()
