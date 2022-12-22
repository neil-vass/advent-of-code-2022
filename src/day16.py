from collections import namedtuple
from collections import deque
from pprint import pprint
import re

Move = namedtuple("Move", "target cost value")

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


    def _choose_path(self, time_remaining, start_valve):

        current_valve = start_valve
        routes_and_costs = self._routes_and_costs()
        valves_and_rates = self._valves_and_rates()
        release_by_end = 0

        # Strategy 1: Go for the highest-value valve, wherever it is?
        # Works for very simple volcanos.
        # With sample data, this gets to 1595, best is 1651. 
        while True:
            # Generate options
            preferred_move = None
            for target_valve, rate in valves_and_rates:
                cost_for_this_move = routes_and_costs[current_valve][target_valve]
                if cost_for_this_move <= time_remaining:
                    value_for_this_move = rate * (time_remaining - cost_for_this_move)
                    if preferred_move is None or preferred_move.value < value_for_this_move:
                        preferred_move = Move(target_valve, cost_for_this_move, value_for_this_move)

            if preferred_move is None:
                break

            # Take move
            current_valve = preferred_move.target
            time_remaining -= preferred_move.cost
            release_by_end += preferred_move.value
            valves_and_rates = [(v,r) for v,r in valves_and_rates if v != current_valve]
            print(preferred_move)
        
        return release_by_end

    def _best_path_from(self, time_remaining, current_valve, routes_and_costs, valves_and_rates, release_by_end=0):
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

        if possible_moves:
            return max(possible_moves)
        else:
            return 0




    def _choose_path_v2(self, time_remaining, start_valve):
        # Strategy 2: A search of all paths, return the best choice.
        # Might take a while, let's see...
        current_valve = start_valve
        routes_and_costs = self._routes_and_costs()
        valves_and_rates = self._valves_and_rates()
        release_by_end = 0

        return self._best_path_from(time_remaining, start_valve, routes_and_costs, valves_and_rates)

        

    def most_pressure_in(self, minutes):
        return self._choose_path_v2(time_remaining=minutes, start_valve='AA')


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

#-----------------------------------------------------#

if __name__ == "__main__":
    volcano = fetch_data('data/day16.txt')
    print(volcano.most_pressure_in(30))
    


# Or is it better to leave it (and maybe come back to it later?)
# So we could consider all paths from here (from now until time runs out, or all valves turned)
# Consider them "if I turn this now", and also "if I leave this now"
# wow

# Or ... 
# Redo the map so we move directly to where we're turning something. 
# Include the time to turn on valve in the "time to make that move" calculation.
# Never be stood in front of a valve deciding whether to turn it on, we've either 
# moved here to turn it, or we've run right past it.

# A table of: where we could step to, and what the cost / gain would be, given our 
# location and the time remaining.
# Global hash table so we can look it up in future, only calcualte new values when we 
# need to.
# That might get too big and slow - but it's a start!