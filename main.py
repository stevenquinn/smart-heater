import network
import time
from wificonnection import WifiConnection
from webserver import WebServer
from servo import Servo
import config


class SmartHeater:
    
    on_button = Servo(config.on_pin)
    temp_button = Servo(config.temp_pin)
    on_button_max = 285
    on_button_min = 0
    temp_button_max = 300
    temp_button_min = 0
    button_delay = 0.5
    

    def __init__(self):

        self.routes = {
            'ping': self.ping_route,
            'on-off': self.on_off_route,
            'temp': self.temp_route,
        }

        self.wifi = WifiConnection(config.ssid, config.password)
        self.webserver = WebServer(self.wifi, self.routes, config.api_token)
        self.webserver.listen()
        self.on_button.goto(0)
        self.init_buttons()


    #Initialize the buttons to their starting positions
    def init_buttons(self):
        time.sleep(2)
        self.temp_button.goto(0)
        time.sleep(2)
        
    
    # Route definitions
    def ping_route(self, request):
        return { "pong": True }

    def on_off_route(self, request):
        self.press_on_button()
        return { "on": True }

    def temp_route(self, request):
        self.press_temp_button()
        return { "temp": True }
    

    # Interacting with the pins
    def press_on_button(self):
        self.on_button.goto(self.on_button_max)
        time.sleep(self.button_delay)
        self.on_button.goto(self.on_button_min)
        
    def press_temp_button(self):
        self.temp_button.goto(self.temp_button_max)
        time.sleep(self.button_delay)
        self.temp_button.goto(self.temp_button_min)
    

 
    


smart_heater = SmartHeater()



