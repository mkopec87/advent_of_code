from collections import deque

ch2points = {")": 3, "]": 57, "}": 1197, ">": 25137}
ch2points2 = {")": 1, "]": 2, "}": 3, ">": 4}
open2close = {"[": "]", "{": "}", "<": ">", "(": ")"}


def is_opening(sign):
    return sign in open2close.keys()


def score_line(line):
    stack = deque()
    for sign in line:
        if is_opening(sign):
            stack.append(sign)
        else:
            expected = stack.pop()
            if sign != open2close[expected]:
                return ch2points[sign]
    return 0


def score_line2(line):

    stack = deque()
    for sign in line:
        if is_opening(sign):
            stack.append(sign)
        else:
            stack.pop()

    result = 0
    while stack:
        result *= 5
        result += ch2points2[open2close[stack.pop()]]
    return result


def main():
    with open("input.txt") as f:
        lines = [[ch for ch in line.strip()] for line in f.readlines()]
    print(f"{len(lines)} read")

    scores = []
    part1 = 0
    for line in lines:
        score = score_line(line)
        if score:
            part1 += score
            continue
        scores.append(score_line2(line))

    result = sorted(scores)[int(len(scores) / 2)]
    print(f"Result part 1: {part1}")
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    main()
