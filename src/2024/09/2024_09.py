import dataclasses


from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Block:
    position: int
    length: int
    file: bool
    id: int | None


def main(debug: bool) -> None:
    input_data = load_data(debug)

    digits = list(map(int, input_data))

    disk = ["." for _ in range(sum(digits))]
    file = True
    pos = 0
    id = 0
    for d in digits:
        for _ in range(d):
            if file:
                disk[pos] = id
            pos += 1
        if file:
            id += 1
        file = not file

    pos_right = len(disk) - 1
    pos_left = 0
    while True:
        while disk[pos_left] != "." and pos_left < len(disk):
            pos_left += 1
        while disk[pos_right] == "." and pos_right > pos_left:
            pos_right -= 1
        if pos_left >= pos_right:
            break

        disk[pos_left] = disk[pos_right]
        disk[pos_right] = "."

    result_part1 = 0
    pos = 0
    while disk[pos] != ".":
        result_part1 += int(disk[pos]) * pos
        pos += 1

    # part 2
    digits = list(map(int, input_data))
    blocks = []
    file = True
    pos = 0
    id = 0
    for d in digits:
        blocks.append(Block(position=pos, length=d, file=file, id=id if file else None))
        if file:
            id += 1
        file = not file
        pos += d

    print_blocks(blocks)
    block_index_right = len(blocks) - 1
    while block_index_right > 1:
        if not blocks[block_index_right].file:
            block_index_right -= 1
            continue

        file = blocks[block_index_right]
        # print(f"looking for place for {file}")

        # find space
        block_index_left = 0
        while block_index_left < block_index_right:
            space = blocks[block_index_left]
            if not space.file and space.length >= file.length:
                break
            block_index_left += 1
        else:
            # print(f"no space")
            block_index_right -= 1
            continue

        space = blocks[block_index_left]
        # print(f"found space {space}")

        # space is enough
        if space.length == file.length:
            blocks[block_index_left], blocks[block_index_right] = (
                blocks[block_index_right],
                blocks[block_index_left],
            )
            file.position, space.position = space.position, file.position
            block_index_right -= 1

        else:
            # we have to split
            blocks.pop(block_index_right)
            blocks.insert(block_index_left, file)
            file.position = space.position
            space.position += file.length
            space.length -= file.length

            block_index_right -= 1

        # print_blocks(blocks)

    result_part2 = 0
    for b in blocks:
        if b.file:
            for p in range(b.length):
                result_part2 += (b.position + p) * b.id

    submit_or_print(result_part1, result_part2, debug)


def print_disk(disk):
    print(" ".join(disk))


def print_blocks(blocks):
    for b in blocks:
        for i in range(b.length):
            print(b.id if b.file else ".", end="")
    print()


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
