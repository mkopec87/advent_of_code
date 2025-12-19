from collections import deque
from dataclasses import dataclass
from enum import Enum

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, direction: "Direction"):
        return Position(self.x + direction.value.x, self.y + direction.value.y)

    def __sub__(self, direction: "Direction"):
        return Position(self.x - direction.value.x, self.y - direction.value.y)

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def __eq__(self, other: "Position"):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def copy(self):
        return Position(self.x, self.y)

    def __lt__(self, other):
        return self.x < other.x


class Direction(Enum):
    UP = Position(-1, 0)
    RIGHT = Position(0, 1)
    DOWN = Position(1, 0)
    LEFT = Position(0, -1)


char_to_direction = {
    "^": Direction.UP,
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
}


def main(debug: bool) -> None:
    input_data = load_data(debug)

    s = input_data.split("\n\n", 1)
    rows = []
    for line in s[0].splitlines():
        row = [ch for ch in line]
        rows.append(row)
    warehouse = np.array(rows)
    moves = []
    for line in s[1].splitlines():
        moves.extend([char_to_direction[ch] for ch in line])

    for x, y in np.ndindex(warehouse.shape):
        if warehouse[x, y] == "@":
            robot_position = Position(x, y)
            break

    for move in moves:
        next_robot_pos = robot_position + move
        if warehouse[next_robot_pos.x, next_robot_pos.y] == ".":
            warehouse[next_robot_pos.x, next_robot_pos.y] = "@"
            warehouse[robot_position.x, robot_position.y] = "."
            robot_position = next_robot_pos
        elif warehouse[next_robot_pos.x, next_robot_pos.y] == "O":
            block_end_pos = next_robot_pos.copy()
            while warehouse[block_end_pos.x, block_end_pos.y] == "O":
                block_end_pos += move
            if warehouse[block_end_pos.x, block_end_pos.y] == ".":
                warehouse[block_end_pos.x, block_end_pos.y] = "O"
                warehouse[next_robot_pos.x, next_robot_pos.y] = "@"
                warehouse[robot_position.x, robot_position.y] = "."
                robot_position = next_robot_pos

    result_part1 = 0
    for x, y in np.ndindex(warehouse.shape):
        if warehouse[x, y] == "O":
            result_part1 += 100 * x + y

    # part 2
    mapping = {"#": "##", "O": "[]", ".": "..", "@": "@."}
    s = input_data.split("\n\n", 1)
    rows = []
    for line in s[0].splitlines():
        row = [c for ch in line for c in mapping[ch]]
        rows.append(row)
    warehouse = np.array(rows)

    for x, y in np.ndindex(warehouse.shape):
        if warehouse[x, y] == "@":
            robot_position = Position(x, y)
            break
    print(len(moves), "moves")
    print(warehouse.shape, "shape")
    print(robot_position, "robot pos")
    print_warehouse(warehouse)

    for move in moves:
        next_robot_pos = robot_position + move

        # empty space
        if warehouse[next_robot_pos.x, next_robot_pos.y] == ".":
            warehouse[next_robot_pos.x, next_robot_pos.y] = "@"
            warehouse[robot_position.x, robot_position.y] = "."
            robot_position = next_robot_pos

        # box
        elif warehouse[next_robot_pos.x, next_robot_pos.y] in {"[", "]"}:
            # left right box shift
            if move in {Direction.LEFT, Direction.RIGHT}:
                # find box block end
                block_end_pos = next_robot_pos.copy()
                while warehouse[block_end_pos.x, block_end_pos.y] in {"[", "]"}:
                    block_end_pos += move

                if warehouse[block_end_pos.x, block_end_pos.y] == ".":
                    # move all boxes in the block
                    opening = move == Direction.LEFT
                    while block_end_pos != robot_position:
                        warehouse[block_end_pos.x, block_end_pos.y] = (
                            "[" if opening else "]"
                        )
                        block_end_pos -= move
                        opening = not opening

                    # move robot
                    warehouse[next_robot_pos.x, next_robot_pos.y] = "@"
                    warehouse[robot_position.x, robot_position.y] = "."
                    robot_position = next_robot_pos

            # up down box shift
            else:
                # find all boxes - initial two positions
                box_positions = {next_robot_pos}
                if warehouse[next_robot_pos.x, next_robot_pos.y] == "[":
                    box_positions.add(next_robot_pos + Direction.RIGHT)
                else:
                    box_positions.add(next_robot_pos + Direction.LEFT)

                # bfs
                queue = deque(box_positions)
                while queue:
                    box_position = queue.popleft()
                    box_positions.add(box_position)
                    next_p = box_position + move
                    if warehouse[next_p.x, next_p.y] in {"[", "]"}:
                        for p in [
                            next_p,
                            next_p
                            + (
                                Direction.RIGHT
                                if warehouse[next_p.x, next_p.y] == "["
                                else Direction.LEFT
                            ),
                        ]:
                            if p not in box_positions:
                                queue.append(p)

                move_possible = True
                for box_position in sorted(box_positions):
                    next_p = box_position + move
                    if (
                        next_p not in box_positions
                        and warehouse[next_p.x, next_p.y] != "."
                    ):
                        move_possible = False
                        break

                if move_possible:
                    overwrites = {}
                    for box_position in sorted(
                        box_positions, reverse=move == Direction.DOWN
                    ):
                        next_p = box_position + move
                        overwrites[next_p] = warehouse[box_position.x, box_position.y]
                        overwrites[box_position] = "."
                    for pos, val in overwrites.items():
                        warehouse[pos.x, pos.y] = val

                    # move robot
                    warehouse[next_robot_pos.x, next_robot_pos.y] = "@"
                    warehouse[robot_position.x, robot_position.y] = "."
                    robot_position = next_robot_pos

        # print(f"\nMove {move}:")
        # print_warehouse(warehouse)

    result_part2 = 0
    for x, y in np.ndindex(warehouse.shape):
        if warehouse[x, y] == "[":
            result_part2 += 100 * x + y

    submit_or_print(result_part1, result_part2, debug)


def print_warehouse(warehouse):
    print()
    for x in range(warehouse.shape[0]):
        for y in range(warehouse.shape[1]):
            print(warehouse[x, y], end="")
        print()
    print()


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
