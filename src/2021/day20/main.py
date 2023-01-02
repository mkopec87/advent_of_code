import numpy as np

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"
MARGIN = 3


def print_board(board: np.array):
    for row in board:
        print("".join(map(lambda b: "#" if b else ".", row)))
    print()


def enhance_pixel(x, y, board, algorithm):
    matrix = board[(x - 1) : (x + 2), (y - 1) : (y + 2)]
    bin_str = "".join([str(x) for x in matrix.ravel()])
    index = int(bin_str, 2)
    return algorithm[index] == "#"


def add_margin(board, zeros=True):
    if zeros:
        new = np.zeros(
            shape=(board.shape[0] + 2 * MARGIN, board.shape[1] + 2 * MARGIN),
            dtype=np.int8,
        )
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                new[x + MARGIN, y + MARGIN] = board[x, y]
        return new
    else:
        for _ in range(MARGIN):
            board = np.hstack(
                [
                    board[:, 0].reshape((board.shape[0], 1)),
                    board,
                    board[:, -1].reshape((board.shape[0], 1)),
                ]
            )  # right and left

            board = np.vstack(
                [
                    board[0, :].reshape((1, board.shape[1])),
                    board,
                    board[-1, :].reshape((1, board.shape[1])),
                ]
            )  # top and bottom
        return board


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    algorithm = lines[0]
    print(len(algorithm))

    lightup_coords = []
    for x, line in enumerate(lines[2:]):
        for y, ch in enumerate(line):
            if ch == "#":
                lightup_coords.append((x, y))
    print(len(lightup_coords), "light up pixels")

    xs = [x for x, y in lightup_coords]
    ys = [y for x, y in lightup_coords]
    print("X range:", min(xs), max(xs))
    print("Y range:", min(ys), max(ys))

    shape_x = max(xs) - min(xs) + 1
    shape_y = max(ys) - min(ys) + 1

    board = np.zeros(shape=(shape_x, shape_y), dtype=np.int8)
    for x, y in lightup_coords:
        board[x, y] = 1

    print("Start board with margin:")
    board = add_margin(board, zeros=True)
    print_board(board)

    for i in range(1, 51):
        board = enhance_board(algorithm, board)
        print(f"Board after step {i}")
        # print_board(board)
        board = add_margin(board, zeros=False)
        # print(f"Board after step {i} plus margin")
        # print_board(board)

    result_part1 = np.sum(board)
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


def enhance_board(algorithm, board):
    result = np.zeros(shape=board.shape, dtype=np.int8)
    for x in range(1, board.shape[0] - 1):
        for y in range(1, board.shape[1] - 1):
            result[x, y] = enhance_pixel(x, y, board, algorithm)
    for x in range(1, result.shape[0]):
        result[x, 0] = result[x, 1]
        result[x, result.shape[1] - 1] = result[x, result.shape[1] - 2]
    for y in range(result.shape[1]):
        result[0, y] = result[1, y]
        result[result.shape[0] - 1, y] = result[result.shape[0] - 2, y]

    return result


if __name__ == "__main__":
    main()
