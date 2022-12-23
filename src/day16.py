from itertools import chain, combinations
from collections import deque
from tqdm import tqdm
import re

class Valve:
    def __init__(self, id, flow_rate, tunnels):
        self.id = id
        self.flow_rate = flow_rate
        self.tunnels = tunnels

class Volcano:
    def __init__(self):
        self.valves = {}

    def add(self, valve):
        self.valves[valve.id] = valve
        
    def _routes_and_costs(self):
        targets = [k for k,v in self.valves.items() if v.flow_rate]
        starts = ['AA'] + targets[:]
        routes_and_costs = dict()

        for start in starts:
            routes_and_costs[start] = dict()
            for target in targets:
                # Depth first search to target
                explored = {start}
                queue = deque([(start, 0)])
                while queue: 
                    v, path_length = queue.popleft()
                    if v == target:
                        routes_and_costs[start][v] = path_length +1
                        break
                    for neighbour in self.valves[v].tunnels:
                        if neighbour not in explored:
                            explored.add(neighbour)
                            queue.append((neighbour, path_length +1))
        return routes_and_costs

    def _valves_and_rates(self):
        valves_and_rates = [(k, v.flow_rate) for k,v in self.valves.items() if v.flow_rate]
        return sorted(valves_and_rates, key=lambda x: x[1])


    def _best_path_from(self, time_remaining, current_valve, routes_and_costs, valves_and_rates, release_by_end=0, already_calculated=None):
        if already_calculated is None:
            already_calculated = dict()
            
        possible_moves = []
        for target_valve, rate in valves_and_rates:
                cost_for_this_move = routes_and_costs[current_valve][target_valve]
                if cost_for_this_move <= time_remaining:
                    value_for_this_move = rate * (time_remaining - cost_for_this_move)
                    value_for_this_move += self._best_path_from(
                        time_remaining=time_remaining - cost_for_this_move,
                        current_valve= target_valve,
                        routes_and_costs= routes_and_costs,
                        valves_and_rates= [(v,r) for v,r in valves_and_rates if v not in (current_valve, target_valve)],
                        release_by_end= release_by_end + value_for_this_move
                    )
                    possible_moves.append(value_for_this_move)

        return max(possible_moves, default=0)


    def most_pressure_in(self, minutes):
        return self._best_path_from(minutes, 'AA', self._routes_and_costs(), self._valves_and_rates())


    def most_pressure_with_elephant(self, minutes):
        # An idea: Agree at the start which valves you'll each go for!
        # Calculate the max release for all subsets of valves turned
        # Pick the 2 disjoint sets that have the highest total pressure
        routes_and_costs = self._routes_and_costs()
        valves_and_rates = self._valves_and_rates()
        powerset = list(chain.from_iterable(combinations(valves_and_rates, i) for i in range(1, len(valves_and_rates))))

        progressbar = tqdm(desc='Best paths', total=sum(len(s) for s in powerset))
        choices = []
        for subset_of_valves_and_rates in powerset:
            max_release = self._best_path_from(minutes, 'AA', routes_and_costs, subset_of_valves_and_rates)
            choice = (set(v for v,r in subset_of_valves_and_rates), max_release)
            choices.append(choice)
            progressbar.update(len(subset_of_valves_and_rates))
        progressbar.close()

        progressbar = tqdm(desc='Best pair', total=(len(choices)*(len(choices)+1)//2))
        best_combo = 0
        for a in range(len(choices)):
            valves_a, max_release_a = choices[a]
            for b in range(a+1, len(choices)):
                valves_b, max_release_b = choices[b]
                if valves_a.isdisjoint(valves_b):
                    best_combo = max(best_combo, max_release_a + max_release_b)
                progressbar.update()
        progressbar.close()
        return best_combo


def fetch_data(path):
    volcano = Volcano()
    with open(path, 'r') as f:
        for ln in f:
            m = re.match(r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.+)$', ln)
            volcano.add(Valve(
                id = m[1],
                flow_rate = int(m[2]),
                tunnels = m[3].split(', ')
            ))
    return volcano

#--------------------- tests -------------------------#

def test_fetch_data():
    volcano = fetch_data('sample_data/day16.txt')
    assert len(volcano.valves) == 10
    assert volcano.valves['BB'].flow_rate == 13
    assert volcano.valves['II'].tunnels == ['AA', 'JJ']

def test_simple_routes_and_costs():
    sut = Volcano()
    sut.add(Valve('AA', 0, ['BB']))
    sut.add(Valve('BB', 13, ['AA']))  
    assert sut._routes_and_costs() == {
        'AA': {'BB': 2}, 'BB': {'BB': 1}
    } 

def test_routes_and_costs():
    volcano = fetch_data('sample_data/day16.txt')
    routes = volcano._routes_and_costs()
    assert len(routes) == 7
    assert routes['AA']['JJ'] == 3 # Can go AA->II->JJ, then a minute to turn on

def test_simple_volcano_pressure():
    sut = Volcano()
    sut.add(Valve('AA', 0, ['BB']))
    sut.add(Valve('BB', 13, ['AA']))
    assert sut.most_pressure_in(minutes=30) == 364

def test_volcano_pressure():
    volcano = fetch_data('sample_data/day16.txt')
    assert volcano.most_pressure_in(minutes=30) == 1651

def test_volcano_pressure_with_elephant():
    volcano = fetch_data('sample_data/day16.txt')
    assert volcano.most_pressure_with_elephant(minutes=26) == 1707

#-----------------------------------------------------#

if __name__ == "__main__":
    volcano = fetch_data('data/day16.txt')
    print(volcano.most_pressure_with_elephant(26))
    
