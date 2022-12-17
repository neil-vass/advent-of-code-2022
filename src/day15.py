import re
from tqdm import tqdm

class Sensor:
    def __init__(self, sensor_x, sensor_y, beacon_x, beacon_y):
        self.position = (sensor_x, sensor_y)
        self.closest_beacon = (beacon_x, beacon_y)
        self._dist_to_beacon = (abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y))

    def cannot_be_beacons_for_row(self, row):
        sensor_x, sensor_y = self.position
        dist_to_target_row = abs(sensor_y - row)

        no_beacons = set()
        for x in range(self._dist_to_beacon - dist_to_target_row + 1):
            no_beacons |= {(sensor_x + x, row), (sensor_x - x, row)}

        return no_beacons - {self.position, self.closest_beacon}

    def no_beacons_range_for_row(self, row):
        sensor_x, sensor_y = self.position
        dist_to_target_row = abs(sensor_y - row)
        x_extent = self._dist_to_beacon - dist_to_target_row
        if x_extent >= 0:
            return (sensor_x - x_extent), (sensor_x + x_extent)


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
    for y in tqdm(range(max_y+1)):
        ranges = (sensor.no_beacons_range_for_row(y) for sensor in sensors)
        ranges = sorted(r for r in ranges if r is not None)

        left_edge = right_edge = None
        for left_for_this_sensor, right_for_this_sensor in ranges:
            if left_edge is None:
                left_edge, right_edge = left_for_this_sensor, right_for_this_sensor
            else:
                if (right_edge +1) < left_for_this_sensor <= max_x:
                    return right_edge +1, y
                else:
                    right_edge = max(right_edge, right_for_this_sensor)
                    if left_edge < 0 and right_edge > max_x:
                        break


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

def test_no_beacons_range_for_row():
    sensor = Sensor(8,7, 2,10)
    assert sensor.no_beacons_range_for_row(-2) == (8, 8)
    assert sensor.no_beacons_range_for_row(10) == (2, 14)
    assert sensor.no_beacons_range_for_row(18) is None

def test_find_distress_beacon():
    sensors = fetch_data('sample_data/day15.txt')
    assert find_distress_beacon(sensors, 20, 20) == (14, 11)

#-----------------------------------------------------#

if __name__ == "__main__":
    sensors = fetch_data('data/day15.txt')
    x, y = find_distress_beacon(sensors, 4000000, 4000000)
    print(x*4000000 + y)
