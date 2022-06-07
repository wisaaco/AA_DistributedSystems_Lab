import socketserver
# Doc: https://docs.python.org/3/library/socketserver.html


# The server
from datetime import datetime

class DateHandler(socketserver.StreamRequestHandler): #This type of server works file-like object: 
    def handle(self):
        date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p\n")
        
        self.wfile.write(date.encode("utf-8")) # we write the data on the channel
        # Note: Data coding and marshalling in next chapter

# A socket connection has a "file" syntax 
with socketserver.TCPServer(('', 5088), DateHandler) as server: # localhost:5088
    print('The date server is running...')
    server.serve_forever()

# The client
## in our case, the client can be the OS 


# using netcat or nc commands:
# nc localhost 5088
# nc -v localhost 5088

# is the port used?
# lsof -i -P -n | grep 5088