import re
from collections import defaultdict, deque
import copy

class Factory:
    def __init__(self, blueprint, time_remaining):
        self.blueprint = blueprint
        self.time_remaining = time_remaining
        self.robots = defaultdict(int, {'ore': 1})
        self.materials = defaultdict(int)

    def __hash__(self):
        return hash((self.time_remaining, repr(self.robots), repr(self.materials)))

    def __eq__(self, other):
        return self.time_remaining == other.time_remaining and repr(self.robots) == repr(other.robots) and repr(self.materials) == repr(other.materials)

    # What could we make next?
    def choices(self):
        robots_and_times = []
        possible_materials = set(self.robots.keys())
        for robot_type, materials_needed in self.blueprint.items():
            if set(materials_needed.keys()).issubset(possible_materials):
                time_needed = 0
                for material_type, quantity_needed in materials_needed.items():   
                    got_in_stock = self.materials[material_type]
                    if quantity_needed > got_in_stock:
                        time_for_this_material = -((quantity_needed - got_in_stock) // -self.robots[material_type]) # Ceiling division
                        time_needed = max(time_needed, time_for_this_material)
                time_needed += 1 # Time to make the robot once all materials are ready
                if time_needed <= self.time_remaining:
                    robots_and_times.append((robot_type, time_needed))
        return robots_and_times

    # Put in an order for a robot. We trust that this is one of the chocies().
    def make(self, robot_to_make, time_needed):
        for robot_type, robot_quantity in self.robots.items():
            self.materials[robot_type] += (robot_quantity * time_needed)
        for material_type, quantity_needed in self.blueprint[robot_to_make].items():
            self.materials[material_type] -= quantity_needed
        self.time_remaining -= time_needed
        self.robots[robot_to_make] += 1

    def run_out_clock(self):
        for robot_type, robot_quantity in self.robots.items():
            self.materials[robot_type] += (robot_quantity * self.time_remaining)
        self.time_remaining = 0


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            m = re.match(r'Blueprint (\d+):', ln)
            id = int(m[1])
            details = dict()
            for robot_type, materials_needed in re.findall(r'Each (\w+) robot costs (.+?)\.', ln):
                details[robot_type] = dict()
                for quantity, material_type in re.findall(r'(\d+) (ore|clay|obsidian)', materials_needed):
                    details[robot_type][material_type] = int(quantity)
            yield id, details


# Ask the factory to crack the most geodes it can.
def make_good_choices(initial_factory):
    most_geodes = 0
    explored = {initial_factory}
    queue = deque([initial_factory])
    while queue:
        factory = queue.popleft()
        next_moves = factory.choices()
        if len(next_moves) == 0:
            factory.run_out_clock()
            most_geodes = max(most_geodes, factory.materials['geode'])

        for robot_to_make, time_needed in next_moves:
            option = copy.deepcopy(factory)
            option.make(robot_to_make, time_needed)
            if option not in explored:
                explored.add(option)
                queue.append(option)
    return most_geodes

#--------------------- tests -------------------------#

def test_fetch_data():
    blueprints = fetch_data('sample_data/day19.txt')
    assert next(blueprints) == (1, {
        'ore': {'ore': 4},
        'clay': {'ore': 2},
        'obsidian': {'ore': 3, 'clay': 14},
        'geode': {'ore': 2, 'obsidian': 7}
    })

    assert next(blueprints) == (2, {
        'ore': {'ore': 2},
        'clay': {'ore': 3},
        'obsidian': {'ore': 3, 'clay': 8},
        'geode': {'ore': 3, 'obsidian': 12}
    })

def test_factory_initialisation():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint, 24)
    assert factory.robots == {'ore': 1}
    assert factory.materials == {}
    assert factory.choices() == [('ore', 5), ('clay', 3)]

def test_make_robot():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint, 24)
    factory.make('clay', 3)
    assert factory.robots == {'ore': 1, 'clay': 1}
    assert factory.materials == {'ore': 1}
    assert factory.time_remaining == 21

def test_copy_factory():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint, 24)
    factory2 = copy.deepcopy(factory)
    factory2.make('clay', 3)
    assert factory.robots == {'ore': 1}
    assert factory2.robots == {'ore': 1, 'clay': 1}

def test_example_factory_run():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint, 24)
    assert ('clay', 3) in factory.choices()
    factory.make('clay', 3)
    assert ('clay', 2) in factory.choices()
    factory.make('clay', 2)
    assert ('clay', 2) in factory.choices()
    factory.make('clay', 2)

    assert factory.time_remaining == 17 # Minute 7
    assert factory.materials == {'ore': 1, 'clay': 6}
    assert factory.robots == {'ore': 1, 'clay': 3}
    assert ('obsidian', 4) in factory.choices()
    factory.make('obsidian', 4)
    assert ('clay', 1) in factory.choices()
    factory.make('clay', 1)
    assert ('obsidian', 3) in factory.choices()
    factory.make('obsidian', 3)
    assert ('geode', 3) in factory.choices()
    factory.make('geode', 3)

    assert factory.time_remaining == 6 # Minute 18
    assert ('geode', 3) in factory.choices()
    factory.make('geode', 3)
    factory.run_out_clock()
    assert factory.materials['geode'] == 9



def __test_make_good_choices():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint, 24)
    assert make_good_choices(factory) == 9

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day19.txt')
    print('Hello, World!')
