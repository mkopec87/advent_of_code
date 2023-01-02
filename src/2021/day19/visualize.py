import graphviz
import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


def main():
    graph = nx.read_graphml("overlap.graphml")

    for viz in graphviz.ENGINES:
        pos = graphviz_layout(graph, prog=viz)
        ax = plt.gca()
        options = {
            "alpha": 0.5,
            "labels": {x: str(x) for x in graph.nodes()},
            "pos": pos,
            "edge_color": "b",
            "ax": ax,
        }
        nx.draw_networkx(graph, **options)
        ax.margins(0.20)
        plt.axis("off")
        plt.savefig(f"plots/{viz}.png", format="PNG")
        plt.clf()


if __name__ == "__main__":
    main()
