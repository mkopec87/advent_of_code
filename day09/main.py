import numpy as np


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    moves = parse_moves(lines)

    result_part1 = solve(moves, 2)
    print(f"Result part 1: {result_part1}")

    result_part2 = solve(moves, 10)
    print(f"Result part 2: {result_part2}")


def parse_moves(lines):
    moves = []
    for line in lines:
        split = line.split(" ")
        move = split[0], int(split[1])
        moves.append(move)
    return moves


def solve(moves, line_len):
    node_to_pos = {i: [0, 0] for i in range(line_len)}
    visited = {tuple(node_to_pos[line_len - 1])}

    for direction, count in moves:
        for _ in range(count):

            # move head
            head_pos = node_to_pos[0]
            if direction == "U":
                head_pos[0] += 1
            elif direction == "D":
                head_pos[0] -= 1
            elif direction == "R":
                head_pos[1] += 1
            elif direction == "L":
                head_pos[1] -= 1
            else:
                raise Exception("Unknown direction", direction)

            # move nodes
            for n in range(1, line_len):
                head_pos = node_to_pos[n - 1]
                tail_pos = node_to_pos[n]
                if head_pos[0] == tail_pos[0]:  # same row
                    diff = head_pos[1] - tail_pos[1]
                    if abs(diff) > 1:
                        tail_pos[1] += np.sign(diff)
                elif head_pos[1] == tail_pos[1]:  # same col
                    diff = head_pos[0] - tail_pos[0]
                    if abs(diff) > 1:
                        tail_pos[0] += np.sign(diff)
                else:
                    diff_x = head_pos[0] - tail_pos[0]
                    diff_y = head_pos[1] - tail_pos[1]
                    if abs(diff_x) + abs(diff_y) > 2:  # diagonal move
                        tail_pos[0] += np.sign(diff_x)
                        tail_pos[1] += np.sign(diff_y)

            visited.add(tuple(node_to_pos[line_len - 1]))

    return len(visited)


if __name__ == "__main__":
    main()
