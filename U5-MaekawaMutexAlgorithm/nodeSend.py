from copy import deepcopy
from datetime import datetime, timedelta
import heapq
from math import ceil, sqrt
import re
import select
import sys
from threading import Event, Thread, Timer
import utils
import config

class NodeSend(Thread):
    def __init__(self, node):
        Thread.__init__(self)
        self.node = node
        self.client_sockets = [utils.create_client_socket() for i in range(config.numNodes)]
    
    def build_connection(self):
        # print("Node_%i build_connections"%self.node.id)
        for i in range(config.numNodes):
            # print("\t on N%i: %i"%(i,config.port+i))
            # print('localhost',config.port+i)
            self.client_sockets[i].connect(('localhost',config.port+i))
            # print("\t socket on N%i: %s"%(i,self.client_sockets[i]))
    
    def run(self):
        None

    def send_message(self, msg, dest, multicast=False):
        """Send message to another node

        Args:
            msg (Message): message object to be sent
            dest (int): node id of the destination node
            multicast (boolean): indicates whether the message is sent by
                                 unicast or multicast.

        """
        if not multicast:
            self.node.lamport_ts += 1
            msg.set_ts(self.node.lamport_ts)
        assert dest == msg.dest

       
        self.client_sockets[dest].sendall(bytes(msg.to_json(),encoding='utf-8'))


    def multicast(self, msg, group):
        """Multicast message to a group

        Args:
            msg (Message): message object to be multicasted
            group: a list of destination node ids 

        """
        self.node.lamport_ts += 1
        msg.set_ts(self.node.lamport_ts)
        for dest in group:
            new_msg = deepcopy(msg)
            new_msg.set_dest(dest)
            assert new_msg.dest == dest
            assert new_msg.ts == msg.ts
            self.send_message(new_msg, dest, True)

