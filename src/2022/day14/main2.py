from dataclasses import dataclass

import numpy as np


@dataclass
class Line:
    start: tuple[int, ...]
    end: tuple[int, ...]


def print_cave(m):
    for x in range(m.shape[0]):
        print("")
        for y in range(m.shape[1]):
            print(m[x, y], end="")
    print()


def main():
    with open("input.txt") as f:
        rows = [line.strip() for line in f.readlines()]
    print(f"{len(rows)} rows read")

    lines = []
    for row in rows:
        points = [
            tuple([int(y) for y in x.strip().split(",")]) for x in row.split("->")
        ]
        rows = [Line(x, y) for x, y in zip(points, points[1:])]
        lines.extend(rows)
    print(len(lines), "lines parsed")
    source = (0, 500)

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 1000
    for line in lines:
        for point in [line.start, line.end]:
            x = point[1]
            y = point[0]
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
    print("x range:", min_x, max_x)
    print("y range:", min_y, max_y)
    shape_x = max_x - min_x + 3  # +1 for bottom border
    shape_y = max_y - min_y + 3  # +2 for left/right border
    print(shape_x, shape_y)

    # correct coordinates
    for line in lines:
        line.start = (line.start[1], line.start[0] - min_y + 1)
        line.end = (line.end[1], line.end[0] - min_y + 1)
    source = (source[0], source[1] - min_y + 1)

    cave = np.full((shape_x, shape_y), fill_value=".")
    cave[:, 0] = "x"
    cave[:, shape_y - 1] = "x"
    cave[shape_x - 1, :] = "#"

    cave[source] = "+"
    for line in lines:
        point = line.start
        cave[point] = "#"
        while point != line.end:
            if point[0] != line.end[0]:
                point = (point[0] + np.sign(line.end[0] - point[0]), point[1])
            if point[1] != line.end[1]:
                point = (point[0], point[1] + np.sign(line.end[1] - point[1]))
            cave[point] = "#"

    # print_cave(cave)

    steps = 0
    while True:
        steps += 1
        sand = add_sand_unit(cave, source)
        if cave[sand] == "+":
            break
        cave[sand] = "#"

    # print_cave(cave)
    result_part2 = steps

    print()
    print("##########")
    print(f"Result part 2: {result_part2}")


def add_sand_unit(cave, source):
    sand = source
    while cave[sand] != "x":
        under = (sand[0] + 1, sand[1])
        left = (sand[0] + 1, sand[1] - 1)
        right = (sand[0] + 1, sand[1] + 1)
        if cave[under] != "#":
            sand = under
        elif cave[left] != "#":
            sand = left
        elif cave[right] != "#":
            sand = right
        else:
            break
    return sand


if __name__ == "__main__":
    main()
