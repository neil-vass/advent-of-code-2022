import re
from collections import defaultdict

class Factory:
    def __init__(self, blueprint, time_remaining):
        self.blueprint = blueprint
        self.time_remaining = time_remaining
        self.robots = {'ore': 1}
        self.materials = defaultdict(int)

    # What could we make next?
    def choices(self):
        possible_materials = set(self.robots.keys())
        for robot_type, materials_needed in self.blueprint.items():
            if set(materials_needed.keys()).issubset(possible_materials):
                time_needed = 1
                for material_type, quantity_needed in materials_needed.items():   
                    got_in_stock = self.materials[material_type]
                    if quantity_needed > got_in_stock:
                        time_needed += (quantity_needed - got_in_stock) // self.robots[material_type] 
                if time_needed <= self.time_remaining:
                    yield (robot_type, time_needed)



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
    assert list(factory.choices()) == [('ore', 5), ('clay', 3)]


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day19.txt')
    print('Hello, World!')
