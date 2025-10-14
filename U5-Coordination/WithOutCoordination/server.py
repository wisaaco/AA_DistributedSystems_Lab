import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 57839
FILENAME = 'shared_resource.txt'

# lock = threading.Lock()

f = open(FILENAME, "w", buffering=1)

def handle_client(conn, addr):
    data = conn.recv(1024).decode()
    print(f"[SERVER] Recibido de {addr}: {data}")

    # with lock:
    for char in data:
        f.write(char)
        time.sleep(0.01) 
    f.write("\n")

    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Esperando conexiones en {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
