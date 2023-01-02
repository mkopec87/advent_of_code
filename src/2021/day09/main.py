from collections import defaultdict

import numpy as np


def find_flow(arr, x, y):
    for xp in [-1, 1]:
        if arr[x + xp, y] < arr[x, y]:
            return x + xp, y
    for yp in [-1, 1]:
        if arr[x, y + yp] < arr[x, y]:
            return x, y + yp
    return x, y


def main():
    with open("input.txt") as f:
        lines = [[int(ch) for ch in line.strip()] for line in f.readlines()]
    print(f"{len(lines)} read")

    width = len(lines[0])

    border = [10 for _ in range(width + 2)]

    board = [border]
    for line in lines:
        line.insert(0, 10)
        line.append(10)
        board.append(line)
    board.append(border)

    arr = np.array(board)
    print(arr)

    flows = {}
    for x in range(1, arr.shape[0] - 1):
        for y in range(1, arr.shape[1] - 1):
            if arr[x, y] == 9:
                continue
            flow_point = find_flow(arr, x, y)
            flows[(x, y)] = flow_point

    root2members = defaultdict(set)
    for k, v in flows.items():
        prev_stop = k
        next_stop = v
        while next_stop != prev_stop:
            prev_stop = next_stop
            next_stop = flows[next_stop]
        print(k, "->", v, "~~>", next_stop)
        root2members[next_stop].add(k)

    lengths = sorted([len(v) for v in root2members.values()], reverse=True)
    result = 1
    for i in range(3):
        result *= lengths[i]

    print(f"Result: {result}")


if __name__ == "__main__":
    main()
