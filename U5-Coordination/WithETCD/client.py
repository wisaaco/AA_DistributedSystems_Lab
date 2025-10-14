import etcd3
import time

print("Connecting to etcd...")
client = etcd3.client(host='localhost', port=2379)  # conecta al cluster de etcd
print("Connected to etcd")
lock_name = "my_distributed_lock"

with client.lock(lock_name, ttl=10) as lock:
    print("Lock acquired, entering critical section")
    time.sleep(5)  # simulamos operación crítica
    print("Exiting critical section, lock released")
