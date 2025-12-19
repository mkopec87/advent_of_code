import dataclasses
import re

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Range:
    start: int
    end: int
    property: str


@dataclasses.dataclass
class MapRange:
    start: int
    end: int
    shift: int


@dataclasses.dataclass
class Map:
    map_from: str
    map_to: str
    ranges: list[MapRange]


def main(debug: bool) -> None:
    input_data = load_data(debug)

    maps = load_maps(input_data)

    # part 1
    seeds = load_seeds(input_data)
    result_part1 = solve_part1(maps, seeds)

    # part 2
    seed_ranges = load_ranges(input_data)
    result_part2 = solve_part2(maps, seed_ranges)

    submit_or_print(result_part1, result_part2, debug)


def load_maps(input_data: str) -> dict[str, Map]:
    lines = input_data.splitlines()
    maps = {}
    line_nr = 2
    while line_nr < len(lines):
        m = re.match(r"([^-]+)-to-([^- ]+).*", lines[line_nr])
        map_from = m.group(1)
        map_to = m.group(2)
        ranges = []
        line_nr += 1
        while line_nr < len(lines) and lines[line_nr]:
            dest_start, source_start, range_len = (
                int(n.strip()) for n in lines[line_nr].split(" ")
            )
            end = source_start + range_len
            shift = dest_start - source_start
            ranges.append(MapRange(source_start, end, shift))
            line_nr += 1
        line_nr += 1
        ranges = sorted(ranges, key=lambda r: r.start)
        maps[map_from] = Map(map_from, map_to, ranges)
    return maps


def load_seeds(input_data: str) -> set[int]:
    first_line = input_data.splitlines()[0]
    return {int(n) for n in re.findall(r"\d+", first_line)}


def load_ranges(input_data: str) -> list[Range]:
    seed_ranges = []
    first_line = input_data.splitlines()[0]
    numbers = [int(n.strip()) for n in first_line.split(":")[1].strip().split(" ")]
    i = 0
    while i < len(numbers):
        seed_ranges.append(
            Range(start=numbers[i], end=numbers[i] + numbers[i + 1], property="seed")
        )
        i += 2
    return seed_ranges


def solve_part1(maps: dict[str, Map], seeds: set[int]) -> int:
    values = []
    for value in seeds:
        property = "seed"
        while property != "location":
            m = maps[property]
            property = m.map_to
            for r in m.ranges:
                if r.start <= value < r.end:
                    value += r.shift
                    break
        values.append(value)
    result_part1 = min(values)
    return result_part1


def solve_part2(maps, seed_ranges) -> int:
    min_value = None
    while seed_ranges:
        seed_range = seed_ranges.pop()

        if seed_range.property == "location":
            if min_value is None:
                min_value = seed_range.start
            else:
                min_value = min(min_value, seed_range.start)

        else:
            mapping = maps[seed_range.property]
            for r in mapping.ranges:
                if r.end > seed_range.start:
                    # first overlapping range
                    overlap_start = max(r.start, seed_range.start)
                    overlap_end = min(r.end, seed_range.end)

                    if overlap_end > overlap_start:
                        # send overlapping part
                        seed_ranges.append(
                            Range(
                                overlap_start + r.shift,
                                overlap_end + r.shift,
                                mapping.map_to,
                            )
                        )

                        if overlap_start > seed_range.start:
                            # send non-overlapping part before overlap
                            seed_ranges.append(
                                Range(seed_range.start, overlap_start, mapping.map_to)
                            )

                        if overlap_end < seed_range.end:
                            # send non-overlapping part after overlap
                            seed_ranges.append(
                                Range(overlap_end, seed_range.end, mapping.map_from)
                            )

                        break
                    else:
                        # no overlap, it means we are before first range
                        seed_ranges.append(
                            Range(seed_range.start, seed_range.end, mapping.map_to)
                        )
                        break

            else:
                # no overlap with any range, it means we are after last range
                seed_ranges.append(
                    Range(seed_range.start, seed_range.end, mapping.map_to)
                )

    return min_value


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
