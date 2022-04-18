from light_sensor import LightSensor
from networking import Networking
import time

print("Starting Lightsensor")
lightsensor = LightSensor()
print("Lightsensor Started")

print("Starting Networking")
networking = Networking()
print("Networking Started")

while True:
    time.sleep(.5)
    print("CONT: " + str(lightsensor.get_last_measurement()))