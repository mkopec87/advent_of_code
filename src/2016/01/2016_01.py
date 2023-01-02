from dataclasses import dataclass
from enum import Enum

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other: "Position"):
        return Position(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Position(self.x * other, self.y * other)

    def __rmul__(self, other: int):
        return self * other

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def __eq__(self, other: "Position"):
        return (self.x == other.x) and (self.y == other.y)


class Turn(Enum):
    RIGHT = 1
    LEFT = -1


@dataclass
class Command:
    turn: Turn
    steps: int


class Direction(Enum):
    NORTH = Position(1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(-1, 0)
    WEST = Position(0, -1)

    def turn(self, turn: Turn):
        directions = list(Direction)
        return directions[(directions.index(self) + turn.value) % len(Direction)]


def main(debug: bool) -> None:
    input_data = load_data(debug)
    commands = parse_commands(input_data)

    position = Position(0, 0)
    direction = Direction.NORTH
    for command in commands:
        direction = direction.turn(command.turn)
        position += command.steps * direction.value
    result_part1 = abs(position.x) + abs(position.y)

    position = find_first_repeated_position(commands)
    result_part2 = abs(position.x) + abs(position.y)

    submit_or_print(result_part1, result_part2, debug)


def find_first_repeated_position(commands):
    position = Position(0, 0)
    direction = Direction.NORTH
    visited = set()
    visited.add(position)
    for command in commands:
        direction = direction.turn(command.turn)
        for _ in range(command.steps):
            position += direction.value
            if position in visited:
                return position
            visited.add(position)
    return None


def parse_commands(input_data):
    commands = []
    for command in input_data.split(", "):
        turn = Turn.LEFT if command[0] == "L" else Turn.RIGHT
        steps = int(command[1:])
        commands.append(Command(turn, steps))
    return commands


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
