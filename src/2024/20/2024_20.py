from collections import Counter
from dataclasses import dataclass
from enum import Enum

import networkx as nx
import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def __add__(self, direction: "Direction"):
        if isinstance(direction, Direction):
            return Position(self.x + direction.value.x, self.y + direction.value.y)
        else:
            return Position(self.x + direction.x, self.y + direction.y)

    def valid(self, shape):
        return (0 <= self.x < shape[0]) and (0 <= self.y < shape[1])

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Direction(Enum):
    UP = Position(-1, 0)
    RIGHT = Position(0, 1)
    DOWN = Position(1, 0)
    LEFT = Position(0, -1)

    def __mul__(self, other: int):
        return Position(self.value.x * other, self.value.y * other)

    def __rmul__(self, other: int):
        return self * other


@dataclass(frozen=True)
class State:
    pos: Position
    cheated: bool


def main(debug: bool) -> None:
    input_data = load_data(debug)

    rows = []
    for line in input_data.splitlines():
        row = [ch for ch in line]
        rows.append(row)

    racetrack = np.array(rows)
    for x, y in np.ndindex(racetrack.shape):
        if racetrack[x, y] == "S":
            start_pos = Position(x, y)
        elif racetrack[x, y] == "E":
            end_pos = Position(x, y)

    print(racetrack.shape)
    print(start_pos)
    print(end_pos)

    # find race path positions
    graph = nx.DiGraph()
    for x, y in np.ndindex(racetrack.shape):
        if racetrack[x, y] == "#":
            continue
        source_pos = Position(x, y)
        for direction in list(Direction):
            target_pos = source_pos + direction
            if (
                not target_pos.valid(racetrack.shape)
                or racetrack[target_pos.x, target_pos.y] == "#"
            ):
                continue
            graph.add_edge(source_pos, target_pos)
    pos_to_time = {
        pos: time
        for time, pos in enumerate(nx.shortest_path(graph, start_pos, end_pos))
    }

    #
    savings = Counter()
    for source_pos, source_time in pos_to_time.items():
        for direction in list(Direction):
            target_pos = source_pos + 2 * direction
            if target_pos not in pos_to_time.keys():
                continue
            target_time = pos_to_time[target_pos]
            saved_time = source_time - target_time - 2
            if saved_time > 0:
                savings[saved_time] += 1
    result_part1 = sum([c for k, c in savings.items() if k >= 100])

    print(len(pos_to_time), "is racetrack length")
    savings = Counter()
    for source_pos, source_time in pos_to_time.items():
        for target_pos, target_time in pos_to_time.items():
            distance = source_pos.distance(target_pos)
            if distance > 20:
                continue
            saved_time = source_time - target_time - distance
            if saved_time < 100:
                continue
            savings[saved_time] += 1

    print(savings)
    result_part2 = sum([c for k, c in savings.items() if k >= 100])

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
