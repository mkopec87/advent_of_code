from functools import lru_cache
from queue import PriorityQueue

import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"

COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

LETTER_TO_ROOM_ENTRANCE = {"A": 11, "B": 12, "C": 13, "D": 14}

ADDITIONAL_LINES = ["#D#C#B#A#", "#D#B#A#C#"]


def main() -> None:
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    state_part1 = parse_state(lines)
    state_part2 = parse_state(lines[:3] + ADDITIONAL_LINES + lines[3:])

    result_part1 = solve(state_part1)
    result_part2 = solve(state_part2)

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")  # expected for small input: 12521
    print(f"Result part 2: {result_part2}")  # expected for small input: 44169


def parse_state(lines: list[str]) -> str:
    state = ""
    for i, line in enumerate(lines):
        state += line.replace("#", "")
    return state


def solve(state: str) -> int:
    print(f"Solving state: {state}")

    room_size = int((len(state) - 11) / 4)
    print(f"Room size: {room_size}")

    graph = create_graph(room_size=room_size)
    draw_graph(graph, f"plots/{room_size}_rooms.png")

    state2cost = dijkstra(state, graph)
    return state2cost[final_state(room_size=room_size)]


def create_graph(room_size=2):
    graph = nx.Graph()
    for i in range(11 + room_size * 4):
        graph.add_node(i)
    for i in range(10):
        graph.add_edge(i, i + 1)
    for i in range(4):
        graph.add_edge(2 + 2 * i, 11 + i)
        for j in range(room_size - 1):
            graph.add_edge(11 + i + j * 4, 15 + i + j * 4)
    nx.set_node_attributes(graph, {i: True for i in [2, 4, 6, 8]}, name="forbidden")
    return graph


def draw_graph(graph: nx.Graph, target_path: str) -> None:
    pos = graphviz_layout(graph, prog="dot")
    ax = plt.gca()
    labels = {}
    for i in graph.nodes:
        labels[i] = str(i) + ":" + graph.nodes[i].get("value", "")
    options = {"alpha": 0.5, "labels": labels, "pos": pos, "edge_color": "b", "ax": ax}
    nx.draw_networkx(graph, **options)
    ax.margins(0.20)
    plt.axis("off")
    plt.savefig(target_path, format="PNG")
    plt.clf()


def dijkstra(start_state: str, graph: nx.Graph) -> dict[str, int]:
    state2cost = {start_state: 0}
    pq = PriorityQueue()
    pq.put((0, start_state))
    visited = set()
    while not pq.empty():
        (current_cost, current_state) = pq.get()
        visited.add(current_state)
        for neighbour_state, neighbour_cost in get_neighbours(current_state, graph):
            if neighbour_state not in visited:
                old_cost = state2cost.get(neighbour_state, float("inf"))
                new_cost = int(state2cost[current_state] + neighbour_cost)
                if new_cost < old_cost:
                    pq.put((new_cost, neighbour_state))
                    state2cost[neighbour_state] = new_cost
    print(len(visited), "nodes visited")
    return state2cost


def get_neighbours(state: str, graph: nx.Graph) -> list[tuple[str, int]]:
    result = []
    for index, ch in enumerate(state):
        if ch == ".":
            continue  # we don't move empty space :)
        if not in_final_position(state, index):
            result.extend(get_neighbours_from(state, index, graph))
    return result


@lru_cache(maxsize=None)
def in_final_position(state, index):
    if index <= 10:
        return False
    ch = state[index]
    checked_index = LETTER_TO_ROOM_ENTRANCE[ch]
    checking = False
    while checked_index < len(state):
        if checking and state[checked_index] != ch:
            return False
        if index == checked_index:
            checking = True
        checked_index += 4
    return checking


def get_neighbours_from(state: str, index: int, graph: nx.Graph):
    for target_index, cost in valid_moves(state, index, graph).items():
        new_state = list(state)
        new_state[index] = "."
        new_state[target_index] = state[index]
        new_state = "".join(new_state)
        yield new_state, cost


def valid_moves(state: str, index: int, graph: nx.Graph):
    def weight(v, u, e):
        if state[u] != ".":
            return 1e20  # don't enter nodes with something inside
        return COSTS[state[index]]

    target2cost = nx.single_source_dijkstra_path_length(
        graph, index, cutoff=1e19, weight=weight
    )

    # don't stop before the room and do an actual change
    target2cost = {
        k: v
        for k, v in target2cost.items()
        if v > 0 and not graph.nodes[k].get("forbidden", False)
    }

    # filter invalid moves
    target2cost = {
        end_index: cost
        for end_index, cost in target2cost.items()
        if valid_move(state, index, end_index)
    }

    return target2cost


@lru_cache(maxsize=None)
def valid_move(state: str, start_index: int, end_index: int):
    if start_index > 10:  # we leave the room to the corridor
        return end_index <= 10

    else:  # we leave the corridor to enter the room
        ch = state[start_index]
        checked_index = LETTER_TO_ROOM_ENTRANCE[ch]
        checking = False
        while checked_index < len(state):
            if checking and state[checked_index] != ch:
                return False
            if end_index == checked_index:
                checking = True
            checked_index += 4
        return checking


def final_state(room_size=2) -> str:
    return "." * 11 + "ABCD" * room_size


if __name__ == "__main__":
    main()
