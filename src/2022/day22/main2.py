import re
from dataclasses import dataclass
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np


class Value(Enum):
    EMPTY = "."
    WALL = "#"


class Rotation(Enum):
    LEFT = (2, 1)
    RIGHT = (1, 2)
    UP = (2, 0)
    DOWN = (0, 2)

    def opposite(self):
        return Rotation(tuple(reversed(self.value)))


@dataclass
class Point:
    map_x: int
    map_y: int
    value: Value


def print_grid(grid: np.matrix) -> None:
    print()
    for x in range(grid.shape[0]):
        print(str(x).ljust(3), end="")
        for y in range(grid.shape[1]):
            if grid[x, y]:
                print(grid[x, y].value.value, end="")
            else:
                print(" ", end="")
        print()
    print()


def plot_cube(cube: np.matrix):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # align visuals to first dim being top->down
    # second dim being left -> right
    # third dim being front -> back
    cube = np.swapaxes(cube, 0, 2)
    cube = np.swapaxes(cube, 0, 1)
    cube = np.flip(cube, axis=2)

    voxels = np.empty(cube.shape, dtype=bool)
    colors = np.full(cube.shape, dtype="str", fill_value="grey")
    for index, point in np.ndenumerate(cube):
        if point:
            colors[index] = "red" if point.value == Value.WALL else "yellow"
        voxels[index] = True
    ax.voxels(voxels, facecolors=colors, edgecolor="k")
    plt.savefig("plot.png")


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def next_position(position, facing):
    row = position[0]
    col = position[1]
    match facing:
        case Direction.RIGHT:
            return row, col + 1
        case Direction.LEFT:
            return row, col - 1
        case Direction.DOWN:
            return row + 1, col
        case Direction.UP:
            return row - 1, col


def pos_after_rot(pos, cube_size, rotation: Rotation):
    match rotation:
        case Rotation.RIGHT:
            return pos[0], cube_size + 1
        case Rotation.LEFT:
            return pos[0], 0
        case Rotation.UP:
            return 0, pos[1]
        case Rotation.DOWN:
            return cube_size + 1, pos[1]


def main():
    input_file = "input.txt"
    grid, commands = parse_input(input_file)

    # print_grid(grid)

    cube_size = max(grid.shape) // 4
    faces_grid = np.full(tuple(map(lambda x: x // cube_size, grid.shape)), fill_value=0)
    face_number = 1
    for x in range(faces_grid.shape[0]):
        for y in range(faces_grid.shape[1]):
            if grid[x * cube_size, y * cube_size]:
                faces_grid[x, y] = face_number
                face_number += 1
    print(faces_grid)

    cube = np.empty(
        tuple(cube_size + 2 for _ in range(3)), dtype=Point
    )  # add +2 for edges

    # TODO: DFS this shit using neighbourhood info in faces_grid matrix
    sequence = [
        ([Rotation.UP], 3),
        ([Rotation.RIGHT], 3),
        ([Rotation.RIGHT], 2),
        ([Rotation.LEFT, Rotation.LEFT, Rotation.UP], 5),
        ([Rotation.LEFT], 6),
        ([Rotation.RIGHT, Rotation.DOWN, Rotation.DOWN], 1),
    ]

    sequence = [
        ([Rotation.LEFT], 2),
        ([Rotation.RIGHT, Rotation.UP], 3),
        ([Rotation.UP], 5),
        ([Rotation.RIGHT], 4),
        ([Rotation.UP], 6),
        ([Rotation.DOWN, Rotation.LEFT, Rotation.DOWN, Rotation.DOWN], 1),
    ]

    for rotations, face_nr in sequence:
        for rotation in rotations:
            cube = np.rot90(cube, axes=rotation.value)
        face_index = tuple(x[0] for x in np.where(faces_grid == face_nr))
        grid_x = face_index[0] * cube_size
        grid_y = face_index[1] * cube_size
        grid_slice = grid[grid_x : grid_x + cube_size, grid_y : grid_y + cube_size]
        for x in range(cube_size):
            for y in range(cube_size):
                cube[x + 1, y + 1, 0] = grid_slice[x, y]

    position = (
        1,
        min(
            [
                y
                for y, val in enumerate(cube[1, :, 0])
                if val is not None and val.value == Value.EMPTY
            ]
        ),
    )
    facing = Direction.RIGHT

    plot_cube(cube)
    print("Start State:", position, "facing:", facing)

    for command in commands:
        if command == "L":
            facing = Direction((facing.value - 1) % len(Direction))
        elif command == "R":
            facing = Direction((facing.value + 1) % len(Direction))
        else:
            for _ in range(command):
                next_pos = next_position(position, facing)

                rotated = False
                if cube[next_pos + (0,)] is None:  # next pos at edge
                    rotation = Rotation[facing.name].opposite()
                    cube = np.rot90(cube, axes=rotation.value)
                    next_pos = pos_after_rot(next_pos, cube_size, rotation)
                    next_pos = next_position(next_pos, facing)
                    rotated = True

                if cube[next_pos + (0,)].value == Value.WALL:
                    if rotated:  # reverse rotation
                        cube = np.rot90(cube, axes=Rotation[facing.name].value)
                    break
                else:
                    position = next_pos

        # print(command, position, facing)

    print("Final state:", position, "facing:", facing)
    # expected position: 5, 7, facing: 0
    # expected sample: ?
    point = cube[position + (0,)]
    print(point)
    result_part1 = 1000 * point.map_x + 4 * point.map_y + facing.value
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


def parse_input(input_file):
    with open(input_file) as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    grid_lines = lines[:-2]
    path_str = lines[-1].strip()
    grid = parse_grid(grid_lines)
    commands = parse_commands(path_str)
    return grid, commands


def parse_grid(map_lines):
    shape_x = len(map_lines)
    shape_y = max([len(line) for line in map_lines])
    grid = np.full((shape_x, shape_y), fill_value=None)
    for x, line in enumerate(map_lines):
        for y, ch in enumerate(line):
            if ch not in {v.value for v in Value}:
                continue
            grid[x, y] = Point(x + 1, y + 1, Value(ch))
    return grid


def parse_commands(path_str):
    commands = []
    for m in re.finditer(r"(\d+|R|L)", path_str):
        command_str = m.group(1)
        if command_str not in {"R", "L"}:
            commands.append(int(command_str))
        else:
            commands.append(command_str)
    return commands


if __name__ == "__main__":
    main()
