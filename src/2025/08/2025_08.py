import math
from itertools import combinations
from operator import itemgetter
from typing import NamedTuple

from scipy._lib._disjoint_set import DisjointSet

from src.utils.data import load_data
from src.utils.submission import submit_or_print


class Box(NamedTuple):
    x: int
    y: int
    z: int

    def distance(self, other):
        return math.dist([self.x, self.y, self.z], [other.x, other.y, other.z])


def main(debug: bool) -> None:
    input_data = load_data(debug)

    boxes = [Box(*map(int, line.split(","))) for line in input_data.splitlines()]
    print(len(boxes), "boxes")

    pair_to_distance = {}
    for box1, box2 in combinations(boxes, 2):
        pair_to_distance[(box1, box2)] = box1.distance(box2)
    circuits = DisjointSet(elements=boxes)
    for (box1, box2), distance in sorted(pair_to_distance.items(), key=itemgetter(1))[
        :1000
    ]:
        circuits.merge(box1, box2)
    result_part1 = math.prod(
        sorted([len(s) for s in circuits.subsets()], reverse=True)[:3]
    )

    circuits = DisjointSet(elements=boxes)
    for (box1, box2), distance in sorted(pair_to_distance.items(), key=itemgetter(1)):
        circuits.merge(box1, box2)
        if circuits.n_subsets == 1:
            result_part2 = box1.x * box2.x
            break

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
