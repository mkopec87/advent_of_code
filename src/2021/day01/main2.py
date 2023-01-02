from collections import deque


def main():
    with open("input.txt") as f:
        measurements = [int(l.strip()) for l in f.readlines()]

    prev = deque()
    prev.extend(measurements[:3])

    increased = 0
    for m in measurements[3:]:

        prev_sum = sum(prev)

        prev.popleft()
        prev.append(m)

        next_sum = sum(prev)
        if next_sum > prev_sum:
            increased += 1

    print(increased)


if __name__ == "__main__":
    main()
