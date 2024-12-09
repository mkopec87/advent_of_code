import dataclasses
import math
from collections import defaultdict
from itertools import combinations
from typing import Dict, Set, Tuple

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def __eq__(self, other: "Point"):
        return (self.x == other.x) and (self.y == other.y)

    def direction(self):
        gcd = math.gcd(self.x, self.y)
        return Point(self.x // gcd, self.y // gcd)

    def within_bounds(self, shape):
        return 0 <= self.x < shape.x and 0 <= self.y < shape.y


def main(debug: bool) -> None:
    input_data = load_data(debug)

    letter_to_antennas, shape = parse_input(input_data)

    antinodes = antinodes_part1(letter_to_antennas, shape)
    result_part1 = len(antinodes)

    antinodes = antinodes_part2(letter_to_antennas, shape)
    result_part2 = len(antinodes)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> Tuple[Dict[str, Set[Point]], Point]:
    letter_to_antennas = defaultdict(set)
    lines = input_data.splitlines()
    for x, line in enumerate(lines):
        for y, ch in enumerate(line):
            if ch != ".":
                letter_to_antennas[ch].add(Point(x, y))
    shape = Point(len(lines), len(lines[0]))
    return letter_to_antennas, shape


def antinodes_part1(
    letter_to_antennas: Dict[str, Set[Point]], shape: Point
) -> Set[Point]:
    antinodes = set()
    for letter, antennas in letter_to_antennas.items():
        for antenna1, antenna2 in combinations(antennas, 2):
            diff = antenna1 - antenna2
            resonance1 = antenna2 - diff
            resonance2 = antenna1 + diff
            for p in [resonance1, resonance2]:
                if p.within_bounds(shape):
                    antinodes.add(p)
    return antinodes


def antinodes_part2(
    letter_to_antennas: Dict[str, Set[Point]], shape: Point
) -> Set[Point]:
    antinodes = set()
    for letter, antennas in letter_to_antennas.items():
        for antenna1, antenna2 in combinations(antennas, 2):
            diff = (antenna1 - antenna2).direction()

            p = antenna1
            while p.within_bounds(shape):
                antinodes.add(p)
                p = p + diff

            p = antenna1
            while p.within_bounds(shape):
                antinodes.add(p)
                p = p - diff

    return antinodes


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
