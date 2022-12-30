import itertools
from functools import reduce
from typing import Any, Iterator, List, Set, Tuple


def partition(a_list: List[Any], size: int) -> Iterator[Tuple[Any]]:
    it = iter(a_list)
    return iter(lambda: tuple(itertools.islice(it, size)), ())


def item_to_score(item: str) -> int:
    if item.lower() == item:
        score = 1 + ord(item) - ord("a")
    else:
        score = 27 + ord(item) - ord("A")
    return score


def item_from_singleton_set(items: Set[Any]) -> Any:
    assert len(items) == 1
    return list(items)[0]


def main() -> None:
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"{len(lines)} commands read")

    result = 0
    for line in lines:
        half_size = len(line) // 2
        first_set = set(line[:half_size])
        second_set = set(line[half_size:])
        common_items = first_set.intersection(second_set)
        item = item_from_singleton_set(common_items)
        score = item_to_score(item)
        result += score
    print(f"Result: {result}")

    result = 0
    for group in partition(lines, 3):
        sets = []
        for line in group:
            sets.append(set(line))
        common_items = set(reduce(set.intersection, sets))
        item = item_from_singleton_set(common_items)
        score = item_to_score(item)
        result += score
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
