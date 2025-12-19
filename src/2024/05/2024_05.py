import re
from collections import defaultdict

import networkx as nx

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    page_requirements = defaultdict(set)
    required = defaultdict(set)  # page to it's required predecessor pages
    updates = []
    for line in input_data.splitlines():
        if "|" in line:
            m = re.match(r"(\d+)\|(\d+)", line)
            page_requirements[int(m.group(1))].add(int(m.group(2)))
            required[int(m.group(2))].add(int(m.group(1)))

        elif line.strip():
            updates.append([int(d) for d in line.split(",")])

    for k, v in required.items():
        print(f"{k} must be after {sorted(v)}")

    result_part1 = 0
    incorrect_updates = []
    for update in updates:
        if update_valid(update, page_requirements):
            result_part1 += update[len(update) // 2]
        else:
            incorrect_updates.append(update)

    result_part2 = 0
    for update in incorrect_updates:
        update = fix_update(update, required)
        result_part2 += update[len(update) // 2]

    submit_or_print(result_part1, result_part2, debug)


def update_valid(update, page_requirements) -> bool:
    after = set(update)
    for i in range(len(update)):
        current_page = update[i]
        after.remove(current_page)
        requirements = page_requirements[current_page]
        requirements = requirements & set(update)
        if requirements - after:
            return False
    return True


def fix_update(update: list[int], prerequisites: dict[int, set[int]]) -> list[int]:
    edges = []
    for k, required in prerequisites.items():
        if k in update:
            for r in required:
                if r in update:
                    edges.append((r, k))
    return list(nx.topological_sort(nx.DiGraph(edges)))


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
