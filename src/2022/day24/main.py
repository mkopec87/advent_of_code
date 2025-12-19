from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from queue import PriorityQueue

import numpy as np


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def __lt__(self, other):
        return self.value[0] < other.value[0] or self.value[1] < other.value[1]


class Point:
    def __init__(self, wall, blizzard: Direction | None = None):
        self.blizzards = Counter()
        self.wall = wall
        if blizzard:
            self.blizzards[blizzard] = 1

    def add_blizzards(self, blizzard, count=1):
        self.blizzards[blizzard] += count

    def __str__(self):
        if self.wall:
            return "#"
        elif len(self.blizzards) == 0:
            return "."
        elif len(self.blizzards) > 1:
            return str(len(self.blizzards))
        else:
            return list(self.blizzards.keys())[0]

    def __hash__(self):
        return hash(tuple([self.wall, *sorted(self.blizzards.items())]))

    def __eq__(self, other):
        return (self.wall == other.wall) and (
            sorted(self.blizzards.items()) == sorted(other.blizzards.items())
        )


class Maze:
    def __init__(self, shape):
        self.grid = np.empty(shape, dtype=Point)

    def __hash__(self):
        return hash(tuple([point for index, point in np.ndenumerate(self.grid)]))

    def __eq__(self, other):
        for index, point in np.ndenumerate(self.grid):
            if point != other.grid[index]:
                return False
        return True

    def illegal_position(self, new_pos: tuple[int, ...]):
        if any([not (0 <= new_pos[i] < self.grid.shape[i]) for i in range(2)]):
            return True
        point = self.grid[new_pos]
        return point.wall or point.blizzards


@dataclass
class State:
    position: tuple[int, ...]
    maze_id: int

    def distance_to_end(self, end_pos):
        return sum(abs(end_pos[i] - self.position[i]) for i in range(2))

    def __hash__(self):
        return hash(tuple([self.position, self.maze_id]))

    def __lt__(self, other):
        return False


class PQ:
    def __init__(self):
        self.queue = PriorityQueue()
        self.states = set()

    def empty(self):
        return len(self.states) == 0

    def pop_min(self):
        elem = self.queue.get()[1]
        self.states.remove(elem)
        return elem

    def add(self, cost, state_id):
        if state_id in self.states:
            return
        self.queue.put((cost, state_id))
        self.states.add(state_id)


def main():
    path = "input.txt"

    maze, start_pos, end_pos = read_input(path)

    print("maze shape:", maze.grid.shape)
    print("start", start_pos)
    print("end", end_pos)

    print("Enumerating mazes...")
    mazes = enumerate_mazes(maze)
    print(f"{len(mazes)} mazes found.")

    # part 1
    initial_state = State(start_pos, 0)
    result_part1, current_state = a_star(initial_state, end_pos, mazes)

    # part 2
    time_back, current_state = a_star(current_state, start_pos, mazes)
    time_back_again, _ = a_star(current_state, end_pos, mazes)
    result_part2 = result_part1 + time_back + time_back_again

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


def read_input(path: str) -> tuple[Maze, tuple[int, ...], tuple[int, ...]]:
    with open(path) as f:
        lines = [line.strip() for line in f.readlines()]

    char_to_direction = {
        "^": Direction.NORTH,
        ">": Direction.EAST,
        "v": Direction.SOUTH,
        "<": Direction.WEST,
    }

    maze = Maze((len(lines), len(lines[0])))
    for x, line in enumerate(lines):
        for y, ch in enumerate(line):
            maze.grid[x, y] = Point(
                wall=ch == "#", blizzard=char_to_direction.get(ch, None)
            )

    start_pos = (
        0,
        min([y for y, point in enumerate(maze.grid[0, :]) if not point.wall]),
    )
    end_pos = (
        maze.grid.shape[0] - 1,
        max(
            [
                y
                for y, point in enumerate(maze.grid[maze.grid.shape[0] - 1, :])
                if not point.wall
            ]
        ),
    )

    return maze, start_pos, end_pos


def enumerate_mazes(maze: Maze) -> list[Maze]:
    mazes = []
    mazes_set = set()
    while True:
        if maze in mazes_set:
            break
        mazes.append(maze)
        mazes_set.add(maze)
        maze = next_maze(maze)
    return mazes


def next_maze(maze: Maze) -> Maze:
    new_maze = Maze(maze.grid.shape)

    # copy walls & empty points
    for index, point in np.ndenumerate(maze.grid):
        new_maze.grid[index] = Point(wall=point.wall)

    # move blizzards
    for index, point in np.ndenumerate(maze.grid):
        for direction, count in point.blizzards.items():
            blizzard_next_pos = [index[i] + direction.value[i] for i in range(2)]

            # wrap around walls
            for i in range(2):
                if blizzard_next_pos[i] == new_maze.grid.shape[i] - 1:
                    blizzard_next_pos[i] = 1
                elif blizzard_next_pos[i] == 0:
                    blizzard_next_pos[i] = new_maze.grid.shape[i] - 2
            new_maze.grid[tuple(blizzard_next_pos)].add_blizzards(direction, count)

    return new_maze


def a_star(start_state: State, end_pos: tuple[int, ...], mazes) -> tuple[int, State]:
    g_score = defaultdict(lambda: np.inf)
    f_score = defaultdict(lambda: np.inf)

    g_score[start_state] = 0
    f_score[start_state] = g_score[start_state] + start_state.distance_to_end(end_pos)

    queue = PQ()
    queue.add(f_score[start_state], start_state)

    while not queue.empty():
        current_state = queue.pop_min()
        if current_state.distance_to_end(end_pos) == 0:
            return g_score[current_state], current_state

        new_maze_id = (current_state.maze_id + 1) % len(mazes)
        new_maze = mazes[new_maze_id]

        for move in [*[d.value for d in Direction], (0, 0)]:
            new_pos = tuple([current_state.position[i] + move[i] for i in range(2)])
            if new_maze.illegal_position(new_pos):
                continue
            tentative_g_score = g_score[current_state] + 1
            new_state = State(new_pos, new_maze_id)
            if tentative_g_score < g_score[new_state]:
                g_score[new_state] = tentative_g_score
                f_score[new_state] = tentative_g_score + new_state.distance_to_end(
                    end_pos
                )
                queue.add(f_score[new_state], new_state)

    raise Exception("No solution found!")


if __name__ == "__main__":
    main()
