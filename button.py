from servo import Servo
import time

class Button():

    def __init__(self, pin, min_position, max_position):
        self.servo = Servo(pin)
        self.min_position = min_position
        self.max_position = max_position
        self.button_press_delay = 0.5
        self.reset()


    def reset(self):
        time.sleep(1)
        self.servo.goto(0)


    def press(self):
        self.servo.goto(self.max_position)
        time.sleep(self.button_press_delay)
        self.servo.goto(self.min_position)
        time.sleep(self.button_press_delay)