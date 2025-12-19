import enum
from dataclasses import dataclass

import networkx as nx
import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, direction: "Direction"):
        return Position(self.x + direction.value.x, self.y + direction.value.y)

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def __eq__(self, other: "Position"):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def possible(self, shape):
        return 0 <= self.x < shape[0] and 0 <= self.y < shape[1]


class Direction(enum.Enum):
    NORTH = Position(-1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(1, 0)
    WEST = Position(0, -1)


@dataclass
class Node:
    position: Position
    value: int
    neighbours: set["Node"]
    reachable_nines: set["Node"]

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other: "Node"):
        return self.position == other.position

    # def __repr__(self):
    #     return f"[{self.position}]({[str(n.position) for n in self.reachable_nines]})"


def main(debug: bool) -> None:
    input_data = load_data(debug)

    rows = []
    for x, line in enumerate(input_data.splitlines()):
        rows.append(
            [
                Node(Position(x, y), -10 if ch == "." else int(ch), set(), set())
                for y, ch in enumerate(line)
            ]
        )
    matrix = np.array(rows)

    for x, y in np.ndindex(matrix.shape):
        node = matrix[x, y]
        for d in Direction:
            pos = node.position + d
            if pos.possible(matrix.shape):
                nnode = matrix[pos.x, pos.y]
                if nnode.value == node.value + 1:
                    node.neighbours.add(nnode)

    # init
    for x, y in np.ndindex(matrix.shape):
        node = matrix[x, y]
        if node.value == 9:
            node.reachable_nines = set({node})

    for i in range(9, -1, -1):
        print(i)
        for x, y in np.ndindex(matrix.shape):
            node = matrix[x, y]
            if node.value != i:
                continue
            for n in node.neighbours:
                node.reachable_nines.update(n.reachable_nines)

    print(matrix)

    # scores = np.zeros(matrix.shape)
    # for x, y in np.ndindex(matrix.shape):
    #     if matrix[x, y] == 9:
    #         scores[x, y] = 1
    # print(scores)

    result_part1 = 0
    for x, y in np.ndindex(matrix.shape):
        node = matrix[x, y]
        if node.value == 0:
            print(node)
            result_part1 += len(node.reachable_nines)

    G = nx.DiGraph()
    sources = set()
    targets = set()
    for x, y in np.ndindex(matrix.shape):
        node = matrix[x, y]
        G.add_node(node.position)
        if node.value == 9:
            targets.add(node.position)
        elif node.value == 0:
            sources.add(node.position)

    for x, y in np.ndindex(matrix.shape):
        node = matrix[x, y]
        for n in node.neighbours:
            G.add_edge(node.position, n.position)

    result_part2 = 0
    for source in sources:
        result_part2 += len(list(nx.all_simple_paths(G, source, targets)))

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
