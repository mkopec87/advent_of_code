from dataclasses import dataclass
from enum import Enum
from typing import List

import networkx as nx
import numpy as np
from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def __add__(self, direction: "Direction"):
        return Position(self.x + direction.value.x, self.y + direction.value.y)

    def valid(self, shape):
        return (0 <= self.x < shape[0]) and (0 <= self.y < shape[1])


class Direction(Enum):
    UP = Position(-1, 0)
    RIGHT = Position(0, 1)
    DOWN = Position(1, 0)
    LEFT = Position(0, -1)


def main(debug: bool) -> None:
    input_data = load_data(debug)

    byte_positions = parse_input(input_data)
    print(f"{len(byte_positions)} byte positions")

    shape = 71, 71
    start_pos = Position(0, 0)
    end_pos = Position(shape[0] - 1, shape[1] - 1)
    print(f"Space shape: {shape}")
    print(f"Start position: {start_pos}")
    print(f"End position: {end_pos}")

    # part 1
    used_byte_positions = set(byte_positions[:1024])

    graph = nx.DiGraph()
    for y, x in np.ndindex(shape):
        node = Position(x, y)
        graph.add_node(node)
        for d in list(Direction):
            neighbouring_pos = node + d
            if (
                neighbouring_pos.valid(shape)
                and neighbouring_pos not in used_byte_positions
            ):
                graph.add_edge(node, neighbouring_pos)
    print(f"Part 1 graph: {graph}")

    result_part1 = nx.shortest_path_length(graph, start_pos, end_pos)

    # part 2
    graph = nx.DiGraph()
    for y, x in np.ndindex(shape):
        node = Position(x, y)
        graph.add_node(node)
        for d in list(Direction):
            neighbouring_pos = node + d
            if neighbouring_pos.valid(shape):
                graph.add_edge(node, neighbouring_pos)
    print(f"Part 2 graph: {graph}")

    for byte in tqdm(byte_positions):
        # add byte to graph
        for d in list(Direction):
            neighbouring_pos = byte + d
            if neighbouring_pos.valid(shape):
                if graph.has_edge(byte, neighbouring_pos):
                    graph.remove_edge(byte, neighbouring_pos)
                if graph.has_edge(neighbouring_pos, byte):
                    graph.remove_edge(neighbouring_pos, byte)
        # check if it disabled access
        if not nx.has_path(graph, start_pos, end_pos):
            break

    result_part2 = f"{byte.x},{byte.y}"

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> List[Position]:
    byte_positions = []
    for line in input_data.splitlines():
        spl = list(map(int, line.split(",")))
        byte_positions.append(Position(spl[0], spl[1]))
    return byte_positions


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
