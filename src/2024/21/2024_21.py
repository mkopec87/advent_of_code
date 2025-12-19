import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

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


char_to_dir = {
    "^": Direction.UP,
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
}
dir_to_char = {v: k for k, v in char_to_dir.items()}

numeric_keyboard = np.array(
    [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]
)
directional_keyboard = np.array([[None, "^", "A"], ["<", "v", ">"]])


def keyboard_to_mapping(keyboard):
    move_graph = nx.DiGraph()
    for x, y in np.ndindex(keyboard.shape):
        if keyboard[x, y] is None:
            continue
        start_pos = Position(x, y)
        for direction in list(Direction):
            end_pos = start_pos + direction
            if (
                not end_pos.valid(keyboard.shape)
                or keyboard[end_pos.x, end_pos.y] is None
            ):
                continue
            move_graph.add_edge(start_pos, end_pos, move=direction)
    mapping = defaultdict(set)
    for start_pos, d in nx.all_pairs_all_shortest_paths(move_graph):
        start_key = keyboard[start_pos.x, start_pos.y]
        for end_pos, paths in d.items():
            end_key = keyboard[end_pos.x, end_pos.y]
            if start_pos == end_pos:
                mapping[(start_key, end_key)].add("")
            else:
                for path in paths:
                    directions = []
                    for pair in zip(path, path[1:]):
                        direction = move_graph.get_edge_data(*pair)["move"]
                        directions.append(direction)
                    mapping[(start_key, end_key)].add(
                        "".join(map(dir_to_char.get, directions))
                    )
    return mapping


numeric_keyboard_mapping = keyboard_to_mapping(numeric_keyboard)
directional_keyboard_mapping = keyboard_to_mapping(directional_keyboard)


def solve(code, dir_keyboards_count):
    print(f"Processing code: {code}")
    codes = map_all_codes(code, numeric_keyboard_mapping)
    print(f"\t{len(codes)} initial codes")
    min_len = np.inf
    for c in sorted(codes):
        l = min_steps(c, dir_keyboards_count)
        min_len = min(min_len, l)
    print(f"\tGlobal min len: {min_len}")
    return min_len


def min_steps(code, levels):
    counter = code2counter("A" + code)
    for level in range(levels):
        counter = map_counter(counter, level, max_level=levels)
    return score(counter)


def score(counter):
    total = (
        0  # as we always added leading 'A' to code, we can start with 0 instead of 1
    )
    for v, c in counter.items():
        total += (len(v) + 1) * c
    return total


def code2counter(code):
    assert code[0] == "A"
    assert code[-1] == "A"
    counter = Counter()
    for m in re.finditer(r"A([^A]*)(?=A)", code):
        counter[m.group(1)] += 1
    return counter


def map_counter(counter, level, max_level):
    new_counter = Counter()
    for moves_str, count in counter.items():
        move_counter = map_moves(moves_str, level, max_level)
        for m, c in move_counter.items():
            new_counter[m] += count * c
    return new_counter


def map_moves(move_str: str, level, max_level) -> Counter:
    options = map_all_codes("A" + move_str + "A", directional_keyboard_mapping)
    best_option = None
    best_cost = np.inf
    for option in options:
        option = "A" + option
        option_cost = cost_of_option(option, level, max_level)
        if option_cost < best_cost:
            best_option = option
            best_cost = option_cost
    print("best option:", best_option, "cost:", best_cost)
    return code2counter(best_option)


@lru_cache
def cost_of_option(option: str, level: int, max_level: int):
    assert option[0] == "A"
    assert option[-1] == "A"

    if level == max_level:
        return len(option)

    option_cost = 0
    for a, b in zip(option, option[1:]):
        min_mapping_cost = np.inf
        for mapping in directional_keyboard_mapping[(a, b)]:
            mapping_cost = cost_of_option("A" + mapping + "A", level + 1, max_level)
            if mapping_cost < min_mapping_cost:
                min_mapping_cost = mapping_cost
        option_cost += min_mapping_cost
    return option_cost


def map_all_codes(code, keyboard_mapping):
    if code[0] != "A":
        code = "A" + code
    new_codes = {""}
    moves = list(zip(code, code[1:]))
    for move in moves:
        mappings = keyboard_mapping[move]
        if not mappings:
            mappings = {""}

        next_codes = set()
        for mapping in mappings:
            for code in new_codes:
                next_codes.add(code + mapping + "A")
        new_codes = next_codes
    return new_codes


def complexity(code, dir_keyboards):
    return solve(code, dir_keyboards) * int(re.sub(r"[^0-9]", "", code))


def main(debug: bool) -> None:
    input_data = load_data(debug)

    codes = input_data.splitlines()
    print(len(codes), "codes:", codes)

    # remove nonsense moves
    directional_keyboard_mapping[("A", "<")].remove("<v<")
    directional_keyboard_mapping[("<", "A")].remove(">^>")

    result_part1 = sum([complexity(code, 2) for code in codes])
    result_part2 = sum([complexity(code, 25) for code in codes])

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
