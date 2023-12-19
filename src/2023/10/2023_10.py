import enum
from typing import Set, Tuple

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print

GROUND_CH = "."

N = -1, 0
S = 1, 0
W = 0, -1
E = 0, 1


class PipeType(enum.Enum):
    NS = "|"
    EW = "-"
    NE = "L"
    NW = "J"
    SW = "7"
    SE = "F"
    START = "S"
    GROUND = GROUND_CH
    GLUE_NONBLOCKING = "s"
    GLUE_BLOCKING = "b"

    def blocking(self):
        return self not in {PipeType.GROUND, PipeType.GLUE_NONBLOCKING}


class Pipe:
    def __init__(self, ch: str):
        self.type = PipeType(ch)
        self.neighbours = set()
        self.visited = False

    def connected_positions(self) -> Set[Tuple[int, int]]:
        match self.type:
            case PipeType.NS:
                return {N, S}
            case PipeType.EW:
                return {E, W}
            case PipeType.NE:
                return {N, E}
            case PipeType.NW:
                return {N, W}
            case PipeType.SW:
                return {S, W}
            case PipeType.SE:
                return {S, E}
            case PipeType.START:
                return {N, S, E, W}
            case PipeType.GROUND:
                return set()

    def add_neighbour(self, pipe: "Pipe") -> None:
        self.neighbours.add(pipe)

    def is_glue(self):
        return self.type in {PipeType.GLUE_NONBLOCKING, PipeType.GLUE_BLOCKING}


def main(debug: bool) -> None:
    input_data = load_data(debug)

    grid = parse_grid(input_data)

    result_part1 = solve_part1(grid)
    result_part2 = solve_part2(grid)

    submit_or_print(result_part1, result_part2, debug)


def parse_grid(input_data: str) -> np.array:
    rows = []
    for line in input_data.splitlines():
        row = []
        for ch in line:
            row.append(Pipe(ch))
        row = [Pipe(GROUND_CH)] + row + [Pipe(GROUND_CH)]
        rows.append(row)
    rows.insert(0, [Pipe(GROUND_CH) for _ in range(len(rows[0]))])
    rows.append([Pipe(GROUND_CH) for _ in range(len(rows[0]))])
    grid = np.array(rows)

    for x, y in np.ndindex(grid.shape):
        pipe: Pipe = grid[x, y]
        for xd, yd in pipe.connected_positions():
            neighbour_pipe: Pipe = grid[x + xd, y + yd]
            if (
                -xd,
                -yd,
            ) in neighbour_pipe.connected_positions():  # we need both-sides relationship :)
                pipe.add_neighbour(neighbour_pipe)
    return grid


def solve_part1(grid: np.array) -> int:
    current_pipes = [pipe for pipe in grid.ravel() if pipe.type == PipeType.START]

    step = 0
    while current_pipes:
        new_current_pipes = []
        for pipe in current_pipes:
            for neighbour_pipe in pipe.neighbours:
                if neighbour_pipe.visited:
                    continue
                neighbour_pipe.visited = True
                new_current_pipes.append(neighbour_pipe)
        current_pipes = new_current_pipes
        step += 1

    return step - 1


def solve_part2(grid: np.array) -> int:
    new_grid = inflate_grid(grid)

    current_positions = [(0, 0)]
    while current_positions:
        x, y = current_positions.pop()
        for xd, yd in [N, S, W, E]:
            if 0 <= x + xd < new_grid.shape[0] and 0 <= y + yd < new_grid.shape[1]:
                neigh: Pipe = new_grid[x + xd, y + yd]
                if neigh.visited:
                    continue
                neigh.visited = True
                if neigh.type.blocking():
                    continue
                current_positions.append((x + xd, y + yd))

    def score_pipe(pipe: Pipe) -> int:
        return 1 if not pipe.visited and not pipe.is_glue() else 0

    return sum([score_pipe(pipe) for pipe in np.ravel(new_grid)])


def inflate_grid(grid: np.array) -> np.array:
    def create_glue_pipe(blocking: bool) -> Pipe:
        return Pipe(
            PipeType.GLUE_BLOCKING.value
            if blocking
            else PipeType.GLUE_NONBLOCKING.value
        )

    rows = []
    for x in range(grid.shape[0] - 1):
        row = []
        for y in range(grid.shape[1] - 1):
            pipe = grid[x, y]
            next_pipe = grid[x, y + 1]
            row.append(pipe)
            row.append(create_glue_pipe(next_pipe in pipe.neighbours))
        row.append(grid[x, grid.shape[1] - 1])
        row.append(Pipe(PipeType.GLUE_NONBLOCKING.value))
        rows.append(row)

        sep_row = []
        for y in range(grid.shape[1]):
            pipe = grid[x, y]
            next_pipe = grid[x + 1, y]
            sep_row.append(create_glue_pipe(next_pipe in pipe.neighbours))
            sep_row.append(Pipe(PipeType.GLUE_NONBLOCKING.value))
        rows.append(sep_row)

    sep_row = []
    for y in range(grid.shape[1]):
        sep_row.append(grid[grid.shape[0] - 1, y])
        sep_row.append(Pipe(PipeType.GLUE_NONBLOCKING.value))
    rows.append(sep_row)

    return np.matrix(rows)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
