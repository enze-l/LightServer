from machine import Pin, SoftI2C
from bh1750 import BH1750
import _thread
import time
from MicroWebCli.microWebCli import MicroWebCli

class LightSensor:
    def __init__(self, subscriberList):
        self.sensor = BH1750(SoftI2C(scl=Pin(22), sda=Pin(21)))
        self.max_level = 0
        self.min_level = 65000
        self.list_100 = []
        self.list_day = []
        self.last_day_increment = 0
        self.subscriberList = subscriberList
        _thread.start_new_thread(self.__measure, ())

    def __measure(self):
        while True:
            level = int(self.sensor.luminance(BH1750.CONT_HIRES_2))
            
            self.list_100.append(level)
            if len(self.list_100) > 100:
                del self.list_100[0]
                
            if (self.last_day_increment + 60 * 30 <  time.time()):
                self.last_day_increment = time.time()
                self.list_day.append(level)
            if len(self.list_day) > 48:
                del self.list_day[0]
                
            if level < self.min_level:
                self.min_level = level
            if level > self.max_level:
                self.max_level = level

            self.send_value(level)
    
    def get_last_measurement(self):
        return self.list_100[len(self.list_100) - 1]

    def get_list_last_day(self):
        return ' '.join(map(str, self.list_day))
    
    def get_list_last_100(self):
        return ' '.join(map(str, self.list_100))
    
    def get_max_level(self):
        return self.max_level

    def get_min_level(self):
        return self.min_level

    def send_value(self, value):
        try:
            for subscriber in self.subscriberList :
                MicroWebCli.POSTRequest("http://" + subscriber + "/sensor", { "value": str(self.get_last_measurement()) } )
        except Exception as e:
            print(e)