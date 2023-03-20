import time
from wificonnection import WifiConnection
from webserver import WebServer
from servo import Servo
import config
import _thread
import json
from scheduler import Scheduler



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
            'get-schedule': self.scheduler.get_schedule(),
            'set-schedule': self.scheduler.set_schedule(),
        }

        # Separate the scheduler and the webserver into their own threads
        self.scheduler = Scheduler()
        self.baton = _thread.allocate_lock()
        _thread.start_new_thread(self.handle_scheduler, ())

        self.wifi = WifiConnection(config.ssid, config.password)
        self.webserver = WebServer(self.wifi, self.routes, config.api_token)
        self.webserver.listen()
        self.on_button.goto(0)
        self.init_buttons()


    def handle_scheduler(self):

        while True:
            self.baton.acquire()

            if self.scheduler.has_schedule():
                if self.scheduler.should_turn_on():
                    self.scheduler.set_ran_today()
                    self.press_on_button()
                    self.press_temp_button()
                
                elif self.scheduler.should_reset():
                    self.scheduler.set_ran_today(False)

            self.baton.release()


    #Initialize the buttons to their starting positions
    def init_buttons(self):
        time.sleep(2)
        self.temp_button.goto(0)
        time.sleep(2)
        
    
    # Route definitions
    def ping_route(self):
        return { "pong": True }

    def on_off_route(self):
        self.press_on_button()
        return { "on": True }

    def temp_route(self):
        self.press_temp_button()
        return { "temp": True }

    def handle_get_schedule(self):
        return json.dump(self.scheduler.get_schedule())
    
    def handle_set_schedule(self, request, params):

        try:
            return self.scheduler.set_schedule(request, json.loads(params['schedule']))

        except:
            return { "error": "Invalid schedule" }
    

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



