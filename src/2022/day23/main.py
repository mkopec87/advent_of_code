from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum

import numpy as np


@dataclass
class Elf:
    position: tuple[int, ...]

    def next_pos(self, grid, moves):
        if self.stays(grid):
            return None
        for move in moves:
            if self.valid_move(move.checks, grid):
                return self.pos_after_move(move.direction)
        return None

    def valid_move(self, checks, grid):
        return all(self.check_direction(d, grid) for d in checks)

    def check_direction(self, d, grid):
        next_x, next_y = self.pos_after_move(d)
        if next_x < 0 or next_x >= grid.shape[0]:
            return True
        if next_y < 0 or next_y >= grid.shape[1]:
            return True
        return grid[next_x, next_y] == "."

    def pos_after_move(self, direction):
        return tuple(self.position[i] + direction.value[i] for i in range(2))

    def __hash__(self):
        return hash(self.position)

    def stays(self, grid):
        return self.valid_move({d for d in Direction}, grid)


def calc_grid(elves):
    xs = [elf.position[0] for elf in elves]
    ys = [elf.position[1] for elf in elves]
    min_x = min(xs)
    min_y = min(ys)
    xs = [x - min_x for x in xs]
    ys = [y - min_y for y in ys]
    grid = np.full((max(xs) + 1, max(ys) + 1), fill_value=".")
    for i in range(len(xs)):
        pos = xs[i], ys[i]
        grid[pos] = "#"
        elves[i].position = xs[i], ys[i]
    return grid


def print_grid(grid):
    print()
    for x in range(grid.shape[0]):
        print(str(x).ljust(3), end="")
        for y in range(grid.shape[1]):
            print(grid[x, y], end="")
        print()
    print()


class Direction(Enum):
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1)
    W = (0, -1)
    NW = (-1, -1)


@dataclass
class Move:
    checks: set[Direction]
    direction: Direction


def main():
    with open("input-small.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")

    elves = []
    for x, line in enumerate(lines):
        for y, ch in enumerate(line):
            if ch == "#":
                elves.append(Elf((x, y)))

    moves = deque(
        [
            Move({Direction.N, Direction.NE, Direction.NW}, Direction.N),
            Move({Direction.S, Direction.SE, Direction.SW}, Direction.S),
            Move({Direction.W, Direction.NW, Direction.SW}, Direction.W),
            Move({Direction.E, Direction.NE, Direction.SE}, Direction.E),
        ]
    )

    print(len(elves), "elves")
    print(len(moves), "moves")

    grid = calc_grid(elves)

    round_part1 = 10

    round_nr = 1
    while True:
        new_pos_to_elves = defaultdict(set)
        for elf in elves:
            elf_next_pos = elf.next_pos(grid, moves)
            if elf_next_pos:
                new_pos_to_elves[elf_next_pos].add(elf)

        change = False
        for new_pos, elves_for_pos in new_pos_to_elves.items():
            if len(elves_for_pos) > 1:
                continue
            else:
                for elf in elves_for_pos:
                    elf.position = new_pos
                change = True

        grid = calc_grid(elves)
        moves.append(moves.popleft())

        if not change:
            break
        if round_nr == round_part1:
            result_part1 = np.sum(grid == ".")

        round_nr += 1

    result_part2 = round_nr

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")

    # Expected sample:
    # Result part 1: 110
    # Result part 2: 20

    # Expected full:
    # Result part 1: 4056
    # Result part 2: 999


if __name__ == "__main__":
    main()
