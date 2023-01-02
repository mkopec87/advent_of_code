import numpy as np


def print_board(board):
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            print("#" if board[x, y] else ".", end="")
        print()


def fold_y(board, val, axis="y"):
    if axis == "y":
        new_shape = (val, board.shape[1])
    else:
        new_shape = (board.shape[0], val)

    new_board = np.zeros(new_shape, dtype=np.int8)
    for y in range(new_board.shape[0]):
        for x in range(new_board.shape[1]):
            new_board[y, x] = board[y, x]

            if axis == "y" and board[board.shape[0] - y - 1, x]:
                new_board[y, x] = 1
            if axis == "x" and board[y, board.shape[1] - x - 1]:
                new_board[y, x] = 1

    return new_board


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    empty_line_index = lines.index("")

    dots = []
    for line in lines[:empty_line_index]:
        spl = line.split(",")
        dots.append((int(spl[0]), int(spl[1])))
    xs = [d[0] for d in dots]
    ys = [d[1] for d in dots]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    print(min_x, max_x)
    print(min_y, max_y)
    board = np.zeros((max_y + 1, max_x + 1), dtype=np.int8)
    for dot in dots:
        board[dot[1], dot[0]] = 1

    print_board(board)

    dots_sum_after_first_fold = None
    for fold in lines[empty_line_index + 1 :]:
        print(fold)
        spl = fold.split(" ")[2].split("=")
        axis = spl[0]
        val = int(spl[1])

        board = fold_y(board, val, axis)
        print_board(board)

        if dots_sum_after_first_fold is None:
            dots_sum_after_first_fold = np.sum(board)

    result_part1 = dots_sum_after_first_fold
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
