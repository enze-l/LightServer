import network
import socket
from time import sleep
import _thread
import utime
import machine

class Networking:
    
    def __init__(self):
        self.wifi_tcp = network.WLAN(network.STA_IF)
        self.wifi_ssid = str(open('SSID', 'r').readline(), 'utf8')
        self.wifi_password = str(open('PASSWORD', 'r').readline(), 'utf8')
        
        self.address = socket.getaddrinfo('0.0.0.0', 50000)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(self.address)  
        
        self.start_wifi()
        _thread.start_new_thread(self.listen_socket, ())
        
    def start_wifi(self):
        try:
            if not self.wifi_tcp.isconnected():
                print('connecting to network...')
                self.wifi_tcp.active(True)
                self.wifi_tcp.connect(self.wifi_ssid, self.wifi_password)
                while not self.wifi_tcp.isconnected():
                    pass
            print('network config:', self.wifi_tcp.ifconfig())
        except OSError as e:
            print(e)
            machine.reset()              
        
    def listen_socket(self):
        client = None
        while True:
            try:
                self.socket.listen(1)
                client, self.address = self.socket.accept()
                print('client connected from', self.address)
                client_file = client.makefile('rwb', 0)
                line = str(client_file.readline(), 'utf8')
                line = line.replace('\n', '')
                print(line)
                client.close()
            except Exception as e:
                print(e)
