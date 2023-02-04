import network 
import socket
import time


class WifiConnection:

    max_wait = 10
    wlan = network.WLAN(network.STA_IF)


    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
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