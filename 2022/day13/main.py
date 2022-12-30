import math
from dataclasses import dataclass
from typing import List, Union

import numpy as np


class Packet:
    def __init__(self, line, divider=False):
        self.data = self.parse(line)
        self.divider = divider

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.compare(self.data, other.data) < 0

    def __le__(self, other):
        return self.compare(self.data, other.data) <= 0

    @staticmethod
    def compare(left: Union[int, List], right: Union[int, List]) -> int:
        # return -1 if left < right
        # return 0 in left = right
        # return 1 if left > right

        if isinstance(left, int) and isinstance(right, int):
            return np.sign(left - right)
        elif isinstance(left, List) and isinstance(right, List):
            for index, elem in enumerate(left):
                if index >= len(right):
                    return 1
                other_elem = right[index]
                c = Packet.compare(elem, other_elem)
                if c != 0:
                    return c
            if len(left) == len(right):
                return 0
            else:
                return -1
        elif isinstance(left, int):
            left = [left]
            return Packet.compare(left, right)
        else:
            right = [right]
            return Packet.compare(left, right)

    @staticmethod
    def parse(line: str):
        if line.startswith("["):
            line = line[1:-1]
            if not line:
                return []

            split_ranges = []
            depth = 0
            prev_split_index = 0
            for i, ch in enumerate(line):
                if depth == 0 and ch == ",":
                    split_ranges.append((prev_split_index, i))
                    prev_split_index = i + 1
                elif ch == "[":
                    depth += 1
                elif ch == "]":
                    depth -= 1
            if prev_split_index:
                split_ranges.append((prev_split_index, len(line)))
                return [
                    Packet.parse(line[split_range[0] : split_range[1]])
                    for split_range in split_ranges
                ]
            else:
                return [Packet.parse(line)]
        else:
            return int(line)


@dataclass
class Pair:
    index: int
    first: Packet
    second: Packet

    def in_correct_order(self):
        return self.first <= self.second

    def score(self):
        return self.index if self.in_correct_order() else 0


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")

    # part 1
    pairs = []
    for pair_index in range(len(lines) // 3):
        pair_start = pair_index * 3
        first = Packet(lines[pair_start])
        second = Packet(lines[pair_start + 1])
        pair = Pair(pair_index + 1, first, second)
        pairs.append(pair)
    result_part1 = sum([pair.score() for pair in pairs])

    # part 2
    packets = []
    for line in lines:
        if line:
            packets.append(Packet(line))
    packets.append(Packet("[[2]]", divider=True))
    packets.append(Packet("[[6]]", divider=True))
    packets = sorted(packets)
    result_part2 = math.prod([n + 1 for n, p in enumerate(packets) if p.divider])

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
