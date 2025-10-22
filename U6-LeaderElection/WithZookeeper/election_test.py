from kazoo.client import KazooClient
import time


## Leader Election Simple Structure
# - How long does the znode live ?
    # un znode efímero permanece activo solo mientras la sesión del cliente esté viva y conectada


def mi_funcion_watcher(event):
    print("Event: ", event)

# Iniciar conexión con el clúster de ZooKeeper
zk = KazooClient(hosts='localhost:2181')
zk.start()

# Crear nodo efímero y secuencial
zk.ensure_path("/eleccion")
node_path = zk.create("/eleccion/candidato_", ephemeral=True, sequence=True)


while True:
    children = zk.get_children("/eleccion")
    children.sort()
    if node_path.endswith(children[0]):
        print("Soy el líder")
        time.sleep(10)
        # Realizar tareas de líder
    else:
        # Establecer watcher sobre el nodo anterior
        idx = children.index(node_path.split('/')[-1])
        predecessor = children[idx - 1]
        zk.exists(f"/eleccion/{predecessor}", watch=mi_funcion_watcher)
        # Esperar a que el watcher se active
        print("Esperando a que el watcher se active")
        time.sleep(5)

#?
zk.stop()
print("Done")