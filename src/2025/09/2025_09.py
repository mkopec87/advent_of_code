from collections import namedtuple
from itertools import combinations, product
from matplotlib.path import Path
from src.utils.data import load_data
from src.utils.submission import submit_or_print

Point = namedtuple("Point", ["x", "y"])
Segment = namedtuple("Segment", ["start", "end"])


def area(point1: Point, point2: Point) -> int:
    return (abs(point1.x - point2.x) + 1) * (abs(point1.y - point2.y) + 1)


def no_points_inside(point1, point2, points):
    x1, x2 = point1.x, point2.x
    if x1 > x2:
        x1, x2 = x2, x1
    y1, y2 = point1.y, point2.y
    if y1 > y2:
        y1, y2 = y2, y1

    for point in points:
        if x1 < point.x < x2 and y1 < point.y < y2:
            return False
    return True


def polygon(points):
    return [
        Segment(point_from, point_to)
        for point_from, point_to in zip(points, points[1:] + points[0:1])
    ]


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def intersects(lines1, lines2):
    print("checking...")
    print(lines1)
    print(lines2)

    for line1, line2 in product(lines1, lines2):
        if intersect(line1.start, line1.end, line2.start, line2.end):
            print("intersect!")
            print(line1, line2)
            return True
    print("no intersections")
    return False


def rectangle(point1, point2):
    xs = sorted([point1.x, point2.x])
    ys = sorted([point1.y, point2.y])
    points = [
        Point(xs[0], ys[0]),
        Point(xs[0], ys[1]),
        Point(xs[1], ys[1]),
        Point(xs[1], ys[0]),
    ]
    return polygon(points)


def main(debug: bool) -> None:
    input_data = load_data(debug)

    points = [Point(*map(int, line.split(","))) for line in input_data.splitlines()]
    print(len(points), "points")

    result_part1 = max(
        area(point1, point2) for point1, point2 in combinations(points, 2)
    )

    polygon = Path(points)
    print(polygon)
    result_part2 = max(
        area(point1, point2)
        for point1, point2 in combinations(points, 2)
        if not polygon.intersects_path(Path(rectangle(point1, point2)))
    )

    print(polygon.contains_point((5, 5)))

    result_part2 = None
    xs = sorted({p.x for p in points})
    ys = sorted({p.y for p in points})

    print("Xs:", min(xs), max(xs), "all", xs)
    print("Ys:", min(ys), max(ys), "all", ys)

    x_map = {x: i for i, x in enumerate(xs)}
    y_map = {y: i for i, y in enumerate(ys)}

    mapped_points = [Point(x_map[p.x], y_map[p.y]) for p in points]
    print(points)
    print(mapped_points)

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
