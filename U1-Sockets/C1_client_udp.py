import socket
# Client side (UDP)

host, port = "localhost", 5088
data = "hola caracola"

# Create a socket (SOCK_DGRAM means a UDP socket)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    #AF_INET > Conector IPv4
    # Send a datagram to the server (UDP has no connect/handshake)
    sock.sendto(bytes(data + "\n", "utf-8"), (host, port))  # coding

    # Receive the datagram from the server
    received, _ = sock.recvfrom(1024)
    received = str(received, "utf-8")  # decoding


print("Sent:     {}".format(data))
print("Received: {}".format(received))
