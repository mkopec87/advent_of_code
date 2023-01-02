import re

from tqdm import tqdm

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"


VAR_NAMES = set("wxyz")


def solve_part1(lines):
    # move imp lines to the bottom
    index = 0
    while True:
        line = lines[index]
        if line == "inp w":
            next_line = lines[index + 1]
            if "w" not in next_line.split(" ", 1)[1]:
                lines[index + 1] = line
                lines[index] = next_line
        index += 1
        if index == len(lines):
            break

    # merge mul 0 and add
    index = 0
    while True:
        line = lines[index]
        m = re.match("mul (.) 0", line)
        if m:
            variable_name = m.group(1)
            next_line = lines[index + 1]
            mm = re.match(f"add {variable_name} (.*)", next_line)
            if mm:
                addition = mm.group(1)
                lines[index + 1] = f"set {variable_name} {addition}"
                del lines[index]

        index += 1
        if index == len(lines) - 1:
            break

    # merge eql eql
    index = 0
    while True:
        line = lines[index]
        if line == "eql x w" and lines[index + 1] == "eql x 0":
            lines[index + 1] = "neql x w"
            del lines[index]
        index += 1
        if index == len(lines) - 1:
            break
    #
    # # drop add 0
    # lines = list(filter(lambda x: not re.match("add . 0$", x), lines))

    # drop div 1
    lines = list(filter(lambda x: not re.match("div . 1$", x), lines))

    with open("new-input.txt", "w") as out:
        for line in lines:
            out.write(line + "\n")

    # block by input reads
    indices = []
    for i, line in enumerate(lines):
        if line == "inp w":
            indices.append(i)
    indices.append(len(lines))
    blocks = []
    for i, j in zip(indices, indices[1:]):
        blocks.append(lines[i + 1 : j])
    pre_input_block = lines[: indices[0]]

    # pre-input
    state = {v: 0 for v in VAR_NAMES}
    apply_steps(state, pre_input_block)
    print("pre input state:", sorted(state))

    ranges = find_ranges(blocks)
    print(ranges)
    output = check(state, blocks, 0, ranges)
    print(output)


def check(start_state, blocks, block_index, ranges):
    if not blocks:
        return start_state["z"] == 0

    vals = range(9, 0, -1)
    if len(blocks) > 10:
        vals = tqdm(vals, desc=str(len(blocks)) + " " * (14 - len(blocks)))
    for inp in vals:
        state = {**start_state, "w": inp}
        apply_steps(state, blocks[0])

        if block_index + 1 in ranges and state["z"] % 26 not in ranges[block_index + 1]:
            continue

        ch = check(state, blocks[1:], block_index + 1, ranges)
        if ch:
            return inp + ch


def apply_steps(state, block):
    for step in block:
        make_step(state, step)


def make_step(state, step):
    spl = step.split(" ")
    command = spl[0]
    target = spl[1]
    if command == "add":
        state[target] += other(spl, state)
    elif command == "mul":
        state[target] *= other(spl, state)
    elif command == "div":
        state[target] //= other(spl, state)
    elif command == "mod":
        state[target] %= other(spl, state)
    elif command == "eql":
        state[target] = 1 if state[target] == other(spl, state) else 0
    elif command == "neql":
        state[target] = 1 if state[target] != other(spl, state) else 0
    elif command == "set":
        state[target] = other(spl, state)
    else:
        raise Exception("Unknown command ", command)


def other(spl, values):
    other = spl[2]
    return values[other] if other in VAR_NAMES else int(other)


def find_ranges(blocks):
    ranges = {}
    for i, block in enumerate(blocks):
        for line in block:
            m = re.match("add x ([^z]+)", line)
            if m:
                num = int(m.group(1))
                if num <= 9:
                    r1 = 1 - num
                    r2 = 9 - num
                    ranges[i] = range(min(r1, r2), max(r1, r2) + 1)
    return ranges


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    result_part1 = solve_part1(lines)
    result_part2 = 0

    # TODO:
    # - drop DIV x 1
    # - drop ADD x 0
    # - merge eql, eql into nql
    # - merge mul x 0, add x y -> set x y

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
