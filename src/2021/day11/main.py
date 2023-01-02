import numpy as np
from colorama import Fore, Style, init

init()


def color(x):
    if x == 0:
        return f"{Fore.RED}{x}{Style.RESET_ALL}"
    elif x == 9:
        return f"{Fore.YELLOW}{x}{Style.RESET_ALL}"
    elif x == 10:
        return "x"
    elif x > 14:
        return " "
    else:
        return str(x)


def print_board(board):
    print()
    for x in range(board.shape[0]):
        print("".join(map(color, board[x, :])))


def flash(board, x, y):
    board[x, y] = 11
    for xp in [-1, 0, 1]:
        x2 = x + xp
        for yp in [-1, 0, 1]:
            y2 = y + yp
            if board[x2, y2] < 10:
                board[x2, y2] += 1
                if board[x2, y2] == 10:
                    flash(board, x2, y2)


def step(board):
    board += 1
    print_board(board)
    for y, x in np.ndindex(board.shape):
        if board[x, y] == 10:
            flash(board, x, y)

    board[board == 11] = 0
    return board


def main():
    with open("input.txt") as f:
        lines = [[int(ch) for ch in line.strip()] for line in f.readlines()]
    print(f"{len(lines)} read")

    lines_with_border = []
    for line in lines:
        lines_with_border.append([15] + line + [15])

    b = [15 for _ in range(len(lines_with_border[0]))]
    lines_with_border.insert(0, b)
    lines_with_border.append(b)

    board = np.array(lines_with_border)
    print_board(board)

    result_part1 = 0
    step_nr = 0
    while True:
        step_nr += 1
        board = step(board)
        flashes = np.extract(board == 0, board)
        if step_nr < 100:
            result_part1 += len(flashes)
        print_board(board)

        if len(flashes) == 100:
            break

    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {step_nr}")


if __name__ == "__main__":
    main()
