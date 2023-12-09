import dataclasses
import math
import re
from typing import Dict, List, Optional, Tuple

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Node:
    name: str
    left: Optional["Node"]
    right: Optional["Node"]

    def next(self, direction: str):
        if direction == "L":
            return self.left
        elif direction == "R":
            return self.right
        else:
            raise AttributeError(f"Unknown direction {direction}")

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def is_final_part1(self):
        return self.name == "ZZZ"

    def is_final_part2(self):
        return self.name.endswith("Z")


def main(debug: bool) -> None:
    input_data = load_data(debug)

    instructions, nodes = parse_input(input_data)
    print(f"{len(instructions)} instructions")
    print(f"{len(nodes)} nodes")

    # part 1
    node = nodes["AAA"]
    instruction_index = 0
    step = 0
    while node.name != "ZZZ":
        node = node.next(instructions[instruction_index])
        instruction_index = (instruction_index + 1) % len(instructions)
        step += 1
    result_part1 = step

    # part 2
    starting_nodes = {node for node in nodes.values() if node.name[-1] == "A"}
    steps_with_final_node = set()
    for node in starting_nodes:
        current = node
        visited = set()
        instruction_index = 0
        step = 0
        while (instruction_index, current.name) not in visited:
            visited.add((instruction_index, current.name))
            if current.is_final_part2():
                steps_with_final_node.add(step)
            current = current.next(instructions[instruction_index])
            instruction_index = (instruction_index + 1) % len(instructions)
            step += 1
    result_part2 = math.lcm(*steps_with_final_node)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> Tuple[List[str], Dict[str, Node]]:
    lines = input_data.splitlines()
    instructions = list(lines[0])
    nodes = {}
    nodes_str = {}
    for line in lines[2:]:
        m = re.match(r"([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)", line)
        name = m.group(1)
        left = m.group(2)
        right = m.group(3)
        nodes[name] = Node(name, None, None)
        nodes_str[name] = (left, right)
    for name, node in nodes.items():
        node.left = nodes[nodes_str[node.name][0]]
        node.right = nodes[nodes_str[node.name][1]]
    return instructions, nodes


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
