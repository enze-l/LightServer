import network
import machine
import tinyweb
import light_sensor
from light_sensor import LightSensor

app = tinyweb.webserver()
subscriberList = []
light_sensor = LightSensor(subscriberList)

def start_networking():
    wifi_tcp = network.WLAN(network.STA_IF)
    wifi_ssid = str(open('SSID', 'r').readline(), 'utf8')
    wifi_password = str(open('PASSWORD', 'r').readline(), 'utf8')        
    try:
        if not wifi_tcp.isconnected():
            print('connecting to network...')
            wifi_tcp.active(True)
            wifi_tcp.connect(wifi_ssid, wifi_password)
            while not wifi_tcp.isconnected():
                pass
        print('network config:', wifi_tcp.ifconfig())
    except OSError as e:
        print(e)
        machine.reset()
        
def run():
    start_networking()
    app.add_resource(Subscriber, "/subscriber/<ip>")
    app.run(host='0.0.0.0', port=50000)
    
@app.route("/subscriber")
async def subscriber(request, response):
    await response.start_html()
    await response.send(str(subscriberList))

@app.route("/reading")
async def reading(request, response):
    await response.start_html()
    await response.send(str(light_sensor.get_last_measurement()))

@app.route("/reading/min")
async def min(request, response):
    await response.start_html()
    await response.send(str(light_sensor.get_min_level()))

@app.route("/reading/max")
async def max(request, response):
    await response.start_html()
    await response.send(str(light_sensor.get_max_level()))

@app.route("/list/day")
async def list_day(request, response):
    await response.start_html()
    await response.send(str(light_sensor.get_list_last_day()))

@app.route("/list/100")
async def list_100(request, response):
    await response.start_html()
    await response.send(str(light_sensor.get_list_last_100()))
    
class Subscriber():
    def post(self, data, ip):
        subscriberList.append(ip)
        print(ip + " added to Subscribers")
        return ip

    def delete(self, data, ip):
        subscriberList.remove(ip)
        print(ip + " removed from Subscribers")
        return "successfully_deleted"
    