def main():
    elves = []
    with open("input-small.txt") as f:
        elf = 0
        for l in f.readlines():
            if l.strip():
                c = int(l.strip())
                elf += c
            else:
                elves.append(elf)
                elf = 0
        if c:
            elves.append(elf)

    print(len(elves))

    print(max(elves))

    elves = sorted(elves)
    print(sum(elves[-3:]))


if __name__ == "__main__":
    main()
