import itertools

import networkx as nx
import numpy as np
from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print

ROCK = "#"

N = (-1, 0)
S = (1, 0)
W = (0, -1)
E = (0, 1)


def main(debug: bool) -> None:
    input_data = load_data(debug)

    grid, start, end = parse_grid(input_data)

    result_part1 = solve_part1(grid, start, end)
    result_part2 = solve_part2(grid, start, end)

    submit_or_print(result_part1, result_part2, debug)


def parse_grid(input_data: str) -> tuple[np.array, tuple[int, int], tuple[int, int]]:
    rows = []
    for line in input_data.strip().splitlines():
        rows.append(list(line))

    # borders
    rows.append(["#" for _ in rows[0]])
    rows.insert(0, ["#" for _ in rows[0]])

    grid = np.array(rows)

    # search for start and end positions
    start = 1, [y for y in range(grid.shape[1]) if grid[1, y] == "."][0]
    end = (
        grid.shape[0] - 2,
        [y for y in range(grid.shape[1]) if grid[grid.shape[0] - 2, y] == "."][0],
    )

    return grid, start, end


def solve_part1(grid: np.array, start: tuple[int, int], end: tuple[int, int]) -> int:
    graph = create_graph(grid)
    return max(map(len, nx.all_simple_paths(graph, start, end))) - 1


def solve_part2(grid: np.array, start: tuple[int, int], end: tuple[int, int]) -> int:
    graph = create_graph(grid, part2=True)

    print("Compressing graph...")
    compressed_graph = compress(graph)
    print("Initial graph:   ", graph)
    print("Compressed graph:", compressed_graph)

    viz_path = "graph.png"
    pos = nx.planar_layout(compressed_graph)
    nx.draw(compressed_graph, pos, with_labels=True)
    import matplotlib.pyplot as plt

    plt.savefig(viz_path)
    print(f"Saved compressed graph visualization to: {viz_path}")

    print("Searching for longest path in compressed graph...")
    return max(
        map(
            lambda path: nx.path_weight(compressed_graph, path, "weight"),
            nx.all_simple_paths(compressed_graph, start, end),
        )
    )


def create_graph(grid: np.array, part2: bool = False) -> nx.Graph:
    graph = nx.Graph() if part2 else nx.DiGraph()
    for x, y in np.ndindex(grid.shape):
        if grid[x, y] != ROCK:
            graph.add_node((x, y))
    for x, y in np.ndindex(grid.shape):
        p = grid[x, y]
        if p != ROCK:
            if part2:
                p = "."

            match p:
                case ">":
                    dirs = [E]
                case "<":
                    dirs = [W]
                case "^":
                    dirs = [N]
                case "v":
                    dirs = [S]
                case _:
                    dirs = [N, S, W, E]

            for d in dirs:
                n_pos = d[0] + x, d[1] + y
                n = grid[n_pos]
                if n != ROCK:
                    graph.add_edge((x, y), n_pos, weight=1)
    return graph


def compress(graph: nx.Graph) -> nx.Graph:
    crossroads = {node for node in graph.nodes if len(graph.edges(node)) != 2}

    compressed_graph = nx.Graph(graph)
    for p1, p2 in tqdm(list(itertools.combinations(crossroads, 2))):
        # simplified graph without crossroads
        graph_copy = nx.Graph(graph)
        for c in crossroads:
            if c not in {p1, p2}:
                graph_copy.remove_node(c)

        # find all paths
        for path in nx.all_simple_paths(graph_copy, p1, p2):
            if len(path) < 3:
                continue
            weight = len(path) - 1
            compressed_graph.add_edge(p1, p2, weight=weight)
            for n in path[1:-1]:
                compressed_graph.remove_node(n)
    return compressed_graph


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
