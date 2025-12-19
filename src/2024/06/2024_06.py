import enum
from dataclasses import dataclass

import numpy as np
from tqdm import tqdm

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


class Direction(enum.Enum):
    NORTH = Position(-1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(1, 0)
    WEST = Position(0, -1)

    def next(self):
        directions = list(Direction)
        return directions[(directions.index(self) + 1) % len(Direction)]


code_to_direction = {
    "^": Direction.NORTH,
    ">": Direction.NORTH,
    "v": Direction.NORTH,
    "<": Direction.NORTH,
}


class Maze:
    def __init__(self, matrix):
        self.matrix = matrix

    def get(self, position):
        return self.matrix[position.x, position.y]

    def set(self, position, value):
        self.matrix[position.x, position.y] = value

    def __str__(self):
        s = ""
        for x in range(self.matrix.shape[0]):
            s += "".join(self.matrix[x, :]) + "\n"
        return s


class ExitType(enum.Enum):
    BORDER = 1
    CYCLE = 2


def main(debug: bool) -> None:
    input_data = load_data(debug)
    maze, position, direction = parse_input(input_data)

    # part 1
    exit_type, visited = solve(maze, position, direction)
    assert exit_type == ExitType.BORDER
    visited_positions = set(map(lambda state: state[0], visited))
    result_part1 = len(visited_positions)

    # part 2
    result_part2 = 0
    visited_positions.remove(position)
    print(len(visited_positions), "candidate obstacle positions")

    for candidate in tqdm(visited_positions):
        # place obstacle in candidate position
        assert maze.get(candidate) == "."
        maze.set(candidate, "#")

        exit_type, visited = solve(maze, position, direction)
        if exit_type == ExitType.CYCLE:
            result_part2 += 1

        # reset for next test
        maze.set(candidate, ".")

    submit_or_print(result_part1, result_part2, debug)


def solve(maze, position, direction):
    visited = set()
    while True:
        state = (position, direction)
        if state in visited:
            return ExitType.CYCLE, visited
        visited.add(state)
        next_position = position + direction
        next_value = maze.get(next_position)
        if next_value == "e":
            return ExitType.BORDER, visited
        elif next_value == "#":
            direction = direction.next()
        else:
            position = next_position


def parse_input(input_data: str) -> tuple[Maze, Position, Direction]:
    rows = []
    for line in input_data.splitlines():
        rows.append(["e"] + [ch for ch in line] + ["e"])
    rows.append(["e" for _ in range(len(rows[0]))])
    rows.insert(0, ["e" for _ in range(len(rows[0]))])
    matrix = np.array(rows)
    position = None
    direction = None
    for x, y in np.ndindex(matrix.shape):
        if matrix[x, y] in code_to_direction:
            direction = code_to_direction[matrix[x, y]]
            position = Position(x, y)
            break
    maze = Maze(matrix)
    assert position
    assert direction
    return maze, position, direction


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
