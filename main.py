import config
from wificonnection import WifiConnection
from webserver import WebServer
from button import Button


class SmartHeater:
    
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

        self.on_button = Button(pin=config.on_pin, min_position=self.on_button_min, max_position=self.on_button_max)
        self.temperature_button = Button(pin=config.temp_pin, min_position=self.temp_button_min, max_position=self.temp_button_max)

        self.wifi = WifiConnection(config.ssid, config.password)
        self.webserver = WebServer(self.wifi, self.routes, config.api_token)
        self.webserver.listen()
        
        
    
    # Route definitions
    def ping_route(self, request):
        return { "pong": True }

    def on_off_route(self, request):
        self.on_button.press()
        return { "on": True }

    def temp_route(self, request):
        self.temperature_button.press()
        return { "temp": True }
    

smart_heater = SmartHeater()



