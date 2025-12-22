from functools import cache
from typing import AbstractSet
import networkx as nx
from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    graph = parse_input(input_data)
    print(graph)

    result_part1 = solve_part1(digraph=graph, start="you", end="out")
    result_part2 = solve_part2(
        digraph=graph, start="svr", end="out", via={"fft", "dac"}
    )

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> nx.DiGraph[str]:
    graph: nx.DiGraph[str] = nx.DiGraph()
    for line in input_data.splitlines():
        s = line.split(":")
        source = s[0].strip()
        targets = set(s[1].strip().split(" "))
        graph.add_edges_from((source, target) for target in targets)
    return graph


def solve_part1(digraph: nx.DiGraph[str], start: str, end: str) -> int:
    return sum(tqdm(1 for _ in nx.all_simple_paths(digraph, start, end)))


def solve_part2(
    digraph: nx.DiGraph[str], start: str, end: str, via: AbstractSet[str]
) -> int:
    @cache
    def path_count(start: str, end: str, visited: frozenset[str]) -> int:
        if start == end and visited == via:
            return 1
        total = 0
        for child in digraph.successors(start):
            total += path_count(
                start=child, end=end, visited=frozenset(visited | ({start} & via))
            )
        return total

    return path_count(start=start, end=end, visited=frozenset())


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
