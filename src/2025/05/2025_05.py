from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    ids, ranges = parse_input(input_data)
    print(f"{len(ranges)} ranges, {len(ids)} ids")

    result_part1 = solve_part1(ids, ranges)
    result_part2 = solve_part2(ranges)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> tuple[list[int], list[tuple[int, int]]]:
    ranges_str, ids_str = input_data.split("\n\n")
    ranges = [
        (int(f), int(t))
        for line in ranges_str.splitlines()
        for f, t in [line.split("-")]
    ]
    ids = [int(i) for i in ids_str.splitlines()]
    return ids, ranges


def solve_part1(ids: list[int], ranges: list[tuple[int, int]]) -> int:
    result_part1 = 0
    for i in ids:
        for f, t in ranges:
            if f <= i <= t:
                result_part1 += 1
                break
    return result_part1


def solve_part2(ranges: list[tuple[int, int]]) -> int:
    merged_ranges = set()
    to_add = set(ranges)
    while to_add:
        f, t = to_add.pop()
        for m_f, m_t in merged_ranges:
            if f <= m_t and t >= m_f:
                new_range = min(f, m_f), max(t, m_t)
                to_add.add(new_range)
                merged_ranges.remove((m_f, m_t))
                break
        else:
            merged_ranges.add((f, t))
    result_part2 = sum([r[1] - r[0] + 1 for r in merged_ranges])
    return result_part2


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
