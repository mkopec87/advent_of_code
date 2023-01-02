import re
from collections import deque

import numpy as np


class Board:
    def __init__(self, id, rows):
        self.id = id
        self.board = np.empty((5, 5), dtype=np.int8)
        self.marked = np.zeros((5, 5), dtype=np.int8)
        for x, r in enumerate(rows):
            for y, c in enumerate(r):
                self.board[x, y] = c

    def __str__(self):
        return "\n" + str(self.board)

    def numbers(self):
        return set(self.board.reshape(25).tolist())

    def mark(self, number):
        for ix, iy in np.ndindex(self.marked.shape):
            if self.board[ix, iy] == number:
                self.marked[ix, iy] = 1
                if self.marked[ix, :].sum() == 5 or self.marked[:, iy].sum() == 5:
                    return True
        return False

    def sum_unmarked(self):
        s = 0
        for ix, iy in np.ndindex(self.marked.shape):
            if not self.marked[ix, iy]:
                s += self.board[ix, iy]
        return s


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    lines = deque(lines)
    numbers = [int(n) for n in lines.popleft().split(",")]
    print(f"{len(numbers)} numbers read")

    boards = []
    while len(lines) > 0:
        rows = []
        lines.popleft()  # empty line
        for _ in range(5):
            rows.append([int(n) for n in re.split(" +", lines.popleft())])
        board = Board(len(boards), rows)
        boards.append(board)
    print(f"{len(boards)} boards read")

    board = boards[0]
    print("first board", board)
    print(sorted(board.numbers()))

    def play(numbers, boards):
        for number in numbers:
            print("number: ", number)
            finished_boards = []
            for board in boards:
                done = board.mark(number)
                if done:
                    if len(boards) == 1:
                        s = board.sum_unmarked()
                        return number * s
                    else:
                        finished_boards.append(board)
            for fb in finished_boards:
                boards.remove(fb)
                print(f"\tfinished board {fb.id}")

    result = play(numbers, boards)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
