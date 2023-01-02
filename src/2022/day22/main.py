import re
from enum import Enum

import numpy as np


def print_board(board):
    print()
    for x in range(board.shape[0]):
        print(str(x).ljust(3), end="")
        for y in range(board.shape[1]):
            print(board[x, y], end="")
        print()
    print()


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def next_position(grid, position, facing):
    row = position[0]
    col = position[1]
    match facing:
        case Direction.RIGHT:
            col += 1
            if grid[(row, col)] == " ":
                col = np.min(np.where((grid != " ")[row, :]))
            return row, col
        case Direction.LEFT:
            col -= 1
            if grid[(row, col)] == " ":
                col = np.max(np.where((grid != " ")[row, :]))
            return row, col
        case Direction.DOWN:
            row += 1
            if grid[(row, col)] == " ":
                row = np.min(np.where((grid != " ")[:, col]))
            return row, col
        case Direction.UP:
            row -= 1
            if grid[(row, col)] == " ":
                row = np.max(np.where((grid != " ")[:, col]))
            return row, col


def main():
    with open("input.txt") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    print(f"{len(lines)} lines read")

    map_lines = lines[:-2]
    path_str = lines[-1].strip()

    shape_x = len(map_lines) + 2
    shape_y = max([len(line) for line in map_lines]) + 2
    grid = np.full((shape_x, shape_y), fill_value=" ")
    for x, line in enumerate(map_lines):
        for y, ch in enumerate(line):
            grid[x + 1, y + 1] = ch

    commands = []
    for m in re.finditer(r"(\d+|R|L)", path_str):
        command_str = m.group(1)
        if command_str not in {"R", "L"}:
            commands.append(int(command_str))
        else:
            commands.append(command_str)
    print(commands)
    print(shape_x, shape_y)
    # print_board(grid)

    position = (1, np.min(np.where((grid == ".")[1, :])))
    facing = Direction.RIGHT

    print("Start State:", position, "facing:", facing)

    for command in commands:
        if command == "L":
            facing = Direction((facing.value - 1) % len(Direction))
        elif command == "R":
            facing = Direction((facing.value + 1) % len(Direction))
        else:
            for _ in range(command):
                next_pos = next_position(grid, position, facing)
                if grid[next_pos] == "#":
                    break
                position = next_pos

    print("Final state:", position, "facing:", facing)
    # expected position: 5, 7, facing: 0
    # expected sample: 6032
    result_part1 = 1000 * position[0] + 4 * position[1] + facing.value
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
