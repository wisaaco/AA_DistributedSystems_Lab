import time
import sys
import threading
from kazoo.client import KazooClient

# Nerd-activity

class ZooKeeperMutex:
    def __init__(self, zk_hosts='localhost:2181', lock_path='/mutex/lock'):
        self.zk = KazooClient(hosts=zk_hosts)
        self.lock_path = lock_path

    def start(self):
        #TODO
    
    def stop(self):
        #TODO
    
    def acquire_lock(self):
        #TODO
    
    def release_lock(self):
        #TODO
    
