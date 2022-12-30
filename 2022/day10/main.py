import numpy as np


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    cycles = set(range(20, 230, 40))
    print(sorted(cycles))

    ops = []
    for line in lines:
        if line == "noop":
            ops.append((1, 0))
        elif line.startswith("addx"):
            amount = int(line.split(" ")[1])
            ops.append((2, amount))

    x = 1
    xs = [x]
    for duration, change in ops:
        for _ in range(duration):
            xs.append(x)
        x += change

    result_part1 = 0
    for c, x in enumerate(xs):
        if c in cycles:
            result_part1 += x * c
    print(f"Result part 1: {result_part1}")

    # part 2
    matrix = np.zeros((6, 40))
    c2x = {c: x for c, x in enumerate(xs)}
    for c in range(6 * 40):
        x = c // 40
        y = c % 40
        v = c2x[c + 1]
        if v - 1 <= c % 40 <= v + 1:
            matrix[x, y] = 1

    print(f"Result part 2:")
    show(matrix)


def show(matrix):
    for x in range(matrix.shape[0]):
        print()
        for y in range(matrix.shape[1]):
            print("." if matrix[x, y] == 0 else "#", end="")
    print()


if __name__ == "__main__":
    main()
