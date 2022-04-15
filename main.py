from light_sensor import LightSensor
from networking import Networking

print("Starting Lightsensor")
lightsensor = LightSensor()
print("Lightsensor Started")

print("Starting Networking")
networking = Networking()
print("Networking Started")

while True:
    print("CONT: " + lightsensor.get_list_last_day())