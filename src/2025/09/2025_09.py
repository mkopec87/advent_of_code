from typing import NamedTuple
from itertools import combinations, product
import numpy as np
from src.utils.data import load_data
from src.utils.submission import submit_or_print


class Point(NamedTuple):
    x: int
    y: int


def main(debug: bool) -> None:
    input_data = load_data(debug)

    points = parse_input(input_data)
    print(len(points), "points")

    result_part1 = solve_part1(points)
    result_part2 = solve_part2(points)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> list[Point]:
    return [
        Point(*map(int, reversed(line.split(",")))) for line in input_data.splitlines()
    ]


def solve_part1(points: list[Point]) -> int:
    return max(area(point1, point2) for point1, point2 in combinations(points, 2))


def area(point1: Point, point2: Point) -> int:
    return (abs(point1.x - point2.x) + 1) * (abs(point1.y - point2.y) + 1)


def solve_part2(points: list[Point]) -> int:
    original_to_compressed = compress_points(points)
    compressed_points = list(original_to_compressed.values())
    matrix = fill_polygon(compressed_points)

    return max(
        [
            area(point1, point2)
            for point1, point2 in combinations(points, 2)
            if inside_polygon(point1, point2, original_to_compressed, matrix)
        ]
    )


def fill_polygon(points: list[Point]) -> np.ndarray:
    xs = sorted({p.x for p in points})
    ys = sorted({p.y for p in points})

    matrix = np.zeros((len(xs), len(ys)), dtype=bool)

    lines = list(zip(points, points[1:] + points[:1]))
    lines_up = [tuple(sorted([p1, p2])) for p1, p2 in lines if p1.y == p2.y]
    lines_right = [tuple(sorted([p1, p2])) for p1, p2 in lines if p1.x == p2.x]

    for p1, p2 in lines_up:
        for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
            matrix[x, p1.y] = True
    for p1, p2 in lines_right:
        for y in range(p1.y, p2.y + 1):
            matrix[p1.x, y] = True

    for x in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            crossings = 0
            for p1, p2 in lines_up:
                if p1.x < x <= p2.x and y >= p1.y:
                    crossings += 1
            if crossings % 2 == 1:
                matrix[x, y] = True
    return matrix


def compress_points(points: list[Point]) -> dict[Point, Point]:
    xs = sorted({p.x for p in points})
    ys = sorted({p.y for p in points})
    x_to_idx = {x: i for i, x in enumerate(xs)}
    y_to_idx = {y: i for i, y in enumerate(ys)}
    return {p: Point(x_to_idx[p.x], y_to_idx[p.y]) for p in points}


def inside_polygon(
    point1: Point,
    point2: Point,
    original_to_compressed: dict[Point, Point],
    matrix: np.ndarray,
) -> bool:
    x1, y1 = original_to_compressed[point1]
    x2, y2 = original_to_compressed[point2]
    all_filled = True
    for x, y in product(
        range(min(x1, x2), max(x1, x2) + 1), range(min(y1, y2), max(y1, y2) + 1)
    ):
        if not matrix[x, y]:
            all_filled = False
            break
    return all_filled


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
