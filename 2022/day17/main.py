import math
from enum import Enum

import numpy as np


class Direction(Enum):
    LEFT = "<"
    RIGHT = ">"


class Rock:
    id = 1

    def __init__(self, lines):
        self._id = Rock.id
        Rock.id += 1
        self._height = len(lines)
        self._width = max([len([ch for ch in l if ch == "#"]) for l in lines])
        self.points = set()
        for x, line in enumerate(lines):
            for y, ch in enumerate(line):
                if ch == "#":
                    self.points.add((x, y))

    def height(self):
        return self._height

    def width(self):
        return self._width

    def draw(self, chamber):
        for point in self.points:
            chamber[point] = "#"

    def valid_position(self, chamber):
        for point in self.points:
            if chamber[point] != ".":
                return False
        return True


class Chamber:
    VERTICAL_ROCK_SEPARATION = 3
    HORIZONTAL_ROCK_SEPARATION = 2

    def __init__(self, height, width):
        self.cut_rows = 0
        self.width = width + 2
        self.height = height + 1
        self.chamber = np.full((self.height, self.width), fill_value=".")
        self.chamber[:, 0] = "#"
        self.chamber[:, self.width - 1] = "#"
        self.chamber[self.height - 1, :] = "#"

    def show(self):
        print()
        for x in range(self.height):
            for y in range(self.width):
                print(self.chamber[x, y], end="")
            print()
        print()

    def ensure_height(self, rock):
        while True:
            x, _ = self.get_rock_initial_position(rock)
            if x < 0:
                self.make_space()
            else:
                break

    def top_rock_row(self):
        current_space = 0
        for current_space in range(self.height):
            if "#" in set(self.chamber[current_space, 1 : self.width - 1]):
                break
        return current_space

    def make_space(self):
        x = self.cutoff_row()
        if x < self.height - 1:
            self.cut_chamber(x)
        else:
            self.double_chamber()

    def cutoff_row(self):
        open_cols = set(range(1, self.width - 1))
        for x in range(self.height):
            new_open_cols = set()
            for start in open_cols:
                y = start
                while self.chamber[x, y] != "#":
                    new_open_cols.add(y)
                    y -= 1
                y = start
                while self.chamber[x, y] != "#":
                    new_open_cols.add(y)
                    y += 1
            if not new_open_cols:
                return x
            else:
                open_cols = new_open_cols

        return self.height

    def cut_chamber(self, height):
        self.cut_rows += self.height - height - 1
        self.height = height + 1
        self.chamber = np.resize(self.chamber, (self.height, self.width))

    def double_chamber(self):
        self.chamber = np.resize(self.chamber, (self.height * 2, self.width))
        for x in range(self.height):
            self.chamber[x, :] = "."
            self.chamber[x, 0] = "#"
            self.chamber[x, self.width - 1] = "#"
        self.height *= 2

    def get_rock_initial_position(self, rock):
        target_x = (
            self.top_rock_row() - Chamber.VERTICAL_ROCK_SEPARATION - rock.height()
        )
        target_y = 1 + Chamber.HORIZONTAL_ROCK_SEPARATION
        return target_x, target_y

    def sub_chamber(self, x, y, rock):
        return self.chamber[x : x + rock.height(), y : y + rock.width()]

    def state(self):
        return str(self.chamber)

    def score(self):
        return self.cut_rows + self.height - self.top_rock_row() - 1


class Repeater:
    def __init__(self, elements):
        self.elements = elements
        self.index = 0

    def next(self):
        d = self.elements[self.index]
        self.index += 1
        if self.index == self.size():
            self.index = 0
        return d

    def size(self):
        return len(self.elements)

    def reset(self):
        self.index = 0


def main():
    rocks = read_rocks()
    directions = read_directions("input.txt")
    print(rocks.size(), "rocks loaded")
    print(directions.size(), "directions loaded")

    result_part1 = solve(directions, rocks, 2022)
    result_part2 = solve(directions, rocks, 1000000000000)

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")  # expected for sample: 3068
    print(f"Result part 2: {result_part2}")  # expected for sample: 1514285714288


def solve(directions, rocks, rocks_count):
    rocks.reset()
    directions.reset()

    chamber_width = 7
    chamber_height = 10
    chamber = Chamber(chamber_height, chamber_width)

    cache = {}
    step = 0
    while step < rocks_count:
        state = (chamber.state(), rocks.index, directions.index)
        if state in cache:
            prev_step, prev_score = cache[state]
            cycle_length = step - prev_step
            score_increase = chamber.score() - prev_score

            cycles = math.floor((rocks_count - step - 1) / cycle_length)
            chamber.cut_rows += cycles * score_increase
            step += cycles * cycle_length
            cache.clear()
        else:
            cache[state] = step, chamber.score()
            drop_rock(chamber, directions, rocks)
            step += 1

    return chamber.score()


def drop_rock(chamber, directions, rocks):
    rock = rocks.next()
    chamber.ensure_height(rock)
    x, y = chamber.get_rock_initial_position(rock)
    falling = True
    while falling:

        # hot jet
        direction = directions.next()
        y2 = y + (1 if direction == Direction.RIGHT else -1)
        sub_chamber = chamber.sub_chamber(x, y2, rock)
        if rock.valid_position(sub_chamber):
            y = y2

        # fall
        x2 = x + 1
        sub_chamber = chamber.sub_chamber(x2, y, rock)
        if rock.valid_position(sub_chamber):
            x = x2
        else:
            falling = False
    sub_chamber = chamber.sub_chamber(x, y, rock)
    rock.draw(sub_chamber)


def read_rocks():
    with open("rocks.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    current_rock_lines = []
    rocks = []
    for line in lines:
        if line:
            current_rock_lines.append(line)
        else:
            rocks.append(Rock(current_rock_lines))
            current_rock_lines = []
    if current_rock_lines:
        rocks.append(Rock(current_rock_lines))

    rocks = Repeater(rocks)
    return rocks


def read_directions(path):
    with open(path) as f:
        lines = [line.strip() for line in f.readlines()]
    return Repeater([Direction(ch) for ch in lines[0]])


if __name__ == "__main__":
    main()
