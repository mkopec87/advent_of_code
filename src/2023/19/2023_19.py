import operator
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print

ACCEPT = "A"
REJECT = "R"


@dataclass
class Part:
    ratings: Dict

    def score(self):
        return sum(self.ratings.values())


@dataclass(frozen=True)
class Range:
    min: int
    max: int

    def split(self, split: int) -> Tuple["Range", "Range"]:
        assert split + 1 <= self.max
        return Range(self.min, split), Range(split + 1, self.max)


@dataclass(frozen=True)
class Ranges:
    ranges: Dict[str, Range]

    def combinations(self):
        return np.prod([r.max - r.min + 1 for r in self.ranges.values()])


@dataclass
class Rule:
    result: str
    property: Optional[str] = None
    op_str: Optional[str] = None
    value: Optional[int] = None

    def __post_init__(self):
        self.has_condition = self.property is not None
        if self.has_condition:
            match self.op_str:
                case "<":
                    op = operator.lt
                case ">":
                    op = operator.gt
                case _:
                    raise Exception(f"Unknown op string: {self.op_str}")
            self.op = op

    def matches(self, part: Part):
        if not self.has_condition:
            return True
        return self.op(part.ratings[self.property], self.value)

    def matches_whole(self, ranges: Ranges) -> bool:
        prop_range = ranges.ranges[self.property]
        return self.op(prop_range.min, self.value) and self.op(
            prop_range.max, self.value
        )

    def not_matches_whole(self, ranges: Ranges) -> bool:
        prop_range = ranges.ranges[self.property]
        return not (
            self.op(prop_range.min, self.value) or self.op(prop_range.max, self.value)
        )

    def split(self, ranges: Ranges) -> Tuple[Ranges, Ranges]:
        left_ranges = ranges.ranges.copy()
        right_ranges = ranges.ranges.copy()

        prop_range = ranges.ranges[self.property]
        if self.op_str == "<":
            split_point = self.value - 1
            left_matching = True
        else:
            split_point = self.value
            left_matching = False
        left_ranges[self.property] = Range(prop_range.min, split_point)
        right_ranges[self.property] = Range(split_point + 1, prop_range.max)

        pair = [Ranges(left_ranges), Ranges(right_ranges)]
        if not left_matching:
            pair = reversed(pair)
        return tuple(pair)


@dataclass
class Workflow:
    name: str
    rules: List[Rule]

    def run_for_part(self, part: Part) -> str:
        for rule in self.rules:
            if rule.matches(part):
                return rule.result

    def run_for_ranges(self, ranges: Ranges) -> List[Tuple[Ranges, str]]:
        result = []
        for rule in self.rules:
            # last rule matched
            if not rule.has_condition:
                result.append((ranges, rule.result))
                break

            # rule matched whole range
            if rule.matches_whole(ranges):
                result.append((ranges, rule.result))
                break

            # rule not matched whole range
            if rule.not_matches_whole(ranges):
                continue

            # rule splits range
            matched_ranges, non_matched_ranges = rule.split(ranges)
            result.append((matched_ranges, rule.result))
            ranges = non_matched_ranges

        return result


def main(debug: bool) -> None:
    input_data = load_data(debug)

    workflows, parts = parse_input(input_data)
    print(len(workflows), "workflows read")
    print(len(parts), "parts read")

    result_part1 = solve_part1(parts, workflows)
    result_part2 = solve_part2(workflows)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> Tuple[Dict[str, Workflow], List[Part]]:
    workflows_str, parts_str = input_data.strip().split("\n\n")

    workflows = parse_workflows(workflows_str)
    parts = parse_parts(parts_str)

    return workflows, parts


def parse_workflows(workflows_str: str) -> Dict[str, Workflow]:
    workflows = {}
    for line in workflows_str.splitlines():
        m = re.match(r"([a-z]+){(.*)}", line)
        workflow_name = m.group(1)
        rules_str = m.group(2)
        rules = []
        for rule_str in rules_str.split(","):
            if rule_m := re.match(r"([a-z])(.)(\d+):([^,]+)", rule_str):
                prop = rule_m.group(1)
                op_str = rule_m.group(2)
                val = int(rule_m.group(3))
                result = rule_m.group(4)
                rules.append(Rule(result, prop, op_str, val))
            else:
                rules.append(Rule(rule_str))
        workflow = Workflow(workflow_name, rules)
        workflows[workflow_name] = workflow
    return workflows


def parse_parts(parts_str: str) -> List[Part]:
    parts = []
    for part_str in parts_str.splitlines():
        ratings = {}
        for prop_m in re.finditer(r"([a-z])=(\d+)", part_str):
            ratings[prop_m.group(1)] = int(prop_m.group(2))
        parts.append(Part(ratings))
    return parts


def solve_part1(parts: List[Part], workflows: Dict[str, Workflow]) -> int:
    accepted_parts = []

    for part in parts:
        workflow = workflows["in"]
        while True:
            result = workflow.run_for_part(part)
            if result == ACCEPT:
                accepted_parts.append(part)
                break
            elif result == REJECT:
                break
            else:
                workflow = workflows[result]

    return sum([part.score() for part in accepted_parts])


def solve_part2(workflows: Dict[str, Workflow]) -> int:
    accepted_ranges = []

    work = [(Ranges({p: Range(1, 4000) for p in ["x", "m", "a", "s"]}), "in")]

    while work:
        ranges, workflow_name = work.pop()
        workflow = workflows[workflow_name]
        for ranges, result in workflow.run_for_ranges(ranges):
            if result == ACCEPT:
                accepted_ranges.append(ranges)
            elif result == REJECT:
                continue
            else:
                work.append((ranges, result))

    return sum([r.combinations() for r in accepted_ranges])


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
