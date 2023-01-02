def main():
    with open("input.txt") as f:
        measurements = [int(l.strip()) for l in f.readlines()]

    print(measurements)

    prev = None
    increased = 0
    for m in measurements:
        if prev and prev < m:
            increased += 1
        prev = m

    print(increased)


if __name__ == "__main__":
    main()
