import math
import re
from collections import defaultdict
from dataclasses import dataclass

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, direction: "Position"):
        return Position(self.x + direction.x, self.y + direction.y)

    def __mul__(self, d: int):
        return Position(self.x * d, self.y * d)

    def __rmul__(self, d: int):
        return self.__mul__(d)

    def __sub__(self, direction: "Position"):
        return Position(self.x - direction.x, self.y - direction.y)

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def __eq__(self, other: "Position"):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return f"[{self.x},{self.y}]"


@dataclass
class Robot:
    position: Position
    velocity: Position

    def quadrant(self, shape):
        mid_x = shape.x // 2
        mid_y = shape.y // 2
        if self.position.x == mid_x or self.position.y == mid_y:
            return None
        first_row = 0 if self.position.x < mid_x else 1
        first_col = 0 if self.position.y < mid_y else 1
        return first_row, first_col

    def advance(self, steps, shape):
        self.position = self.position + (self.velocity * steps)
        self.position.x = self.position.x % shape.x
        self.position.y = self.position.y % shape.y


def main(debug: bool) -> None:
    input_data = load_data(debug)

    robots = parse_robots(input_data)

    shape = Position(101, 103)
    steps = 100
    print(len(robots), "robots")
    print(shape)
    print(steps)

    # part 1
    quadrant_to_count = defaultdict(int)
    for robot in robots:
        robot.advance(steps, shape)
        quadrant = robot.quadrant(shape)
        if quadrant:
            quadrant_to_count[quadrant] += 1
    result_part1 = math.prod(quadrant_to_count.values())

    # part 2
    robots = parse_robots(input_data)

    step = 0
    while True:
        step += 1
        quadrant_to_count = defaultdict(int)
        for robot in robots:
            robot.advance(1, shape)
            quadrant = robot.quadrant(shape)
            quadrant_to_count[quadrant] += 1

        if max(quadrant_to_count.values()) > 0.5 * len(robots):
            print_map(step, robots, shape)
            result_part2 = step
            break

    submit_or_print(result_part1, result_part2, debug)


def parse_robots(input_data):
    robots = []
    for line in input_data.splitlines():
        m = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
        groups = m.groups()
        position = Position(int(groups[0]), int(groups[1]))
        velocity = Position(int(groups[2]), int(groups[3]))
        robots.append(Robot(position, velocity))
    return robots


def print_map(step, robots, shape):
    print()
    print(f"Step: {step}")
    positions = set()
    for r in robots:
        positions.add(r.position)
    for y in range(shape.y):
        for x in range(shape.x):
            print("*" if Position(x, y) in positions else ".", end="")
        print()
    print()


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
