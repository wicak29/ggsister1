import xmlrpc.client
import sys

s = xmlrpc.client.ServerProxy('http://localhost:8000')
s.parseFile('messages')

# Print list of available methods
print(s.system.listMethods())