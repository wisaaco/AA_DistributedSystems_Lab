import socket
# Client side

import sys

host, port = "localhost", 5088
data = "hola caracola"

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((host, port))
    sock.sendall(bytes(data + "\n", "utf-8")) # coding 

    # Receive data from the server
    received = str(sock.recv(1024), "utf-8") #decoding 

print("Sent:     {}".format(data))
print("Received: {}".format(received)),