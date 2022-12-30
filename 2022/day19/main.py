import math
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from functools import lru_cache
from typing import Dict

from tqdm import tqdm


class Resource(Enum):
    GEODE = auto()
    OBSIDIAN = auto()
    CLAY = auto()
    ORE = auto()

    def __str__(self):
        return self.name


@dataclass
class State:
    robots: Dict[Resource, int]
    resources: Dict[Resource, int]

    def copy(self):
        return State(self.robots.copy(), self.resources.copy())

    def __str__(self):
        resources_str = ""
        robots_str = ""
        for resource in Resource:
            resources_str += f"{resource}: {str(self.resources[resource])} "
            robots_str += f"{resource}: {str(self.robots[resource])} "
        return f"Resources: {resources_str} | Robots: {robots_str}"

    def __hash__(self):
        return hash(str(self))


@dataclass
class Blueprint:
    id: int
    robot_costs: Dict

    def __hash__(self):
        return hash(id)


@lru_cache(maxsize=None)
def robot_type_to_time(
    blueprint: Blueprint, state: State, minutes_left: int
) -> Dict[Resource, int]:
    result = {}
    for robot_type in Resource:
        resources = state.resources.copy()
        minutes = 0
        for resource, resource_needed in blueprint.robot_costs[robot_type].items():
            resources_present = resources[resource]
            robots_present = state.robots[resource]
            if resources_present < resource_needed and robots_present != 0:
                missing_resources = resource_needed - resources_present
                minutes_wait = math.ceil(missing_resources / robots_present)
                minutes += minutes_wait
                for r, robot_count in state.robots.items():
                    resources[r] += minutes_wait * robot_count
        if minutes >= minutes_left:
            continue
        can_be_build = True
        for resource, resource_needed in blueprint.robot_costs[robot_type].items():
            if resources[resource] < resource_needed:
                can_be_build = False
                break
        if can_be_build:
            result[robot_type] = minutes

    return result


@lru_cache(maxsize=None)
def max_reachable_resource(
    blueprint: Blueprint,
    state: State,
    resource: Resource,
    minutes_left: int,
    current_max: int,
) -> int:
    if minutes_left == 0:
        return state.resources[resource]

    robot_type_to_minutes = robot_type_to_time(blueprint, state, minutes_left)
    if not robot_type_to_minutes:
        state.resources[resource] += minutes_left * state.robots[resource]
        return state.resources[resource]

    for robot_type, minutes in robot_type_to_minutes.items():
        new_state = state.copy()

        # collect resources after minutes passed
        for r in Resource:
            new_state.resources[r] += (1 + minutes) * state.robots[r]

        # build robot
        for r, cost in blueprint.robot_costs[robot_type].items():
            new_state.resources[r] -= cost
        new_state.robots[robot_type] += 1

        new_minutes = minutes_left - minutes - 1

        # check if possible to get better score
        potential_score = (
            new_state.resources[resource]  # current inventory
            + new_state.robots[resource]
            * new_minutes  # current robots output until end
            + max(0, new_minutes * (new_minutes - 1) // 2)  # if we build one each turn
        )
        if potential_score <= current_max:
            continue

        score = max_reachable_resource(
            blueprint, new_state, resource, new_minutes, current_max
        )
        current_max = max(current_max, score)

    return current_max


def solve(blueprint: Blueprint, minutes: int) -> int:
    robots = defaultdict(int)
    robots[Resource.ORE] += 1
    state = State(robots=robots, resources=defaultdict(int))
    return max_reachable_resource(
        blueprint, state, Resource.GEODE, minutes_left=minutes, current_max=0
    )


def main():
    blueprints = read_blueprints()
    print(len(blueprints), "blueprints parsed")

    result_part1 = 0
    minutes = 24
    for blueprint in tqdm(blueprints):
        max_reachable_resource.skipped = 0
        score = solve(blueprint, minutes)
        result_part1 += score * blueprint.id
        max_reachable_resource.cache_clear()
        robot_type_to_time.cache_clear()

    result_part2 = 1
    minutes = 32
    for blueprint in tqdm(blueprints[:3]):
        max_reachable_resource.skipped = 0
        score = solve(blueprint, minutes)
        result_part2 *= score
        max_reachable_resource.cache_clear()
        robot_type_to_time.cache_clear()

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")  # Expected sample: 33, expected full: 1127
    print(
        f"Result part 2: {result_part2}"
    )  # Expected sample: 3472, expected full: 21546


def read_blueprints():
    blueprints = []
    with open("input.txt") as f:
        for line in f.readlines():
            m = re.match(
                r"Blueprint (\d+): Each ore robot costs (\d+) ore. "
                r"Each clay robot costs (\d+) ore. "
                r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
                r"Each geode robot costs (\d+) ore and (\d+) obsidian.",
                line.strip(),
            )
            blueprint_id = int(m.group(1))
            ore_robot_cost = {Resource.ORE: int(m.group(2))}
            clay_robot_cost = {Resource.ORE: int(m.group(3))}
            obsidian_robot_cost = {
                Resource.ORE: int(m.group(4)),
                Resource.CLAY: int(m.group(5)),
            }
            geode_robot_cost = {
                Resource.ORE: int(m.group(6)),
                Resource.OBSIDIAN: int(m.group(7)),
            }
            robot_costs = {
                Resource.ORE: ore_robot_cost,
                Resource.CLAY: clay_robot_cost,
                Resource.OBSIDIAN: obsidian_robot_cost,
                Resource.GEODE: geode_robot_cost,
            }
            blueprints.append(Blueprint(blueprint_id, robot_costs))
    return blueprints


if __name__ == "__main__":
    main()
