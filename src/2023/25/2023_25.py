import math
import re

import matplotlib.pyplot as plt
import networkx as nx

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    graph = parse_graph(input_data)
    print(graph)

    viz_path = "graph.png"
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    plt.savefig(viz_path)
    print(f"Saved graph visualization to: {viz_path}")

    edges = nx.edge_betweenness_centrality(graph)
    top3 = sorted(edges.items(), key=lambda k: k[1], reverse=True)[:3]
    for e, _ in top3:
        graph.remove_edge(*e)
    print(f"Removed 3 key edges: {[t[0] for t in top3]}")

    result_part1 = math.prod([len(c) for c in nx.connected_components(graph)])
    result_part2 = None

    submit_or_print(result_part1, result_part2, debug)


def parse_graph(input_data: str) -> nx.Graph:
    graph = nx.Graph()
    for line in input_data.strip().splitlines():
        nodes = re.findall(r"[a-z]+", line)
        for node in nodes[1:]:
            graph.add_edge(nodes[0], node)
    return graph


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
