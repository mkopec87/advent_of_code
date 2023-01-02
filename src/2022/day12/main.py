from collections import deque
from dataclasses import dataclass, field
from typing import Set

import numpy as np


@dataclass
class Position:
    x: int
    y: int
    elevation: int
    neighbours: Set["Position"] = field(default_factory=set)
    visited: bool = False
    distance: int = np.inf

    def __hash__(self):
        return hash(tuple([self.x, self.y]))


def main():
    with open("input.txt") as f:
        lines = [[c for c in line.strip()] for line in f.readlines()]
    print(f"{len(lines)} read")

    elevation = np.matrix(lines)
    start_position = tuple(x.item() for x in np.where(elevation == "S"))
    end_position = tuple(x.item() for x in np.where(elevation == "E"))
    elevation[start_position] = "a"
    elevation[end_position] = "z"
    elevation = np.vectorize(lambda x: ord(x) - ord("a"))(elevation)

    graph = np.full(elevation.shape, fill_value=None, dtype=Position)
    for x, y in np.ndindex(elevation.shape):
        graph[x, y] = Position(x, y, elevation[x, y])

    for x, y in np.ndindex(graph.shape):
        position = graph[x, y]
        for x2 in range(x - 1, x + 2):
            for y2 in range(y - 1, y + 2):
                if (
                    (abs(x2 - x) + abs(y2 - y) < 2)
                    and (0 <= x2 < graph.shape[0])
                    and (0 <= y2 < graph.shape[1])
                    and ((x2, y2) != (x, y))
                ):
                    neighbour_candidate = graph[x2, y2]
                    if neighbour_candidate.elevation <= position.elevation + 1:
                        position.neighbours.add(graph[x2, y2])

    result_part1 = bfs(graph, start_position, end_position)
    print(f"Result part 1: {result_part1}")

    result_part2 = np.inf
    start_positions = np.where(elevation == 0)
    start_positions = list(zip(start_positions[0], start_positions[1]))
    for start_position in start_positions:
        result_part2 = min(result_part2, bfs(graph, start_position, end_position))
    print(f"Result part 2: {result_part2}")


def bfs(graph, start_position, end_position):
    for x, y in np.ndindex(graph.shape):
        position = graph[x, y]
        position.visited = False
        position.distance = np.inf
    start = graph[start_position]
    start.visited = True
    start.distance = 0
    stack = deque()
    stack.append(start)
    while stack:
        position = stack.popleft()
        for neighbour in position.neighbours:
            if not neighbour.visited:
                neighbour.visited = True
                neighbour.distance = position.distance + 1
                stack.append(neighbour)
    return graph[end_position].distance


if __name__ == "__main__":
    main()
