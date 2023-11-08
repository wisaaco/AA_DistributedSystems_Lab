import socketserver
# Doc: https://docs.python.org/3/library/socketserver.html


# The server
from datetime import datetime

class DateHandler(socketserver.DatagramRequestHandler): # changes !! HERE
    def handle(self):
        print("Got a UDP message from ",self.client_address[0])
        date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p\n")
        self.wfile.write(date.encode("utf-8")) # we write the data on the request 


# A socket connection has a "file" syntax 
with socketserver.UDPServer(('', 5088), DateHandler) as server: # localhost:5088
    print('The date server is running...')
    server.serve_forever()

# The client
## in our case, the client can be the OS 


# using netcat or nc commands:
# nc localhost 5088
# nc -v localhost 5088
# nc -u localhost 5088
# is the port used?
# lsof -i -P -n | grep 5088