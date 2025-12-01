from enum import Enum
from typing import NamedTuple

from src.utils.data import load_data
from src.utils.submission import submit_or_print


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"

    def __repr__(self):
        return self.value


class Rotation(NamedTuple):
    direction: Direction
    distance: int

    def __repr__(self):
        return f"{self.direction!r}{self.distance}"


def main(debug: bool) -> None:
    input_data = load_data(debug)
    rotations = parse_input(input_data)

    limit = 100
    initial_position = 50

    result_part1 = solve(initial_position, limit, rotations)
    result_part2 = solve(initial_position, limit, rotations, part2=True)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> list[Rotation]:
    return [
        Rotation(direction=Direction(line[0]), distance=int(line[1:]))
        for line in input_data.splitlines()
    ]


def solve(
    init_pos: int, limit: int, commands: list[Rotation], part2: bool = False
) -> int:
    print()
    result = 0

    current_pos = init_pos
    for direction, distance in commands:
        start_pos = current_pos

        # remove all full rotations
        quotient, distance = divmod(distance, limit)

        # each full rotation goes once through zero
        if part2:
            result += quotient

        # rotate
        current_pos += (1 if direction == Direction.RIGHT else -1) * distance
        # go back to required range [0, limit)
        quotient, current_pos = divmod(current_pos, limit)

        # count going through zero if not starting or ending with it
        if all([part2, quotient, start_pos != 0, current_pos != 0]):
            result += 1

        # count ending rotation at zero
        if current_pos == 0:
            result += 1

    return result


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
