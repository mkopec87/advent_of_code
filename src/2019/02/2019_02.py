from itertools import product
from operator import add, mul
from typing import List

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)
    parsed_input = [int(x) for x in input_data.split(",")]

    # part 1
    result_part1 = solve(parsed_input, 12, 2)[0]

    # part 2
    for i, j in product(range(100), range(100)):
        solution = solve(parsed_input, i, j)
        if solution and solution[0] == 19690720:
            break
    else:
        raise Exception("No solution found!")
    result_part2 = solution[1] * 100 + solution[2]

    submit_or_print(result_part1, result_part2, debug)


def solve(input_list: List[int], val1: int, val2: int) -> List[int]:
    try:
        memory = input_list.copy()
        memory[1] = val1
        memory[2] = val2

        pos = 0
        while memory[pos] != 99:
            if memory[pos] == 1:
                op = add
            elif memory[pos] == 2:
                op = mul
            else:
                raise Exception(f"Unknown op code! {memory[pos]}")
            memory[memory[pos + 3]] = op(
                memory[memory[pos + 1]], memory[memory[pos + 2]]
            )
            pos += 4

        return memory
    except:
        return [-1]


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
