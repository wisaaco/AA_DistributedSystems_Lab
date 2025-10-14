import socket
import threading
import random
import time

HOST = '127.0.0.1'
PORT = 57839
NODOS = 10
def send_message(node_id):
    msg = f"Mensaje_de_nodo_{node_id}"
    time.sleep(random.uniform(0, 0.5))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(msg.encode())

def main():
    threads = []
    for i in range(NODOS):
        t = threading.Thread(target=send_message, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
