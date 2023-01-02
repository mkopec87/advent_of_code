from collections import defaultdict
from functools import reduce
from typing import Set


def get_set_only_item(s):
    assert len(s) == 1
    return next(iter(s))


str2digit = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def decode_number(outputs):
    r = 0
    m = 1
    for digit in reversed(outputs):
        r += str2digit[digit] * m
        m *= 10
    return r


def main():
    with open("input.txt") as f:
        lines = f.readlines()
    print(f"{len(lines)} read")

    total = 0
    for line in lines:
        spl = line.split("|")
        signals = [set(x) for x in spl[0].strip().split(" ")]
        outputs = [set(x) for x in spl[1].strip().split(" ")]

        len2signals = defaultdict(list)
        for signal in signals:
            len2signals[len(signal)].append(signal)

        assert 2 in len2signals.keys()
        assert 3 in len2signals.keys()
        assert 4 in len2signals.keys()

        two_letters = len2signals[2][0]
        three_letters = len2signals[3][0]
        four_letters = len2signals[4][0]
        five_letters_common: Set[str] = reduce(set.intersection, len2signals[5])
        six_letters_common: Set[str] = reduce(set.intersection, len2signals[6])

        a_mapping = three_letters - two_letters
        b_d_mapping = four_letters - two_letters
        d_mapping = b_d_mapping & five_letters_common
        b_mapping = b_d_mapping - d_mapping
        g_mapping = five_letters_common - a_mapping - d_mapping
        f_mapping = six_letters_common - a_mapping - b_mapping - g_mapping
        c_mapping = two_letters - f_mapping

        mapping = {
            get_set_only_item(a_mapping): "a",
            get_set_only_item(b_mapping): "b",
            get_set_only_item(c_mapping): "c",
            get_set_only_item(d_mapping): "d",
            get_set_only_item(f_mapping): "f",
            get_set_only_item(g_mapping): "g",
        }
        e_mapping = get_set_only_item({l for l in "abcdefg"} - mapping.keys())
        mapping[e_mapping] = "e"

        mapped_outputs = [
            "".join(sorted(map(lambda x: mapping[x], output))) for output in outputs
        ]
        number = decode_number(mapped_outputs)
        print(mapped_outputs, number)

        total += number

    result = total
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
