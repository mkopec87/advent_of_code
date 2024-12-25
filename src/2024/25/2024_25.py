from typing import List, Tuple

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    keys, locks, height = parse_input(input_data)
    print(f"{len(locks)} locks")
    print(f"{len(keys)} keys")
    print(f"lock and key height: {height}")

    result_part1 = 0
    for lock in locks:
        for key in keys:
            result_part1 += int(fit(key, lock, height))

    result_part2 = None

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> Tuple[List[List[int]], List[List[int]], int]:
    locks = []
    keys = []
    spl = input_data.split("\n\n")
    for s in spl:
        lines = s.splitlines()
        heights = [0 for _ in range(len(lines[0]))]
        for line in lines[1:-1]:
            for i, ch in enumerate(line):
                if "#" == ch:
                    heights[i] += 1

        lock = lines[0][0] == "#"
        if lock:
            locks.append(heights)
        else:
            keys.append(heights)

    height = len(spl[0].splitlines()) - 2
    return keys, locks, height


def fit(key: List[int], lock: List[int], height: int) -> bool:
    for l, k in zip(lock, key):
        if l + k > height:
            return False
    return True


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
