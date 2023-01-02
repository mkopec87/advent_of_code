import numpy as np

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"

ENDCODING = ".>v"


# 0 .
# 1 >
# 2 v
def print_board(board):
    for x in range(len(board)):
        print("".join([ENDCODING[b] for b in board[x]]))


def solve_part1(lines):
    shape = (len(lines), len(lines[0]))
    print(shape)
    board = np.zeros(shape, dtype=np.int8)
    for x, line in enumerate(lines):
        for y, ch in enumerate(line):
            board[x, y] = ENDCODING.index(ch)

    # print("Initial state:")
    # print_board(board)

    step = 0
    while True:
        board_before_step = board.copy()
        # moves right
        for x, y in np.ndindex(*shape):
            if board_before_step[x, y] == 1:
                neighbour = (x, (y + 1) if y + 1 < shape[1] else 0)
                if not board_before_step[neighbour]:
                    board[neighbour] = 1
                    board[x, y] = 0

        board_before_step2 = board.copy()
        # moves down
        for y, x in np.ndindex(*reversed(shape)):
            if board_before_step2[x, y] == 2:
                neighbour = (x + 1 if x + 1 < shape[0] else 0, y)
                if not board_before_step2[neighbour]:
                    board[neighbour] = 2
                    board[x, y] = 0

        step += 1

        # print(f"\nAfter {step} step(s):")
        # print_board(board)

        if (board == board_before_step).all():
            break

    return step


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    result_part1 = solve_part1(lines)
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
