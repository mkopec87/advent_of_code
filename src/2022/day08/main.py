import numpy as np


def main():
    # read input
    with open("input.txt") as f:
        rows = [[int(ch) for ch in l.strip()] for l in f.readlines()]
    print(f"{len(rows)} lines read")
    matrix = np.matrix(rows)
    print(f"Matrix shape: {matrix.shape}")

    # part 1
    visible = np.zeros(shape=matrix.shape, dtype=bool)
    for axis in [0, 1]:
        for ascending in [True, False]:
            mark_direction(matrix, visible, axis=axis, ascending=ascending)
    result_part1 = visible.sum()
    print(f"Result part 1: {result_part1}")

    scores = np.zeros(shape=matrix.shape, dtype=int)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            scores[i, j] = score_tree(i, j, matrix)
    result_part2 = scores.max()
    print(f"Result part 2: {result_part2}")


def mark_direction(matrix, visible, axis, ascending):
    for x in range(matrix.shape[axis]):
        max_height = -1
        other_shape = matrix.shape[int(not axis)]
        r = range(other_shape) if ascending else range(other_shape - 1, -1, -1)
        for y in r:
            current_tree = matrix[x, y] if axis == 0 else matrix[y, x]
            if current_tree > max_height:
                if axis == 0:
                    visible[x, y] = True
                else:
                    visible[y, x] = True
            max_height = max(current_tree, max_height)


def score_tree(i, j, matrix):
    total = 1
    for axis in [0, 1]:
        for ascending in [True, False]:
            total *= score_direction(i, j, matrix, axis=axis, ascending=ascending)

    return total


def score_direction(i, j, matrix, axis: int, ascending: bool):
    current_tree = matrix[i, j]
    score = 0

    k = i if axis == 0 else j
    k += 1 if ascending else -1
    while 0 <= k < matrix.shape[axis]:
        next_tree = matrix[k, j] if axis == 0 else matrix[i, k]
        score += 1
        if next_tree >= current_tree:
            break
        k += 1 if ascending else -1

    return score


if __name__ == "__main__":
    main()
