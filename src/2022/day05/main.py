import dataclasses
import re
from collections import deque


@dataclasses.dataclass
class Move:
    from_stack: int
    to_stack: int
    count: int


def main():
    with open("input.txt") as f:
        lines = [line for line in f.readlines()]
    print(f"{len(lines)} lines read")

    stacks = parse_stacks(lines)
    print(len(stacks), "stacks parsed")
    for stack in stacks:
        print("\t", list(stack))

    moves = parse_moves(lines)
    print(len(moves), "moves parsed")

    # part 1
    stacks_part1 = [s.copy() for s in stacks]
    stacks_part2 = [s.copy() for s in stacks]
    for move in moves:
        for _ in range(move.count):
            item = stacks_part1[move.from_stack].pop()
            stacks_part1[move.to_stack].append(item)

        items = []
        for _ in range(move.count):
            item = stacks_part2[move.from_stack].pop()
            items.append(item)
        for item in reversed(items):
            stacks_part2[move.to_stack].append(item)

    print(f"Result part 1: {create_result(stacks_part1)}")
    print(f"Result part 2: {create_result(stacks_part2)}")


def create_result(stacks):
    return "".join([s.pop() for s in stacks])


def parse_stacks(lines):
    stack_lines = []
    for line in lines:
        if not line.strip().startswith("["):
            stack_count = int(line.strip().split(" ")[-1])
            break
        stack_lines.append(line)
    stacks = [deque() for _ in range(stack_count)]
    for line in reversed(stack_lines):
        i = 0
        while 4 * i + 2 < len(line):
            item = line[4 * i + 1 : 4 * i + 2]
            if item.strip():
                stacks[i].append(item)
            i += 1
    return stacks


def parse_moves(lines):
    moves = []
    for line in lines:
        if not line.strip().startswith("move"):
            continue
        match = re.match(r"move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)", line)
        count = int(match.group("count"))
        from_stack = int(match.group("from")) - 1
        to_stack = int(match.group("to")) - 1
        moves.append(Move(from_stack=from_stack, to_stack=to_stack, count=count))
    return moves


if __name__ == "__main__":
    main()
