import re

class Factory:
    def __init__(self, blueprint):
        self.blueprint = blueprint



def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            m = re.match(r'Blueprint (\d+):', ln)
            id = int(m[1])
            details = dict()
            for robot_type, costs in re.findall(r'Each (\w+) robot costs (.+?)\.', ln):
                details[robot_type] = dict()
                for amount, material_type in re.findall(r'(\d+) (ore|clay|obsidian)', costs):
                    details[robot_type][material_type] = int(amount)
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


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day19.txt')
    print('Hello, World!')
