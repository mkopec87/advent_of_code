from collections import deque

import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)


def main():
    points = load_points()

    grid = create_grid(points)
    print(f"Shape of grid: {grid.shape}")

    result_part1 = 0
    for index, x in np.ndenumerate(grid):
        if x:
            result_part1 += len(list(empty_neighbour_cubes(grid, index)))

    result_part2 = 0
    reachable = find_reachable_cubes(grid)
    for index, x in np.ndenumerate(grid):
        if x:
            for neighbour_index in empty_neighbour_cubes(grid, index):
                if reachable[neighbour_index]:
                    result_part2 += 1

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")

    plot_grid(grid)


def load_points():
    points = []
    with open("input.txt") as f:
        for line in f.readlines():
            numbers = [int(x) + 1 for x in line.split(",")]  # add 1 for border
            points.append(tuple(numbers))
    return points


def create_grid(points):
    n_dims = len(points[0])
    grid_shape = [0 for _ in range(n_dims)]
    for point in points:
        assert len(point) == n_dims
        for dim in range(n_dims):
            assert point[dim] >= 0
            grid_shape[dim] = max(grid_shape[dim], point[dim] + 2)  # add 2 for borders

    grid = np.full(grid_shape, fill_value=False, dtype=bool)
    for point in points:
        grid[point] = True

    return grid


def empty_neighbour_cubes(grid, position):
    for dim in range(len(position)):
        for direction in [-1, 1]:
            neighbour_position = list(position)
            neighbour_position[dim] = position[dim] + direction
            neighbour_position = tuple(neighbour_position)
            if not grid[neighbour_position]:
                yield neighbour_position


def find_reachable_cubes(grid):
    visited = np.full(grid.shape, fill_value=False, dtype=bool)

    start_position = tuple(0 for _ in range(len(visited.shape)))
    visited[start_position] = True

    stack = deque()
    stack.append(start_position)
    while stack:
        position = stack.popleft()
        for neighbour in empty_neighbour_cubes(grid, position):
            if not visited[neighbour]:
                visited[neighbour] = True
                stack.append(neighbour)
    return visited


def plot_grid(grid):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.voxels(grid, edgecolor="k")
    plt.savefig("plot.png")


if __name__ == "__main__":
    main()
