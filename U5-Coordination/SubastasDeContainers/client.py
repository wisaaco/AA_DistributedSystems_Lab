# auction_client.py
import socket
import json
import threading
import time
import random

class AuctionClient:
    def __init__(self, client_id, servers=[('192.168.0.102', 5000), ('192.168.0.103', 5001)]):
        self.client_id = client_id
        self.servers = servers
        self.current_server = 0
        
    def connect_to_server(self):
        """Intenta conectarse a un servidor disponible"""
        for i, server in enumerate(self.servers):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(30)  # Timeout más largo para esperar respuestas de cola
                s.connect(server)
                self.current_server = i
                return s
            except:
                continue
        return None
    
    def get_auction_state(self):
        """Obtiene el estado actual de la subasta"""
        sock = self.connect_to_server()
        if sock:
            try:
                message = {'action': 'get_auction_state'}
                sock.send(json.dumps(message).encode('utf-8'))
                response = json.loads(sock.recv(1024).decode('utf-8'))
                return response
            finally:
                sock.close()
        return {'status': 'error', 'message': 'No se pudo conectar a ningún servidor'}
    
    def place_bid(self, amount):
        """Intenta realizar una puja"""
        sock = self.connect_to_server()
        if sock:
            try:
                message = {
                    'action': 'place_bid',
                    'bid_amount': amount,
                    'bidder_id': self.client_id
                }
                sock.send(json.dumps(message).encode('utf-8'))
                
                # Recibir respuesta inicial
                response = json.loads(sock.recv(1024).decode('utf-8'))
                
                # Si la puja fue agregada a la cola, esperar respuesta final
                if response.get('status') == 'queued':
                    print(response['message'])
                    print("Esperando procesamiento...")
                    
                    # Mantener conexión abierta y esperar respuesta final
                    try:
                        final_response = json.loads(sock.recv(1024).decode('utf-8'))
                        return final_response
                    except Exception as e:
                        return {'status': 'error', 'message': f'Error esperando respuesta: {e}'}
                else:
                    # Respuesta inmediata (token disponible)
                    return response
                    
            except Exception as e:
                return {'status': 'error', 'message': f'Error de conexión: {e}'}
            finally:
                sock.close()
        return {'status': 'error', 'message': 'No se pudo conectar a ningún servidor'}
    


def main():
    client_id = input("Ingresa tu ID de cliente: ")
    client = AuctionClient(client_id)
    
    print("=== Sistema de Subastas Distribuidas ===")
    print("Comandos: estado, pujar <monto>, salir")
    
    while True:
        command = input("> ").strip().split()
        
        if not command:
            continue
            
        if command[0] == 'estado':
            response = client.get_auction_state()
            if response['status'] == 'success':
                state = response['data']
                print(f"Producto: {state['product']}")
                print(f"Puja actual: ${state['current_bid']}")
                print(f"Mejor postor: {state['current_bidder']}")
            else:
                print(f"Error: {response['message']}")
                
        elif command[0] == 'pujar' and len(command) > 1:
            try:
                amount = int(command[1])
                response = client.place_bid(amount)
                print(response['message'])
            except ValueError:
                print("Monto debe ser un número")
       
                
        elif command[0] == 'salir':
            break
            
        else:
            print("Comando no reconocido")

if __name__ == "__main__":
    main()