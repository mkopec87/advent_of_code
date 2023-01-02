import numpy as np


class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.end_y = end_y
        self.end_x = end_x
        self.start_y = start_y
        self.start_x = start_x

    def horizontal(self) -> bool:
        return self.start_x == self.end_x

    def vertical(self) -> bool:
        return self.start_y == self.end_y

    def diagonal(self) -> bool:
        return not (self.horizontal() or self.vertical())

    def __str__(self) -> str:
        return f"({self.start_x},{self.start_y}) -> ({self.end_x},{self.end_y})"


def main():
    with open("input.txt") as f:
        lines_str = [line.strip() for line in f.readlines()]
    print(f"{len(lines_str)} lines read")

    lines = []
    xs = set()
    ys = set()
    for line in lines_str:
        spl = line.split(" ")
        start = spl[0]
        end = spl[2]
        spl1 = start.split(",")
        start_x = int(spl1[0])
        start_y = int(spl1[1])
        spl2 = end.split(",")
        end_x = int(spl2[0])
        end_y = int(spl2[1])
        xs.add(start_x)
        ys.add(start_y)
        xs.add(end_x)
        ys.add(end_y)
        if start_x > end_x:
            start_x, end_x = end_x, start_x
            start_y, end_y = end_y, start_y
        lines.append(Line(start_x, start_y, end_x, end_y))

    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)
    print("Max:", max_x, max_y)
    print("Min:", min_x, min_y)

    # lines = [a for a in filter(lambda x: x.horizontal() or x.vertical(), lines)]
    print(f"Only horizontal or vertical: {len(lines)}")

    board = np.zeros((max_x + 1, max_y + 1), dtype=np.int8)

    for line in lines:
        print("line", line)
        if line.diagonal():
            step = 1 if line.start_y < line.end_y else -1
            y = line.start_y
            for x in range(line.start_x, line.end_x + 1):
                board[x, y] = board[x, y] + 1
                y = y + step
        else:
            for x in range(line.start_x, line.end_x + 1):
                step = 1 if line.start_y < line.end_y else -1
                for y in range(line.start_y, line.end_y + step, step):
                    print("\t", x, y)
                    board[x, y] = board[x, y] + 1

    result = len(np.extract(board > 1, board))
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
