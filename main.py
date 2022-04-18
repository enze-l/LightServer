from light_sensor import LightSensor
import networking
import time

print("Starting Lightsensor")
lightsensor = LightSensor()
print("Lightsensor Started")

print("Starting Networking")
networking.run()
print("Networking Started")
