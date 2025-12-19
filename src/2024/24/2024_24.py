import dataclasses
import random
import re
from collections import deque

import graphviz
import networkx as nx

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass(frozen=True)
class Gate:
    input1: str
    input2: str
    output: str
    op: str

    def compute(self, val1, val2):
        if self.op == "AND":
            return val1 and val2
        if self.op == "OR":
            return val1 or val2
        if self.op == "XOR":
            return val1 ^ val2


def main(debug: bool) -> None:
    input_data = load_data(debug)

    s = input_data.split("\n\n")

    wire_to_value = {}
    for line in s[0].splitlines():
        m = re.match(r"([a-z0-9]+): ([0-1])", line)
        wire_to_value[m.group(1)] = m.group(2) == "1"
    print(len(wire_to_value), "initial values")

    output_to_gate = {}
    for line in s[1].splitlines():
        m = re.match(r"([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z0-9]+)", line)
        wire1 = m.group(1)
        wire2 = m.group(3)
        gate_type = m.group(2)
        wire_out = m.group(4)
        output_to_gate[wire_out] = Gate(wire1, wire2, wire_out, gate_type)
    print(len(output_to_gate), "gates")

    output_wires = set()
    for wire in set(wire_to_value.keys()) | set(output_to_gate.keys()):
        if wire.startswith("z"):
            output_wires.add(wire)
    print(len(output_wires), "output wires")

    result_part1 = solve(output_to_gate, output_wires, wire_to_value)

    graph = nx.DiGraph()
    for gate in output_to_gate.values():
        for w in [gate.input1, gate.input2, gate.output]:
            graph.add_node(w)
        graph.add_node(f"gate_{gate.output}", type="op")
        graph.add_edge(gate.input1, f"gate_{gate.output}")
        graph.add_edge(gate.input2, f"gate_{gate.output}")
        graph.add_edge(f"gate_{gate.output}", gate.output)

    print(graph)
    pos = nx.nx_agraph.graphviz_layout(graph, prog="neato")
    nx.draw(graph, pos=pos, with_labels=True)
    import matplotlib.pyplot as plt

    plt.show()

    graph = graphviz.Digraph()
    for gate in output_to_gate.values():
        for w in [gate.input1, gate.input2, gate.output]:
            if w.startswith("z"):
                graph.node(w, color="blue")
            elif w.startswith("x") or w.startswith("y"):
                graph.node(w, color="red")
            else:
                graph.node(w)
        gate_node_name = f"gate_{gate.op}_{gate.output}"
        match gate.op:
            case "AND":
                c = "lightgreen"
            case "OR":
                c = "lightblue"
            case "XOR":
                c = "lightpink"
        graph.node(gate_node_name, shape="box", style="filled", fillcolor=c)
        graph.edge(gate.input1, gate_node_name)
        graph.edge(gate.input2, gate_node_name)
        graph.edge(gate_node_name, gate.output)

    graph.view()

    tests = 1000

    random.seed(1)

    for bits in range(1, 45):
        outputs = ["z" + str(i).zfill(2) for i in range(bits)]
        for _ in range(tests):
            init_values = {}
            xs = []
            ys = []
            for b in range(bits):
                xs.append(random.choice(["0", "1"]))
                ys.append(random.choice(["0", "1"]))
            x = int("".join(reversed(xs)), base=2)
            y = int("".join(reversed(ys)), base=2)
            for i in range(bits):
                init_values[f"x{str(i).zfill(2)}"] = xs[i] == "1"
                init_values[f"y{str(i).zfill(2)}"] = ys[i] == "1"

            expected = (x + y) % (2**bits)
            solution = solve(output_to_gate, outputs, init_values)
            assert expected == solution, (
                f"{bits}, expected: {expected}, solution: {solution}"
            )

    swaps = ["z31", "dmh", "z38", "dvq", "rpv", "z11", "ctg", "rpb"]
    result_part2 = ",".join(sorted(swaps))

    submit_or_print(result_part1, result_part2, debug)


def solve(output_to_gate, output_wires, wire_to_value: dict):
    wire_to_value = {k: v for k, v in wire_to_value.items()}  # copy

    stack = deque()
    stack.extend(output_wires)
    while stack:
        wire = stack[-1]
        if wire in wire_to_value:
            stack.pop()
            continue
        gate = output_to_gate[wire]
        missing_inputs = False
        for input in [gate.input1, gate.input2]:
            if input not in wire_to_value:
                stack.append(input)
                missing_inputs = True
        if missing_inputs:
            continue
        val1 = wire_to_value[gate.input1]
        val2 = wire_to_value[gate.input2]
        out = gate.compute(val1, val2)
        wire_to_value[gate.output] = out
    binary_str = ""
    for output_wire in sorted(output_wires, reverse=True):
        binary_str += "1" if wire_to_value[output_wire] else "0"
    return int(binary_str, base=2)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
