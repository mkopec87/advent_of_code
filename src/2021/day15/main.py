import networkx as nx
import numpy as np


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    board_input = [[int(ch) for ch in line] for line in lines]

    board = np.array(board_input, dtype=np.int8)
    print(board)

    def bump(board):
        f = lambda x: x + 1 if x < 9 else 1
        return np.vectorize(f)(board)

    bigboard = board.copy()
    for _ in range(4):
        board = bump(board)
        bigboard = np.concatenate([bigboard, board])

    board = bigboard.copy()
    for _ in range(4):
        board = bump(board)
        bigboard = np.concatenate([bigboard, board], axis=1)

    print(bigboard.shape)

    board = bigboard

    graph = nx.Graph()
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            graph.add_node((x, y), weight=board[x, y])
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if x > 0:
                graph.add_edge((x - 1, y), (x, y))
            if y > 0:
                graph.add_edge((x, y - 1), (x, y))

    # fig, ax = plt.subplots()
    # nx.draw(graph, ax=ax)
    # plt.show()

    def node_weight(u, v, d):
        return graph.nodes[v].get("weight")

    length, _ = nx.single_source_dijkstra(
        graph,
        source=(0, 0),
        target=(board.shape[0] - 1, board.shape[1] - 1),
        weight=node_weight,
    )

    result_part1 = length
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
