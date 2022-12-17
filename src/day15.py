import re

class Sensor:
    def __init__(self, sensor_x, sensor_y, beacon_x, beacon_y):
        self.position = (sensor_x, sensor_y)
        self.closest_beacon = (beacon_x, beacon_y)

    def cannot_be_beacons_for_row(self, row):
        sensor_x, sensor_y = self.position
        dist_to_beacon = (abs(sensor_x - self.closest_beacon[0]) + 
                abs(sensor_y - self.closest_beacon[1]))

        dist_to_target_row = abs(sensor_y - row)

        no_beacons = set()
        for x in range(dist_to_beacon - dist_to_target_row + 1):
            no_beacons |= {(sensor_x + x, row), (sensor_x - x, row)}

        return no_beacons - {self.position, self.closest_beacon}


    def rule_out(self, possible_locations):
        sensor_x, sensor_y = self.position
        dist_to_beacon = (abs(sensor_x - self.closest_beacon[0]) + 
                abs(sensor_y - self.closest_beacon[1]))

        return {(x,y) for x,y in possible_locations 
                if (abs(sensor_x - x) + abs(sensor_y - y)) > dist_to_beacon}
    


def fetch_data(path):
    with open(path, 'r') as f:
        sensors = []
        for ln in f:
            values = [int(n) for n in re.findall(r'-?\d+', ln)]
            sensors.append(Sensor(*values))
        return sensors

def count_no_beacon_positions_for_row(sensors, row):
    positions = set()
    for sensor in sensors:
        positions |= sensor.cannot_be_beacons_for_row(row)
    return len(positions)

def find_distress_beacon(sensors, max_x, max_y):
   
    possible_locations = {(x,y) for x in range(max_x+1) for y in range(max_y+1)}
    for sensor in sensors:
        possible_locations = sensor.rule_out(possible_locations)
    return list(possible_locations)[0]


#--------------------- tests -------------------------#

def test_sensor_init():
    sensor = Sensor(2,18, -2,15)
    assert sensor.position == (2, 18)
    assert sensor.closest_beacon == (-2, 15)

def test_cannot_be_beacons_for_row():
    sensor = Sensor(8,7, 2,10)
    no_beacons = sensor.cannot_be_beacons_for_row(10)
    assert len(no_beacons) == 12

def test_fetch_data():
    sensors = fetch_data('sample_data/day15.txt')
    assert len(sensors) == 14
    assert sensors[0].position == (2,18)
    assert sensors[-1].closest_beacon == (15,3)

def test_count_no_beacon_positions_for_row():
    sensors = fetch_data('sample_data/day15.txt')
    assert count_no_beacon_positions_for_row(sensors, row=10) == 26

def test_rule_out():
    sensor = Sensor(0,0, 1,0)
    max_x = max_y = 1
    possible_locations = {(x,y) for x in range(max_x+1) for y in range(max_y+1)}
    assert sensor.rule_out(possible_locations) == {(1,1)}

def test_find_distress_beacon():
    sensors = fetch_data('sample_data/day15.txt')
    assert find_distress_beacon(sensors, 20, 20) == (14, 11)

#-----------------------------------------------------#

if __name__ == "__main__":
    sensors = fetch_data('data/day15.txt')
    print(find_distress_beacon(sensors, 4000000, 4000000))
