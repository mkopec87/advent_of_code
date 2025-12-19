import itertools

import networkx as nx

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    graph = nx.Graph()
    for line in input_data.splitlines():
        spl = line.split("-")
        graph.add_edge(spl[0], spl[1])
    print(graph)
    t_nodes = {node for node in graph.nodes if node.startswith("t")}
    print(len(t_nodes), "nodes starting with t")

    # part 1
    result_part1 = solve_part1_networkx(graph, t_nodes)
    assert solve_part1_manual(graph, t_nodes) == result_part1

    # part 2
    result_part2 = solve_part2_networkx(graph)
    assert solve_part2_manual(graph) == result_part2

    submit_or_print(result_part1, result_part2, debug)


def solve_part1_networkx(graph, t_nodes):
    print(f"All cliques: {len(list(nx.find_cliques(graph)))}")
    cliques_with_t = [
        clique for clique in nx.find_cliques(graph) if set(clique) & t_nodes
    ]
    print(f"Cliques with node starting with t: {len(cliques_with_t)}")
    sets = set()
    for clique in cliques_with_t:
        for comb in itertools.combinations(clique, 3):
            if set(comb) & t_nodes:
                sets.add(tuple(sorted(comb)))
    return len(sets)


def solve_part1_manual(graph, t_nodes):
    sets = set()
    for node in sorted(t_nodes):
        edges = graph.edges(node)
        for e1 in edges:
            for e2 in edges:
                if e1 == e2:
                    continue
                if graph.has_edge(e1[1], e2[1]):
                    sets.add(tuple(sorted([node, e1[1], e2[1]])))
    return len(sets)


def solve_part2_networkx(graph):
    max_size = max([len(clique) for clique in nx.find_cliques(graph)])
    max_cliques = [
        clique for clique in nx.find_cliques(graph) if len(clique) == max_size
    ]
    assert len(max_cliques) == 1
    max_clique = max_cliques[0]
    print(max_size)
    return ",".join(sorted(max_clique))


def solve_part2_manual(graph):
    max_clique = bron_kerbosh(graph, set(), set(graph.nodes), set())
    return ",".join(sorted(max_clique))


def bron_kerbosh(graph, nodes_included_all, nodes_included_some, nodes_included_none):
    if not nodes_included_some and not nodes_included_none:
        return nodes_included_all

    max_clique = None
    max_clique_size = 0
    for node in sorted(nodes_included_some):
        neighbours = set(graph.neighbors(node))
        clique = bron_kerbosh(
            graph,
            nodes_included_all | {node},
            nodes_included_some & neighbours,
            nodes_included_none & neighbours,
        )
        if clique and len(clique) > max_clique_size:
            max_clique_size = len(clique)
            max_clique = clique

        nodes_included_some = nodes_included_some - {node}
        nodes_included_none = nodes_included_none | {node}

    return max_clique


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
