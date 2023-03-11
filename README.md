# Smart Heater

This code allows me to remotely operate my plug in wall heater via a web interface, but is also a great starting point for controlling your own devices remotely.

## Hardware

* [Raspberry Pi Pico W](https://www.adafruit.com/product/5526)
* [Micro Servos x 2](https://www.adafruit.com/product/169)

## Installation

* Clone this repo
* Copy `config.example.py` to `config.py` and edit the values. You'll need the following:
    * `ssid` and `password` for your WiFi network
    * `device_id` for your device
    * `api_token` - this is a simple token you'll generate that allows you to securely communicate with this device over http
    * `on_pin` - the pin on the Raspberry Pi Pico W that's connected to the servo that hits the on button on the heater
    * `temp_pin` - the pin on the Raspberry Pi Pico W that's connected to the servo that hits the temperature button on the heater
* Copy all of this to the root of your Raspberry Pi Pico W using [Thonny](https://thonny.org)
* When it first boots up while connected with Thonny, you should see the IP address of the device in the console. Use this to connect to the device.