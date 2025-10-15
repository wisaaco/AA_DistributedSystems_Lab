# token_server.py
import socket
import threading
import time
import json
import random

class TokenRingServer:
    def __init__(self, host='0.0.0.0', port=5000, server_id=1, peers=[]):
        self.host = host
        self.port = port
        self.server_id = server_id
        self.peers = peers
        self.has_token = (server_id == 1)  # El servidor 1 inicia con el token
        self.token = None
        self.clients = []
        self.bid_queue = []  # Cola de pujas pendientes
        self.pending_clients = {}  # Clientes esperando respuesta de pujas
        self.auction_state = {
            'current_bid': 0,
            'current_bidder': None,
            'product': "Container XA1203-C. Origen Colombia. Destino Ibiza.",
            'active': True
        }
        
    def start_server(self):
        """Inicia el servidor para aceptar conexiones de clientes"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"Servidor {self.server_id} escuchando en {self.host}:{self.port}")
        
        # Hilo para manejar conexiones de clientes
        client_thread = threading.Thread(target=self.accept_clients, args=(server_socket,))
        client_thread.daemon = True
        client_thread.start()
        
        # Hilo para manejar el token ring entre servidores
        if self.peers:
            token_thread = threading.Thread(target=self.token_ring_handler)
            token_thread.daemon = True
            token_thread.start()
            
            # Hilo para recibir tokens de otros servidores
            token_receiver_thread = threading.Thread(target=self.accept_token_connections)
            token_receiver_thread.daemon = True
            token_receiver_thread.start()
        
        # Mantener el servidor activo
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Cerrando servidor...")
    
    def accept_clients(self, server_socket):
        """Acepta conexiones de clientes"""
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexión aceptada de {addr}")
            self.clients.append(client_socket)
            
            # Hilo para manejar cada cliente
            client_thread = threading.Thread(
                target=self.handle_client, 
                args=(client_socket,)
            )
            client_thread.daemon = True
            client_thread.start()
    
    def handle_client(self, client_socket):
        """Maneja las peticiones de un cliente específico"""
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                response = self.process_client_message(message, client_socket)
                
                # Solo enviar respuesta inmediata si no está en cola
                if response.get('status') != 'queued':
                    client_socket.send(json.dumps(response).encode('utf-8'))
                
        except Exception as e:
            print(f"Error con cliente: {e}")
        finally:
            # Limpiar referencias del cliente
            self.clients.remove(client_socket)
            # Remover de pending_clients si existe
            for bid_id, socket in list(self.pending_clients.items()):
                if socket == client_socket:
                    del self.pending_clients[bid_id]
            client_socket.close()
    
    def process_client_message(self, message, client_socket=None):
        """Procesa los mensajes de los clientes"""
        action = message.get('action')
        
        if action == 'get_auction_state':
            return {'status': 'success', 'data': self.auction_state}
        
        elif action == 'place_bid':
            bid_amount = message.get('bid_amount')
            bidder_id = message.get('bidder_id')
            
            if not self.has_token:
                # Si no tenemos el token, agregar a la cola
                bid_id = f"{bidder_id}_{int(time.time() * 1000)}"
                self.bid_queue.append({
                    'bid_id': bid_id,
                    'bid_amount': bid_amount,
                    'bidder_id': bidder_id,
                    'timestamp': time.time()
                })
                
                # Guardar referencia del cliente para responder después
                if client_socket:
                    self.pending_clients[bid_id] = client_socket
                
                return {
                    'status': 'queued', 
                    'message': f'Puja de ${bid_amount} agregada a la cola. Esperando token...',
                    'bid_id': bid_id
                }
            
            # Si tenemos el token, procesar inmediatamente
            return self.process_bid(bid_amount, bidder_id)
        
        return {'status': 'error', 'message': 'Acción desconocida'}
    
    def process_bid(self, bid_amount, bidder_id):
        """Procesa una puja individual"""
        # Verificar si la puja es válida
        if bid_amount > self.auction_state['current_bid']:
            # Simular procesamiento crítico
            rand_time = random.uniform(1, 8)
            time.sleep(rand_time)  # Retardo para evidenciar problemas de concurrencia
            
            self.auction_state['current_bid'] = bid_amount
            self.auction_state['current_bidder'] = bidder_id
            
            return {
                'status': 'success', 
                'message': f'Puja aceptada! Nuevo precio: ${bid_amount}'
            }
        else:
            return {
                'status': 'error', 
                'message': f'Puja debe ser mayor a ${self.auction_state["current_bid"]}'
            }
    
    def token_ring_handler(self):
        """Maneja la lógica del token ring entre servidores"""
        while True:
            if self.has_token:
                # Mantener el token por un tiempo
                time.sleep(10)  # Token held for 10 seconds
                
                # Pasar el token al siguiente servidor
                self.pass_token()
            else:
                time.sleep(1)
    
    def pass_token(self):
        """Pasa el token al siguiente servidor en el anillo"""
        next_server = self.peers[0]  # En este caso simple, solo hay un peer
        token_port = next_server['port'] + 1000  # Puerto para tokens
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((next_server['host'], token_port))
                token_message = {
                    'type': 'token_pass',
                    'auction_state': self.auction_state
                }
                s.send(json.dumps(token_message).encode('utf-8'))
                
                self.has_token = False
                print(f"Token pasado a servidor {next_server['id']} en puerto {token_port}")
                
        except Exception as e:
            print(f"Error pasando token: {e}")
            # Si no se puede pasar, mantener el token
            self.has_token = True
    
    def accept_token_connections(self):
        """Acepta conexiones de otros servidores para recibir tokens"""
        # Usar un puerto diferente para comunicación entre servidores
        token_port = self.port + 1000  # Puerto para tokens
        
        token_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        token_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        token_socket.bind((self.host, token_port))
        token_socket.listen(5)
        
        print(f"Servidor {self.server_id} escuchando tokens en puerto {token_port}")
        
        while True:
            try:
                client_socket, addr = token_socket.accept()
                print(f"Conexión de token recibida de {addr}")
                
                # Hilo para manejar cada conexión de token
                token_handler_thread = threading.Thread(
                    target=self.handle_token_message, 
                    args=(client_socket,)
                )
                token_handler_thread.daemon = True
                token_handler_thread.start()
                
            except Exception as e:
                print(f"Error aceptando conexión de token: {e}")
    
    def handle_token_message(self, client_socket):
        """Maneja mensajes de token de otros servidores"""
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                message = json.loads(data)
                if message.get('type') == 'token_pass':
                    self.receive_token(message)
        except Exception as e:
            print(f"Error manejando mensaje de token: {e}")
        finally:
            client_socket.close()
    
    def receive_token(self, token_data):
        """Recibe el token de otro servidor"""
        self.has_token = True
        self.auction_state = token_data.get('auction_state', self.auction_state)
        print(f"Token recibido. Estado actual: {self.auction_state}")
        
        # Procesar cola de pujas pendientes
        self.process_bid_queue()
    
    def process_bid_queue(self):
        """Procesa todas las pujas en la cola cuando se recibe el token"""
        print(f"Procesando {len(self.bid_queue)} pujas en cola...")
        
        # Ordenar por timestamp para procesar en orden de llegada
        self.bid_queue.sort(key=lambda x: x['timestamp'])
        
        while self.bid_queue:
            bid = self.bid_queue.pop(0)
            bid_id = bid['bid_id']
            bid_amount = bid['bid_amount']
            bidder_id = bid['bidder_id']
            
            print(f"Procesando puja de {bidder_id}: ${bid_amount}")
            
            # Procesar la puja
            result = self.process_bid(bid_amount, bidder_id)
            
            # Enviar respuesta al cliente si aún está conectado
            if bid_id in self.pending_clients:
                try:
                    client_socket = self.pending_clients[bid_id]
                    client_socket.send(json.dumps(result).encode('utf-8'))
                    del self.pending_clients[bid_id]
                    print(f"Respuesta enviada a cliente {bidder_id}: {result['message']}")
                except Exception as e:
                    print(f"Error enviando respuesta a cliente {bidder_id}: {e}")
                    if bid_id in self.pending_clients:
                        del self.pending_clients[bid_id]
        
        print("Cola de pujas procesada completamente")

if __name__ == "__main__":
    import sys
    
    server_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    # Configuración para dos servidores
    if server_id == 1:
        server = TokenRingServer(
            host='0.0.0.0',
            port=5000,
            server_id=1,
            peers=[{'host': '192.168.0.103', 'port': 5001, 'id': 2}]
        )
    else:
        server = TokenRingServer(
            host='0.0.0.0',
            port=5001,
            server_id=2,
            peers=[{'host': '192.168.0.102', 'port': 5000, 'id': 1}]
        )
    
    server.start_server()