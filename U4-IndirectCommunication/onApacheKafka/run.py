import threading
from node_x import node

for i in range(3):
    threading.Thread(target=node, args=(i,), daemon=False).start()
