import network
import socket
import json

class WebServer:

    """
    Create a new web server instance.

    wifiConnection: (WifiConnection) - The wifi connection object that will be used to connect to the wifi.
    routes: (dictionary) - Routes that the server will listen for. The key is the route and the value is the function that will be executed when the route is requested.
    token: (string) - The token that will be used to authenticate requests. This token will be sent in the request as a query parameter.
    """
    def __init__(self, wifiConnection, routes, token):
        self.wifiConnection = wifiConnection
        self.routes = routes
        self.token = token
        self.s = self.wifiConnection.connect()
        self.run_server = True


    # Listen for incoming http requests. This loop will run forever until the server is stopped.
    def listen(self):
        
        while self.run_server:
            try:
                cl,addr = self.s.accept()
                print('client connected from', addr)
                request = cl.recv(1024)
                request = str(request)
                status_code = 200
                json_data = {}

                # Needs to include the api token or it will return a 401
                if (self.request_has_valid_token(request) != True):
                    status_code = 401 
                    self.send_response(cl, status_code, json_data)
                    continue

                # If the route does not exist, return a 404
                if (self.routeExists(request) != True):
                    status_code = 404
                else:
                    json_data = self.executeRoute(request)

                # Send the response back to the requester
                self.send_response(cl, status_code, json_data)

                
            except Exception as e:
                # If it failed, try reconnecting to the wifi
                print('failed to accept client connection')
                cl.close()



    # Check if the request has a valid token. This is a simple check to see if the token is in the request string.
    def request_has_valid_token(self, request_string):
        token_params = "?token=" + self.token
        return token_params in request_string
    
    
    def get_request_route(self, request):
        url = request.split('?')
        url = url[0].split('GET /')
        return url[1]


    # Send an HTTP request with the json data back to the requester.
    def send_response(self, cl, status_code, data):
        cl.send('HTTP/1.0 ' + str(status_code) + '\r\nContent-type: application/json\r\n\r\n')
        cl.send(json.dumps(data))
        cl.close()


    def routeExists(self, request):
        
        return self.get_request_route(request) in self.routes


    """
    Execute the route that was requested.
    Assuming there's a function in the route dictionary that matches the request.
    """ 
    def executeRoute(self, request):
        return self.routes[self.get_request_route(request)](request)
