from dataclasses import dataclass
from enum import Enum

import networkx as nx
import numpy as np
from networkx import NetworkXNoPath

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
    NORTH = Position(-1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(1, 0)
    WEST = Position(0, -1)

    def right(self):
        directions = list(Direction)
        return directions[(directions.index(self) + 1) % len(Direction)]

    def left(self):
        directions = list(Direction)
        return directions[(directions.index(self) + 3) % len(Direction)]


@dataclass(frozen=True)
class State:
    position: Position
    direction: Direction


def main(debug: bool) -> None:
    input_data = load_data(debug)

    rows = []
    for line in input_data.splitlines():
        row = [ch for ch in line]
        rows.append(row)
    maze = np.array(rows)

    start_direction = Direction.EAST
    for x, y in np.ndindex(maze.shape):
        if maze[x, y] == "S":
            start_position = Position(x, y)
        elif maze[x, y] == "E":
            end_position = Position(x, y)

    print(maze.shape)
    start_state = State(start_position, start_direction)
    print("start:", start_state)
    print("end:", end_position)
    print(maze.shape)

    graph = nx.DiGraph()

    # nodes
    for x, y in np.ndindex(maze.shape):
        for direction in list(Direction):
            graph.add_node(State(Position(x, y), direction))

    # edges
    for x, y in np.ndindex(maze.shape):
        if maze[x, y] == "#":
            continue
        position = Position(x, y)
        for direction in list(Direction):
            source = State(position, direction)

            # move
            new_position = position + direction
            if maze[new_position.x, new_position.y] != "#":
                target = State(new_position, direction)
                graph.add_edge(source, target, cost=1)

            # rotate
            for new_direction in [direction.right(), direction.left()]:
                target = State(position, new_direction)
                graph.add_edge(source, target, cost=1000)

    print(graph)

    end_states = [State(end_position, direction) for direction in list(Direction)]
    result_part1 = np.inf
    for end_state in end_states:
        try:
            path_cost = nx.shortest_path_length(
                graph, start_state, end_state, weight="cost"
            )
            result_part1 = min(result_part1, path_cost)
        except NetworkXNoPath:
            pass

    # part 2
    best_positions = set()
    for end_state in end_states:
        try:
            paths = nx.all_shortest_paths(graph, start_state, end_state, weight="cost")
            for path in paths:
                path_cost = nx.path_weight(graph, path, weight="cost")
                if path_cost == result_part1:
                    for s in path:
                        best_positions.add(s.position)
        except NetworkXNoPath:
            pass
    result_part2 = len(best_positions)

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
