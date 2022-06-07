# Source code: https://docs.python.org/es/3/library/xmlrpc.server.html

import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')
# Print list of available methods
print(s.system.listMethods())

print(s.pow(2,3))  # Returns 2**3 = 8
print(s.add(2,3))  # Returns 5
print(s.mul(5,2))  # Returns 5*2 = 10

