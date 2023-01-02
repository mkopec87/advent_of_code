from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Cave:
    name: str
    large: bool
    visits: int = 0

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"[{self.name}]"

    def __eq__(self, other):
        return self.name == other.name

    def can_visit(self, limit=1):
        if self.large:
            return True
        if self.name == "start" or self.name == "end":
            return self.visits == 0
        return self.visits < limit


def find_paths(start, end, nodes, edges, limit=1, depth=0):
    if start == end:
        yield [end.name]
        return
    if not start.can_visit(limit):
        return

    start.visits += 1
    if not start.large and start.visits == 2:
        limit = 1
    for v in sorted(edges[start.name]):
        next_node = nodes[v]
        paths = find_paths(next_node, end, nodes, edges, limit, depth + 1)
        for path in paths:
            path.insert(0, start.name)
            yield path
    start.visits -= 1


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    edges_raw = defaultdict(set)
    node_names = set()
    for line in lines:
        spl = line.split("-")
        v1_name = spl[0]
        v2_name = spl[1]
        node_names.add(v1_name)
        node_names.add(v2_name)
        edges_raw[v1_name].add(v2_name)
        edges_raw[v2_name].add(v1_name)

    print(edges_raw)
    nodes = {}
    for node_name in node_names:
        large = node_name.isupper()
        nodes[node_name] = Cave(node_name, large)
    print(len(nodes), "caves loaded")

    start = nodes["start"]
    end = nodes["end"]

    paths1 = find_paths(start, end, nodes, edges_raw, limit=1)
    result_part1 = len(list(paths1))
    paths2 = list(find_paths(start, end, nodes, edges_raw, limit=2))
    result_part2 = len(list(paths2))

    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
