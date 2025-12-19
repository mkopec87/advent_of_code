from collections import deque

import networkx as nx
from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    source_to_targets = {}
    for line in input_data.splitlines():
        s = line.split(":")
        source = s[0].strip()
        targets = set(s[1].strip().split(" "))
        source_to_targets[source] = targets

    graph = nx.DiGraph()
    for source, targets in source_to_targets.items():
        for target in targets:
            graph.add_edge(source, target)

    # result_part1 = paths_count(graph, "you", "out")

    source = "svr"
    target = "out"

    graphs = deque([graph])
    while graphs:
        g = graphs.pop()
        cut_nodes = nx.minimum_node_cut(g, source, target)
        print(g, len(cut_nodes), cut_nodes)
        if len(cut_nodes) < 10:
            g.remove_nodes_from(cut_nodes)
            graphs.extend(
                [
                    g.subgraph(c).copy()
                    for c in nx.connected_components(g.to_undirected())
                ]
            )

    #
    # inter_fft = paths_count(graph, "fft", "dac")
    # inter_dac = paths_count(graph, "dac", "fft")
    # print(inter_fft, inter_dac)
    #
    # fft = paths_count(graph, "svr", "fft")
    # dac = paths_count(graph, "svr", "dac")
    # print(fft, dac)
    #
    # fft_out = paths_count(graph, "fft", "out")
    # dac_out = paths_count(graph, "dac", "out")
    # print(fft_out, dac_out)

    result_part1 = None
    result_part2 = None

    # nx.draw_networkx(graph)
    # plt.show()

    submit_or_print(result_part1, result_part2, debug)


def paths_count(graph, start, end) -> int:
    return sum(tqdm(1 for _ in nx.all_simple_paths(graph, start, end)))


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
