
class Sensor:
    def __init__(self, sensor_x, sensor_y, beacon_x, beacon_y):
        self.position = (sensor_x, sensor_y)
        self.closest_beacon = (beacon_x, beacon_y)

    def cannot_be_beacons(self):
        sensor_x, sensor_y = self.position
        dist_to_beacon = (abs(sensor_x - self.closest_beacon[0]) + 
                abs(sensor_y - self.closest_beacon[1]))
        
        no_beacons = []
        for x in range(dist_to_beacon+1):
            for y in range(dist_to_beacon+1 -x):
                positions = {
                    (sensor_x + x, sensor_y + y),
                    (sensor_x + x, sensor_y - y),
                    (sensor_x - x, sensor_y - y),
                    (sensor_x - x, sensor_y + y)} 
                positions -= {self.position, self.closest_beacon}
                no_beacons += list(positions)
        return no_beacons
        

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln

#--------------------- tests -------------------------#

def test_sensor_init():
    sensor = Sensor(2,18, -2,15)
    assert sensor.position == (2, 18)
    assert sensor.closest_beacon == (-2, 15)

def testest_cannot_be_beacons():
    sensor = Sensor(0,0, 0,1)
    no_beacons = sensor.cannot_be_beacons()
    assert len(no_beacons) == 3

def test_cannot_be_beacons_8_7():
    sensor = Sensor(8,7, 2,10)
    no_beacons = sensor.cannot_be_beacons()
    assert (8,-2) in no_beacons

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day.txt')
    print('Hello, World!')
