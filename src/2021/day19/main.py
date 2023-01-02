import itertools
from collections import Counter
from typing import List

import networkx as nx
import numpy as np

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"


class Scanner:
    def __init__(self, number, location=None):
        self.number = number
        self.positions: np.array = None
        self.location = location

    def add_position(self, position: List[int]):
        if self.positions is None:
            self.positions = np.array(position)
        else:
            self.positions = np.vstack([self.positions, np.array(position)])

    def rotate(self, indices, signs):
        rotated = Scanner(number=self.number, location=self.location)
        new_positions = self.positions.copy()
        new_positions = new_positions[:, indices]
        assert new_positions.shape[1] == 3
        for i, s in enumerate(signs):
            if not s:
                new_positions[:, i] = -new_positions[:, i]
        rotated.positions = new_positions
        return rotated

    def shift(self, shifts):
        new_positions = self.positions.copy()
        for col_index, shift in enumerate(shifts):
            new_positions[:, col_index] = new_positions[:, col_index] + shift

        shifted = Scanner(number=self.number, location=self.location)
        shifted.positions = new_positions
        return shifted

    def distance(self, other):
        dist = 0
        for i in range(3):
            dist += abs(self.location[i] - other.location[i])
        return dist

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        return self.number == other.number

    def __ge__(self, other):
        return self.number >= other.number

    def __lt__(self, other):
        return self.number < other.number

    def __repr__(self):
        return f"Scanner {self.number} with {len(self.positions)} positions, location: {self.location}"

    def __str__(self):
        return self.__repr__()


def find_shifts(source, candidate):
    def find_shift(column_index):
        source_values = source.positions[:, column_index]
        candidate_values = candidate.positions[:, column_index]

        shift_candidates = set()
        for val1 in source_values:
            for val2 in candidate_values:
                shift_candidates.add(val1 - val2)

        source_values_set = Counter(source_values)
        for diff in sorted(shift_candidates):
            candidate_values_shifted_set = Counter(candidate_values + diff)
            matched_counter = candidate_values_shifted_set & source_values_set
            matched_count = sum(matched_counter.values())
            if matched_count >= 12:
                return diff
        return None

    shifts = []
    for column_index in range(3):
        shift = find_shift(column_index)
        if shift is None:
            return None
        shifts.append(shift)
    return shifts


def find_match(source, candidate):
    for indices in itertools.permutations(range(3)):
        for signs in itertools.product([True, False], [True, False], [True, False]):
            rotated = candidate.rotate(indices=indices, signs=signs)
            shifts = find_shifts(source, rotated)
            if shifts:
                print(f"\tFound: {candidate.number} - {indices}, {signs}, {shifts}")
                shifted = rotated.shift(shifts)
                shifted.location = shifts
                return shifted
    return None


def find_matches(source, candidates):
    result = []
    for candidate in sorted(candidates):
        shifted = find_match(source, candidate)
        if shifted:
            result.append(shifted)
    return result


def main():
    scanners = load_scanners()
    print(f"{len(scanners)} scanners loaded")

    traverse_graph = nx.DiGraph()
    overlap_graph = nx.Graph()
    for scanner in scanners:
        traverse_graph.add_node(scanner.number)
        overlap_graph.add_node(scanner.number)

    scanners[0].location = [0, 0, 0]
    sources = [scanners[0]]
    candidates = set(scanners) - set(sources)
    results = sources.copy()
    while sources:
        source = sources.pop()
        print(
            f"Looking for match from {source}\n\tcandidates: {sorted([x.number for x in candidates])}"
        )
        matching_scanners = find_matches(source, candidates)
        if len(matching_scanners) == 0:
            print("\tNone found")
            continue

        for scanner in matching_scanners:
            traverse_graph.add_edge(source.number, scanner.number)

        results.extend(matching_scanners)
        sources.extend(matching_scanners)
        candidates -= set(matching_scanners)
        if not candidates:
            break
    print(f"{len(results)} scanners reached")

    for s1, s2 in itertools.combinations(scanners, 2):
        if find_match(s1, s2):
            overlap_graph.add_edge(s1.number, s2.number)

    nx.write_graphml(traverse_graph, "traverse.graphml")
    nx.write_graphml(overlap_graph, "overlap.graphml")

    beacons = set()
    for scanner in results:
        for position in scanner.positions:
            beacons.add(tuple(x for x in position))
    print(len(beacons))

    max_dist = max(
        [
            scanner1.distance(scanner2)
            for scanner1, scanner2 in itertools.combinations(results, 2)
        ]
    )

    result_part1 = len(beacons)
    result_part2 = max_dist

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


def load_scanners():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")
    scanners = []
    for line in lines:
        if line.startswith("---"):
            scanner = Scanner(number=int(line.split(" ")[2]))
        elif line.strip() == "":
            scanners.append(scanner)
            scanner = None
        else:
            scanner.add_position([int(x) for x in line.strip().split(",")])
    if scanner:
        scanners.append(scanner)
    return scanners


if __name__ == "__main__":
    main()
