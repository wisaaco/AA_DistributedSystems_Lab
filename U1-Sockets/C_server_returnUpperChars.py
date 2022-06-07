import socketserver
# Doc: https://docs.python.org/3/library/socketserver.html


# The server that receives data from the client
from datetime import datetime

class DateHandler(socketserver.BaseRequestHandler): # changes
    def handle(self):
        data = self.request.recv(1024).strip() # recv() is the buffer
        self.request.sendall(data.upper())
        print(dir(self.request))
        # DOC: https://docs.python.org/3/library/socketserver.html#request-handler-objects


# A socket connection has a "file" syntax 
with socketserver.TCPServer(('', 5088), DateHandler) as server: # localhost:5088˙
    print('The date server is running...')
    server.serve_forever()

# The client
## in our case, the client can be the OS 

# using netcat or nc commands:
# echo hola | nc localhost 5088
