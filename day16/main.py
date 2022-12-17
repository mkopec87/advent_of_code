import math

import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm


def main():
    with open("input-small.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")

    graph = nx.Graph()
    nodes_with_valves = set()
    for line in lines:
        label = line.split(" ")[1]
        flow_rate = int(line.split(";")[0].split("=")[1])
        graph.add_node(label, weight=flow_rate)
        if flow_rate:
            nodes_with_valves.add(label)
        neighbours = line.split("valve")[1].lstrip("s").strip().split(", ")
        for neighbour in neighbours:
            graph.add_edge(label, neighbour)

    draw(graph)

    distances = dict(nx.shortest_path_length(graph))

    print("Nodes with non-zero flow rate:", nodes_with_valves)
    print("Possible permutations:", math.factorial(len(nodes_with_valves)))

    def rec_find_paths(paths, current_path, nodes_to_visit, minutes_left):
        current_node = current_path[-1][0]
        target_to_cost = {
            target: distances[current_node][target] for target in nodes_to_visit
        }
        any_path_found = False
        for target, travel_time in sorted(target_to_cost.items()):
            new_minutes_left = minutes_left - travel_time - 1
            new_to_visit = set(nodes_to_visit) - {target}
            if new_minutes_left < 0:
                continue
            any_path_found = True
            flow_rate = graph.nodes[target]["weight"]
            added_score = new_minutes_left * flow_rate
            new_path = list(current_path) + [(target, added_score)]
            rec_find_paths(paths, new_path, new_to_visit, new_minutes_left)
        if not any_path_found:
            paths.append(current_path)

    paths = []
    budget = 30
    rec_find_paths(paths, [("AA", 0)], nodes_with_valves, budget)
    print(len(paths), "paths reachable with budget of", budget, "minutes")

    def score_path(p):
        return sum([s[1] for s in p])

    best_path = sorted(paths, key=lambda t: score_path(t), reverse=True)[0]
    result_part1 = score_path(best_path)

    paths1 = []
    rec_find_paths(paths1, [("AA", 0)], nodes_with_valves, 26)

    max_score = 0
    for i, path1 in tqdm(enumerate(paths1), total=len(paths1)):
        for path2 in paths1[i + 1 :]:
            node2points = {node: point for node, point in path1}
            for node, point in path2:
                node2points[node] = max(node2points.get(node, 0), point)
            max_score = max(max_score, sum(node2points.values()))
    result_part2 = max_score

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


def draw(graph):
    pos = nx.kamada_kawai_layout(graph)
    color_map = []
    weights = {}
    for node in graph:
        if node == "AA":
            color_map.append("red")
        else:
            color_map.append("grey")
        weights[node] = graph.nodes[node]["weight"]
    nx.draw(graph, node_color=color_map, pos=pos)
    nx.draw_networkx_labels(graph, pos=pos, labels=weights)
    plt.savefig("graph.png")


if __name__ == "__main__":
    main()
