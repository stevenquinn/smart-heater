import network
import socket
import time
import json

from servo import Servo
from machine import Pin, PWM


class WifiConnection:
    
    ssid = "Quinn Wifi"
    password = "Conn8dsHorn"
    max_wait = 10
    wlan = network.WLAN(network.STA_IF)
    
    def __init__(self):
        self.wlan.active(True)
        
    
    def connect(self):
        self.wlan.connect(self.ssid, self.password)
        
        while self.max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            
            self.max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print( 'ip = ' + status[0] )

        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        print('listening on', addr)

        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        
        return s
        
        


class SmartHeater:
    
    on_button = Servo(0)
    temp_button = Servo(1)


    def __init__(self):
        self.wifi = WifiConnection()
        self.s = self.wifi.connect()
        self.on_button.goto(0)
        time.sleep(2)
        self.temp_button.goto(0)
        time.sleep(2)
        self.run_server = True
        
        
    def is_route(self, request, route):
        return request.find(route) == 6
    
    def press_on_button(self):
        self.on_button.goto(285)
        time.sleep(0.5)
        self.on_button.goto(0)
        
    def press_temp_button(self):
        self.temp_button.goto(300)
        time.sleep(0.5)
        self.temp_button.goto(0)
    
        
    def listen_for_input(self):
        
        while self.run_server:
            try:
                cl, addr = self.s.accept()
                print('client connected from', addr)
                request = cl.recv(1024)
                request = str(request)
                json_data = {}
                
                
                # Make sure device is alive and running
                if self.is_route(request, '/ping'):
                    json_data = { "pong": True }
                    
                if self.is_route(request, '/on-off'):
                    self.press_on_button()
                    json_data = { "on": True }
                    
                if self.is_route(request, '/temp'):
                    self.press_temp_button()
                    json_data = { "temp": True }
                    
                if self.is_route(request, '/shut-down'):
                    self.run_server = False
                    

                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(json.dumps(json_data))
                cl.close()

            except OSError as e:
                cl.close()
                print('connection closed')

    


smart_heater = SmartHeater()
smart_heater.listen_for_input()


