import re
from collections import deque
from functools import reduce
from itertools import repeat
from operator import add
from typing import NamedTuple
from z3 import Solver, Int, IntVal
from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print


class State(NamedTuple):
    status: tuple[int, ...]
    buttons: set[set[int]]


class Node(NamedTuple):
    state: State
    depth: int


def main(debug: bool) -> None:
    input_data = load_data(debug)

    result_part1 = 0
    for line in tqdm(input_data.splitlines()):
        m = re.match(r"\[(?P<target>[.#]+)\] (?P<buttons>(\([0-9,]+\) )+)", line)
        target = tuple(c == "#" for c in m.group("target"))
        buttons = frozenset(
            [
                frozenset(map(int, s[1:-1].split(",")))
                for s in m.group("buttons").strip().split(" ")
            ]
        )
        result_part1 += solve(target, buttons)

    result_part2 = 0
    for line in tqdm(input_data.splitlines()):
        m = re.match(
            r"\[(?P<target>[.#]+)\] (?P<buttons>(\([0-9,]+\) )+){(?P<joltage>[0-9,]+)}",
            line,
        )
        target = tuple(map(int, m.group("joltage").split(",")))
        buttons = list(
            [
                frozenset(map(int, s[1:-1].split(",")))
                for s in m.group("buttons").strip().split(" ")
            ]
        )
        result_part2 += solve_part2(target, buttons)

    submit_or_print(result_part1, result_part2, debug)


def solve(target: tuple[bool, ...], buttons: set[set[int]]):
    queue: deque[Node] = deque(
        [
            Node(
                state=State(status=tuple(repeat(0, len(target))), buttons=buttons),
                depth=0,
            )
        ]
    )

    visited_states = set()
    while queue:
        node = queue.popleft()
        state = node.state
        if state in visited_states:
            continue
        visited_states.add(state)
        if state.status == target:
            return node.depth

        for button in state.buttons:
            new_state = State(
                status=tuple(
                    int(not s) if i in button else s for i, s in enumerate(state.status)
                ),
                buttons=frozenset(b for b in state.buttons if b != button),
            )
            queue.append(
                Node(
                    new_state,
                    depth=node.depth + 1,
                )
            )
    return -1


def solve_part2(target, buttons):
    presses = max(target)

    while True:
        s = Solver()
        button_vars = [Int(i) for i in range(len(buttons))]
        for light_nr, target_joltage in enumerate(target):
            target_joltage_constant = IntVal(target_joltage)
            parts = [
                button_vars[button_index]
                for button_index, button in enumerate(buttons)
                if light_nr in button
            ]
            s.add(target_joltage_constant == reduce(add, parts))
        for i in range(len(buttons)):
            s.add(button_vars[i] >= 0)
        total_button_pushes = IntVal(presses)
        s.add(total_button_pushes == reduce(add, button_vars))
        if str(s.check()) == "sat":
            return presses
        else:
            presses += 1


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
