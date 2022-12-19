import multiprocessing as mp
import re
import time
from dataclasses import dataclass
from enum import Enum

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

class Resource(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4

@dataclass(frozen=True)
class Recipe:
    result: Resource
    ore_count: int
    clay_count: int
    obsidian_count: int

class State:
    def __init__(self, robots, resources):
        self.robots = robots
        self.resources = resources

    def __repr__(self) -> str:
        return f"State(robots={self.robots!r}, resources={self.resources!r})"

    def __eq__(self, other):
        return self.robots == other.robots and self.resources == other.resources

    def __hash__(self):
        return hash((
            self.robots[Resource.ORE],
            self.robots[Resource.CLAY],
            self.robots[Resource.OBSIDIAN],
            self.robots[Resource.GEODE],
            self.resources[Resource.ORE],
            self.resources[Resource.CLAY],
            self.resources[Resource.OBSIDIAN],
            self.resources[Resource.GEODE],
        ))

    def step(self, blueprint):
        for recipe in blueprint:
            if self.resources[Resource.ORE] >= recipe.ore_count and \
                    self.resources[Resource.CLAY] >= recipe.clay_count and \
                    self.resources[Resource.OBSIDIAN] >= recipe.obsidian_count:

                new_robots = self.robots.copy()
                new_robots[recipe.result] += 1
                yield State(new_robots, self.incr({
                    Resource.ORE:       self.resources[Resource.ORE] - recipe.ore_count,
                    Resource.CLAY:      self.resources[Resource.CLAY] - recipe.clay_count,
                    Resource.OBSIDIAN:  self.resources[Resource.OBSIDIAN] - recipe.obsidian_count,
                    Resource.GEODE:     self.resources[Resource.GEODE],
                }))
        yield State(self.robots, self.incr(self.resources))

    def incr(self, resources):
        return {
            Resource.ORE:       resources[Resource.ORE] + self.robots[Resource.ORE],
            Resource.CLAY:      resources[Resource.CLAY] + self.robots[Resource.CLAY],
            Resource.OBSIDIAN:  resources[Resource.OBSIDIAN] + self.robots[Resource.OBSIDIAN],
            Resource.GEODE:     resources[Resource.GEODE] + self.robots[Resource.GEODE],
        }

    def geode_count(self):
        return self.resources[Resource.GEODE]


blueprints = []
for line in parse_input():
    _blueprint = []
    nums = [int(x) for x in re.findall(r"\d+", line)[1:]]
    _blueprint.append(Recipe(Resource.ORE, nums[0], 0, 0))
    _blueprint.append(Recipe(Resource.CLAY, nums[1], 0, 0))
    _blueprint.append(Recipe(Resource.OBSIDIAN, nums[2], nums[3], 0))
    _blueprint.append(Recipe(Resource.GEODE, nums[4], 0, nums[5]))
    blueprints.append(_blueprint)


def evaluate_blueprint(blueprint, step_count, print_progress=False) -> int:
    initial_state = State(
        {Resource.ORE: 1, Resource.CLAY: 0, Resource.OBSIDIAN: 0, Resource.GEODE: 0},
        {Resource.ORE: 0, Resource.CLAY: 0, Resource.OBSIDIAN: 0, Resource.GEODE: 0},
    )
    states = [initial_state]
    seen_states = set((initial_state,))
    for i in range(1, step_count + 1):
        new_states = []
        most_geodes = 0
        for state in states:
            for new_state in state.step(blueprint):
                if new_state not in seen_states:
                    seen_states.add(new_state)
                    new_states.append(new_state)
                    most_geodes = max(most_geodes, new_state.geode_count())

        states = [state for state in new_states if state.geode_count() >= most_geodes]
        # sort states with key lambda equal to sum of all values in state and prune excess
        # * place to optimize
        states = sorted(states,
                        key=lambda state: sum(
                            state.robots.values()) + sum(state.resources.values()),
                        reverse=True)[-100000:]
        if print_progress:
            print(
            f"After minute {i}: {len(states):,} state(s) to consider. Most geodes: {most_geodes}."
            )
    return most_geodes

#! Deprecated
def __part_1():
    result = 0
    for i, _blueprint in enumerate(blueprints, start=1):
        print(f"Blueprint #{i}...")
        most_geodes = evaluate_blueprint(_blueprint, 24, print_progress=True)
        print()
        result += i * most_geodes
    print(f"Part one: {result}\n")

#! Deprecated
def __part_2():
    blueprints_2 = blueprints[:3]
    print("================= Part Two =================")
    result = 1
    for i, _blueprint in enumerate(blueprints_2, start=1):
        print(f"Blueprint #{i}...")
        most_geodes = evaluate_blueprint(_blueprint, 32, print_progress=True)
        print()
        result *= most_geodes
    print(f"Part two: {result}")


def part_1():
    final_result = 0
    with mp.Pool(processes=len(blueprints)) as pool:
        results = []
        for b in blueprints:
            results.append(pool.apply_async(evaluate_blueprint, (b, 24)))

        answer = 0
        for i, result in enumerate(results, start=1):
            score = result.get()
            answer += score
            print(f"Blueprint #{i} score: {score}")
            final_result += i * score
    print(f"Final result: {final_result}")

def part_2():
    final_result = 1
    with mp.Pool(processes=3) as pool:
        results = []
        for b in blueprints[:3]:
            results.append(pool.apply_async(evaluate_blueprint, (b, 32)))
        for result in results:
            final_result *= result.get()
    print(f"Final result: {final_result}")


if __name__ == "__main__":
    start_time = time.time()
    part_1()
    part_1_time = time.time()
    print(f"Part one took {part_1_time - start_time:.2f} seconds.")
    part_2()
    part_2_time = time.time()
    print(f"Part two took {part_2_time - part_1_time:.2f} seconds.")
