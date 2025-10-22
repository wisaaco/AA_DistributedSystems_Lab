# DOC Referencies:
# https://kazoo.readthedocs.io/en/latest/api/client.html
# https://zookeeper.apache.org/doc/r3.4.6/javaExample.html

from kazoo.client import KazooClient
import time


### KAZOO Primitives

# Iniciar conexión con el clúster de ZooKeeper
zk = KazooClient(hosts='localhost:2181')


## Start the connection
zk.start()

# Crear un znode si no existe
if not zk.exists("/ejemplo"):
    zk.create("/ejemplo", ephemeral=True)

zk.ensure_path("/ejemplo") # Ensure the path exists

if not zk.exists("/ejemplo/lock-caseA"):
    zk.create("/ejemplo/lock-caseA")

if not zk.exists("/ejemplo/coordinacion/nodo1"):
    zk.create("/ejemplo/coordinacion/nodo1",b"Quiero coordinar")

########################################################


# Obtener datos del nodo
data, stat = zk.get("/ejemplo/coordinacion/nodo1")

print("Datos actuales:", data.decode("utf-8"))
print("Stat: ", stat)

# Modificar nodo
zk.set("/ejemplo/coordinacion/nodo1", b"nuevo valor")

data, stat = zk.get("/ejemplo/coordinacion/nodo1")
print("--------------------------------")
print("Datos actuales:", data.decode("utf-8"))
print("Stat: ", stat)

########################################################

# Crear un nodo de lock
lock_node = zk.create(
                f"/ejemplo/lock-caseA/lock-", 
                ephemeral=True, 
                sequence=True
            )

print("Lock node: ", lock_node)

## Print the lock node

children = zk.get_children("/ejemplo/lock-caseA")
children.sort()
print("Hijos del nodo /ejemplo/lock-caseA: ", children)
print("children[0]: ", children[0])

# Get the lock node
data, stat = zk.get(f"/ejemplo/lock-caseA/{children[0]}")
print("Datos actuales:", data.decode("utf-8"))
print("Stat: ", stat)

print("--------------------------------")
########################################################

# Another "access" to the lock node
lock_node2 = zk.create(
                f"/ejemplo/lock-caseA/lock-", 
                ephemeral=True, 
                sequence=True)

children = zk.get_children("/ejemplo/lock-caseA")
children.sort()
print("Hijos del nodo /ejemplo/lock-caseA: ", children)

def watch_previous_node(event):
    print("\t\tThe node has been deleted: ", event)
    #event.type == 'DELETED'
    #event.type == 'CREATED'
    #event.type == 'CHANGED'

# The second lock wait for the first lock node to be deleted
zk.exists(f"/ejemplo/lock-caseA/{children[0]}", watch=watch_previous_node)
print("Waiting for the previous node to be deleted")
time.sleep(5)

print("Deleting the lock node")
zk.delete(lock_node)

time.sleep(5)



# Cerrar conexión
zk.stop()
print("Done")