import re
from itertools import chain


from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    shape_nr_to_size = {}
    result_part1 = 0
    for block in input_data.split("\n\n"):
        if m := re.match(r"([0-9]+):", block):
            shape_nr = int(m.group(1))
            shape = [list(l) for l in block.splitlines()[1:]]
            size = sum(1 for c in chain.from_iterable(shape) if c == "#")
            shape_nr_to_size[shape_nr] = size
        else:
            for line in block.splitlines():
                m = re.match(r"([0-9]+)x([0-9]+):([0-9 ]+)", line)
                area = int(m.group(1)) * int(m.group(2))
                counts = tuple(map(int, m.group(3).strip().split(" ")))
                required_area = sum(
                    shape_nr_to_size[i] * c for i, c in enumerate(counts)
                )
                print(area, required_area, counts)
                result_part1 += 1 if required_area <= area else 0
    print(shape_nr_to_size)

    result_part2 = None

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
