import re
from collections import defaultdict, deque
import cProfile

class Factory:
    inventory_indexes = {'ore': 0, 'clay': 1, 'obsidian': 2, 'geode': 3}
    initial_state = (24, ((1, 0), (0, 0), (0, 0), (0, 0)))

    def time_remaining(state):
        return state[0]
    
    def inventory(state, rock_type):
        return state[1][Factory.inventory_indexes[rock_type]]

    def possible_materials(state):
        possible = set()
        for rock_type, idx in Factory.inventory_indexes.items():
            if state[1][idx][0] > 0:
                possible.add(rock_type)
        return possible


    def __init__(self, blueprint):
        self.blueprint = blueprint

        # Optimisation: Don't offer to make a robot type once we have enough to make any other bot in one step
        self.max_robots_needed = defaultdict(int)
        for details in blueprint.values():
            for material_type, material_quantity in details.items():
                self.max_robots_needed[material_type] = max(material_quantity, self.max_robots_needed[material_type])

    # What could we make next?
    ## List the (robot_type, time) for all robot types we can make
    ## Optimisation: Don't offer to make a robot type once we have enough to make any other bot in one step
    def choices(self, state):
        possible_materials = Factory.possible_materials(state)

        robots_and_times = []
        for robot_type, materials_needed in self.blueprint.items():
            if robot_type != 'geode':
                have_already, _ = Factory.inventory(state, robot_type)
                if have_already >= self.max_robots_needed[robot_type]:
                    continue
            
            if set(materials_needed.keys()).issubset(possible_materials):
                time_needed = 0
                for rock_type, quantity_needed in materials_needed.items():   
                    robot_count, material_stock = Factory.inventory(state, rock_type)
                    if quantity_needed > material_stock:
                        time_for_this_material = -((quantity_needed - material_stock) // -robot_count) # Ceiling division
                        time_needed = max(time_needed, time_for_this_material)
                time_needed += 1 # Time to make the robot once all materials are ready
                if time_needed <= Factory.time_remaining(state):
                    robots_and_times.append((robot_type, time_needed))
        return robots_and_times


    # Put in an order for a robot. We trust that this is one of the chocies().
    def make(self, robot_to_make, time_needed, state):
        new_robots_and_materials = []
        for rock_type in Factory.inventory_indexes.keys():
            robot_quantity, material_stock = Factory.inventory(state, rock_type)
            material_stock += (robot_quantity * time_needed)
            if rock_type in self.blueprint[robot_to_make]:
                material_stock -= self.blueprint[robot_to_make][rock_type]
            if rock_type == robot_to_make:
                robot_quantity += 1
            new_robots_and_materials.append((robot_quantity, material_stock))
        
        time_remaining = Factory.time_remaining(state) - time_needed
        return (time_remaining, tuple(new_robots_and_materials))
        

    def run_out_clock(self, state):
        new_robots_and_materials = []
        for rock_type in Factory.inventory_indexes.keys():
            robot_quantity, material_stock = Factory.inventory(state, rock_type)
            material_stock += (robot_quantity * Factory.time_remaining(state))
            new_robots_and_materials.append((robot_quantity, material_stock))
        return (0, tuple(new_robots_and_materials))


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


def geode_count(state):
    return Factory.inventory(state, 'geode')[1]
    

# Ask the factory to crack the most geodes it can.
def make_good_choices(factory):
    most_geodes = 0
    explored = {Factory.initial_state}
    queue = deque([Factory.initial_state])
    while queue:
        state = queue.popleft()
        next_moves = factory.choices(state)
        if len(next_moves) == 0:
            state = factory.run_out_clock(state)
            most_geodes = max(most_geodes, geode_count(state))

        for robot_to_make, time_needed in next_moves:
            option = factory.make(robot_to_make, time_needed, state)
            if option not in explored:
                explored.add(option)
                queue.append(option)
    return most_geodes

#--------------------- tests -------------------------#

def test_state():
    state = Factory.initial_state
    assert Factory.time_remaining(state) == 24
    assert Factory.inventory(state, 'ore') == (1, 0)
    assert Factory.possible_materials(state) == {'ore'}


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
    factory = Factory(blueprint)
    assert factory.max_robots_needed == {
        'ore': 4,
        'clay': 14,
        'obsidian': 7
    }
    assert factory.choices(Factory.initial_state) == [('ore', 5), ('clay', 3)]


def test_make_robot():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint)
    state = factory.make('clay', 3, Factory.initial_state)
    assert state == (21, ((1, 1), (1, 0), (0, 0), (0, 0)))


def test_example_factory_run():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint)
    state = Factory.initial_state
    assert ('clay', 3) in factory.choices(state)
    state = factory.make('clay', 3, state)
    assert ('clay', 2) in factory.choices(state)
    state = factory.make('clay', 2, state)
    assert ('clay', 2) in factory.choices(state)
    state = factory.make('clay', 2, state)

    assert state == (17, ((1, 1), (3, 6), (0, 0), (0, 0))) # Minute 7
    assert ('obsidian', 4) in factory.choices(state)
    state = factory.make('obsidian', 4, state)
    assert ('clay', 1) in factory.choices(state)
    state = factory.make('clay', 1, state)
    assert ('obsidian', 3) in factory.choices(state)
    state = factory.make('obsidian', 3, state)
    assert ('geode', 3) in factory.choices(state)
    state = factory.make('geode', 3, state)

    assert state[0] == 6 # Minute 18
    assert ('geode', 3) in factory.choices(state)
    state = factory.make('geode', 3, state)
    state = factory.run_out_clock(state)
    assert geode_count(state) == 9

# Runs for lower 'time_remaining' values (up to 18 is very fast, then gets slower and slower)
def test_make_good_choices():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint)
    assert make_good_choices(factory) == 9

#-----------------------------------------------------#

def foo():
    blueprints = fetch_data('sample_data/day19.txt')
    id, blueprint = next(blueprints)
    factory = Factory(blueprint)
    print(f'Geodes: {make_good_choices(factory)}')

if __name__ == "__main__":
    cProfile.run('foo()', sort='cumulative')
