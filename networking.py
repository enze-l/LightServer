import network
import machine
import tinyweb

app = tinyweb.webserver()
    
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
    app.run(host='0.0.0.0', port=50000)

@app.route("/")
async def index(request, response):
    await response.start_html()
    await response.send('<html><body><h1>Hello, world! (<a href="/table">table</a>)</h1></html>\n')

