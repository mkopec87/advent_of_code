from typing import List

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    patterns = parse_input(input_data)

    result_part1 = sum(map(score_pattern_part1, patterns))
    result_part2 = sum(map(score_pattern_part2, patterns))

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> List[np.array]:
    lines = input_data.splitlines()
    lines.append("")
    patterns = []
    rows = []
    for line in lines:
        if not line:
            pattern = np.array(rows)
            rows = []
            patterns.append(pattern)
        else:
            rows.append(list(line))
    return patterns


def score_pattern_part1(pattern: np.array) -> int:
    candidates_vertical = []
    for x in range(pattern.shape[0] - 1):
        if (pattern[x, :] == pattern[x + 1, :]).all():
            candidates_vertical.append(x)
    for x in candidates_vertical:
        pos = (x, x + 1)
        while 0 <= pos[0] and pos[1] < pattern.shape[0]:
            if (pattern[pos[0], :] != pattern[pos[1], :]).any():
                break
            pos = (pos[0] - 1, pos[1] + 1)
        else:
            return 100 * (x + 1)

    candidates_horizontal = []
    for y in range(pattern.shape[1] - 1):
        if (pattern[:, y] == pattern[:, y + 1]).all():
            candidates_horizontal.append(y)
    for y in candidates_horizontal:
        pos = (y, y + 1)
        while 0 <= pos[0] and pos[1] < pattern.shape[1]:
            if (pattern[:, pos[0]] != pattern[:, pos[1]]).any():
                break
            pos = (pos[0] - 1, pos[1] + 1)
        else:
            return y + 1

    return 0


def score_pattern_part2(pattern: np.array) -> int:
    candidates = []
    for x in range(pattern.shape[0] - 1):
        if (pattern[x, :] != pattern[x + 1, :]).sum() <= 1:
            candidates.append(x)
    for x in candidates:
        pos = (x, x + 1)
        diffs_allowed = 1
        while 0 <= pos[0] and pos[1] < pattern.shape[0]:
            diffs = (pattern[pos[0], :] != pattern[pos[1], :]).sum()
            if diffs > diffs_allowed:
                break
            else:
                diffs_allowed -= diffs
            pos = (pos[0] - 1, pos[1] + 1)
        else:
            if diffs_allowed == 0:
                return 100 * (x + 1)

    candidates_vertical = []
    for y in range(pattern.shape[1] - 1):
        if (pattern[:, y] != pattern[:, y + 1]).sum() <= 1:
            candidates_vertical.append(y)
    for y in candidates_vertical:
        pos = (y, y + 1)
        diffs_allowed = 1
        while 0 <= pos[0] and pos[1] < pattern.shape[1]:
            diffs = (pattern[:, pos[0]] != pattern[:, pos[1]]).sum()
            if diffs > diffs_allowed:
                break
            else:
                diffs_allowed -= diffs
            pos = (pos[0] - 1, pos[1] + 1)
        else:
            if diffs_allowed == 0:
                return y + 1

    return 0


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
