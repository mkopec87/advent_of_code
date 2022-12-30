import operator
from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import pydot_layout


class Node:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.leaf = True
        self.child1 = None
        self.child2 = None
        self.operator = None

    def operation_result(self, value1: int, value2: int) -> int:
        return int(self.operator(value1, value2))

    def reverse_operation_result(
        self, value1: int, value2: int, result_value: int
    ) -> int:
        other_value = value2 if value1 is None else value1
        match self.operator:
            case operator.add:
                return result_value - other_value
            case operator.mul:
                return result_value // other_value
            case operator.sub:
                if value1 is None:
                    return result_value + other_value
                else:
                    return other_value - result_value
            case operator.truediv:
                if value1 is None:
                    return other_value * result_value
                else:
                    return other_value // result_value


def rec_calculate_value(node: Node) -> int:
    if node.leaf:
        return node.value
    child1_value = rec_calculate_value(node.child1)
    child2_value = rec_calculate_value(node.child2)
    return node.operation_result(child1_value, child2_value)


def rec_find_node(node: Node, target_node: Node) -> int:
    # 0 means not found, 1 means in child1, 2 in child 2, 3 means it is the node
    if node.leaf:
        return 3 if target_node == node else 0
    child1_result = rec_find_node(node.child1, target_node)
    if child1_result:
        return 1
    child2_result = rec_find_node(node.child2, target_node)
    if child2_result:
        return 2
    return 0


def rec_find_value(node: Node, target_node: Node, target_value: int) -> int:
    if node == target_node:
        return target_value

    target_node_child = rec_find_node(node, target_node)
    child1_value = None
    child2_value = None
    if target_node_child == 1:
        descend_child = node.child1
        child2_value = rec_calculate_value(node.child2)
    else:
        descend_child = node.child2
        child1_value = rec_calculate_value(node.child1)

    new_target = node.reverse_operation_result(child1_value, child2_value, target_value)
    return rec_find_value(descend_child, target_node, new_target)


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")

    name_to_node = parse_nodes(lines)

    root_node = name_to_node["root"]
    result_part1 = rec_calculate_value(root_node)

    human_node = name_to_node["humn"]
    if rec_find_node(root_node, human_node) == 1:
        root_child_with_human = root_node.child1
        target = rec_calculate_value(root_node.child2)
    else:
        root_child_with_human = root_node.child2
        target = rec_calculate_value(root_node.child1)
    result_part2 = rec_find_value(root_child_with_human, human_node, target)

    print()
    print("##########")
    print(
        f"Result part 1: {result_part1}"
    )  # Expected sample: 152, full: 85616733059734
    print(f"Result part 2: {result_part2}")  # Expected sample: 301, full: 3560324848168

    draw_tree(root_node)


def parse_nodes(lines: List[str]) -> Dict[str, Node]:
    name_to_node = {}
    for line in lines:
        spl = line.split(":")
        name = spl[0]
        name_to_node[name] = Node(name)
    for line in lines:
        spl = line.split(":")
        name = spl[0]
        node = name_to_node[name]
        op_str = spl[1].strip()
        if " " in op_str:
            s = op_str.split(" ")
            first_var = s[0]
            op = parse_operator(s[1])
            second_var = s[2]
            node.child1 = name_to_node[first_var]
            node.child2 = name_to_node[second_var]
            node.operator = op
            node.leaf = False
        else:
            value = int(op_str)
            node.value = value
    return name_to_node


def parse_operator(op_str: str) -> operator:
    str_to_op = {
        "+": operator.add,
        "-": operator.sub,
        "/": operator.truediv,
        "*": operator.mul,
    }
    return str_to_op[op_str]


def draw_tree(node: Node):
    operator_to_str = {
        operator.add: "+",
        operator.sub: "-",
        operator.truediv: "/",
        operator.mul: "*",
    }

    def rec_add_nodes(graph: nx.Graph, node: Node):
        graph.add_node(node.name)
        if node.leaf:
            graph.nodes[node.name]["label"] = node.value
        else:
            rec_add_nodes(graph, node.child1)
            rec_add_nodes(graph, node.child2)
            graph.add_edge(node.child1.name, node.name)
            graph.add_edge(node.child2.name, node.name)
            graph.nodes[node.name]["label"] = operator_to_str[node.operator]

    graph = nx.DiGraph()
    rec_add_nodes(graph, node)

    colors = ["red" if node in {"root", "humn"} else "grey" for node in graph]
    labels = {node: graph.nodes[node]["label"] for node in graph.nodes}

    factor = 3
    fig, ax = plt.subplots(figsize=(factor * 16, factor * 9), dpi=60)
    pos = pydot_layout(graph, prog="dot", root="root")
    nx.draw(graph, node_color=colors, pos=pos, alpha=0.5, node_size=100, arrowsize=6)
    nx.draw_networkx_labels(graph, pos=pos, labels=labels, font_size=6)
    fig.savefig("graph.png")


if __name__ == "__main__":
    main()
