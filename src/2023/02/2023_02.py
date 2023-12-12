import dataclasses
import enum
import operator
import re
from collections import defaultdict
from functools import reduce
from typing import List

from src.utils.data import load_data
from src.utils.submission import submit_or_print


class Color(enum.Enum):
    RED = enum.auto()
    GREEN = enum.auto()
    BLUE = enum.auto()


@dataclasses.dataclass
class Pull:
    counts: dict[Color, int]


@dataclasses.dataclass
class Game:
    game_id: int
    pulls: List[Pull]

    def possible(self, start_counts: dict[Color, int]) -> bool:
        for pull in self.pulls:
            for color, count in pull.counts.items():
                if start_counts[color] < count:
                    return False
        return True

    def power(self) -> int:
        min_counts = defaultdict(int)
        for pull in self.pulls:
            for color, count in pull.counts.items():
                min_counts[color] = max(min_counts[color], count)
        return reduce(operator.mul, min_counts.values())


def parse_games(input_data: str) -> List[Game]:
    games = []

    for line in input_data.split("\n"):
        if not line:
            continue
        game_id = int(re.match(r"^Game (\d+)", line).group(1))
        pulls_str = [p.strip() for p in re.split(r"[:;]", line)[1:]]
        pulls = []
        for pull_str in pulls_str:
            counts = {}
            for match in re.finditer(r"(\d+) ([a-z]+)", pull_str):
                color = Color[match.group(2).upper()]
                count = int(match.group(1))
                counts[color] = count
            pull = Pull(counts=counts)
            pulls.append(pull)

        games.append(Game(game_id=game_id, pulls=pulls))

    return games


def main(debug: bool) -> None:
    input_data = load_data(debug)

    games = parse_games(input_data)
    print(f"{len(games)} games parsed.")

    # part 1
    start = {Color.RED: 12, Color.GREEN: 13, Color.BLUE: 14}
    possible_games = [g for g in games if g.possible(start)]
    result_part1 = reduce(operator.add, map(lambda g: g.game_id, possible_games), 0)

    # part 2
    result_part2 = reduce(operator.add, map(lambda g: g.power(), games), 0)

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
