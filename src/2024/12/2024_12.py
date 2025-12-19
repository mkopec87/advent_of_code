import enum
from collections import deque
from dataclasses import dataclass

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, direction: "Direction"):
        return Position(self.x + direction.value.x, self.y + direction.value.y)

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def __eq__(self, other: "Position"):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def possible(self, shape):
        return 0 <= self.x < shape[0] and 0 <= self.y < shape[1]


class Direction(enum.Enum):
    NORTH = Position(-1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(1, 0)
    WEST = Position(0, -1)

    def next(self):
        directions = list(Direction)
        return directions[(directions.index(self) + 1) % len(Direction)]

    def prev(self):
        directions = list(Direction)
        return directions[(directions.index(self) - 1) % len(Direction)]


def main(debug: bool) -> None:
    input_data = load_data(debug)

    rows = []
    for line in input_data.splitlines():
        rows.append([ch for ch in line])
    garden = np.array(rows)

    result_part1 = 0
    visited = set()
    for x, y in np.ndindex(garden.shape):
        position = Position(x, y)
        if position in visited:
            continue
        queue = deque([position])
        letter = garden[x, y]
        area = 0
        perimeter = 0
        while queue:
            position = queue.popleft()
            visited.add(position)
            area += 1
            for direction in Direction:
                n_pos = position + direction
                if not n_pos.possible(garden.shape):
                    perimeter += 1
                    continue
                n_letter = garden[n_pos.x, n_pos.y]
                if n_letter != letter:
                    perimeter += 1
                    continue
                if n_pos not in visited and n_pos not in queue:
                    queue.append(n_pos)
        result_part1 += perimeter * area

    result_part2 = 0
    visited = set()
    for x, y in np.ndindex(garden.shape):
        position = Position(x, y)
        if position in visited:
            continue
        queue = deque([position])
        letter = garden[x, y]
        area = 0
        sides = 0
        while queue:
            position = queue.popleft()
            visited.add(position)
            area += 1
            for direction in Direction:
                n_pos = position + direction
                if not n_pos.possible(garden.shape):
                    if new_side(position, direction, garden, visited):
                        sides += 1
                    continue
                n_letter = garden[n_pos.x, n_pos.y]
                if n_letter != letter:
                    if new_side(position, direction, garden, visited):
                        sides += 1
                    continue
                if n_pos not in visited and n_pos not in queue:
                    queue.append(n_pos)
        result_part2 += sides * area

    submit_or_print(result_part1, result_part2, debug)


def new_side(position, direction, garden, visited):
    dirs_to_check = [direction.next(), direction.prev()]
    letter = garden[position.x, position.y]
    for dir in dirs_to_check:
        n_pos = position + dir
        if not n_pos.possible(garden.shape):
            continue
        if n_pos not in visited:
            continue
        if garden[n_pos.x, n_pos.y] != letter:
            continue
        nn_pos = n_pos + direction
        if not nn_pos.possible(garden.shape):
            return False
        if garden[nn_pos.x, nn_pos.y] != letter:
            return False
    return True


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
