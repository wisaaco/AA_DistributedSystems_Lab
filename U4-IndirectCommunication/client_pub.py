import socket
import sys
import select
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broker_address = ('localhost', 10000)

message = b'pub:game:ageIV'

# Send data
print('sending {!r}'.format(message))
sent = sock.sendto(message, broker_address)

print('closing socket')
sock.close()
