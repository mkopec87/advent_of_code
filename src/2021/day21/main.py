import dataclasses
import itertools
from collections import Counter
from typing import Tuple

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"


class DeterministicDice:
    def __init__(self):
        self.counter = 1
        self.rolls = 0

    def sum3rolls(self):
        result = self.counter * 3 + 3
        self.counter += 3
        self.rolls += 3
        return result


@dataclasses.dataclass(frozen=True)
class State:
    positions: Tuple[int, int]
    points: Tuple[int, int] = (0, 0)
    next_player_index: int = 0

    def finished(self, limit):
        return max(self.points) >= limit


def part1(player1_start_pos, player2_start_pos):
    dice = DeterministicDice()

    initial_state = State(positions=(player1_start_pos - 1, player2_start_pos - 1))

    states_counter = Counter([initial_state])
    while True:
        state, count = states_counter.popitem()
        if state.finished(1000):
            return dice.rolls * state.points[state.next_player_index]

        outcome = dice.sum3rolls()
        position = (state.positions[state.next_player_index] + outcome) % 10
        points = state.points[state.next_player_index] + position + 1
        if state.next_player_index == 0:
            next_positions = (position, state.positions[1])
            next_points = (points, state.points[1])
        else:
            next_positions = (state.positions[0], position)
            next_points = (state.points[0], points)
        next_player_index = (state.next_player_index + 1) % 2

        next_state = State(
            positions=next_positions,
            points=next_points,
            next_player_index=next_player_index,
        )
        states_counter[next_state] += count


def part2(player1_start_pos: int, player2_start_pos: int):
    combinations = itertools.product(*[range(1, 4) for _ in range(3)])
    outcomes = Counter([sum(x) for x in combinations])

    initial_state = State(positions=(player1_start_pos - 1, player2_start_pos - 1))

    wins = [0, 0]
    states_counter = Counter([initial_state])
    while states_counter:
        state, count = states_counter.popitem()

        # check if state is finished
        if state.finished(21):
            for i in range(2):
                if state.points[i] >= 21:
                    wins[i] += count
        else:
            # add new states
            for outcome, outcome_count in outcomes.items():
                position = (state.positions[state.next_player_index] + outcome) % 10
                points = state.points[state.next_player_index] + position + 1
                if state.next_player_index == 0:
                    next_positions = (position, state.positions[1])
                    next_points = (points, state.points[1])
                else:
                    next_positions = (state.positions[0], position)
                    next_points = (state.points[0], points)
                next_player_index = (state.next_player_index + 1) % 2

                next_state = State(
                    positions=next_positions,
                    points=next_points,
                    next_player_index=next_player_index,
                )
                states_counter[next_state] += count * outcome_count

    return max(wins)


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    player1_start_pos = int(lines[0].split(":")[1].strip())
    player2_start_pos = int(lines[1].split(":")[1].strip())

    print(f"Player 1 start: {player1_start_pos}")
    print(f"Player 2 start: {player2_start_pos}")

    result_part1 = part1(player1_start_pos, player2_start_pos)
    result_part2 = part2(player1_start_pos, player2_start_pos)

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
