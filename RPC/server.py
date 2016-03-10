from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from customParser import parseObject
import datetime
import glob
import os
import timeit
import threading
import socket
import traceback
import pickle
#import sys

# Create server
server = SimpleXMLRPCServer(("localhost", 8000), logRequests=True, allow_none=True)
# server.register_introspection_functions()
print("Listening on port 8000...")

# Fungsi line counter
def line_counter(fileobj):
	eventLog = parseObject(fileobj)
	return eventLog

def adder_function(x,y):
    return x + y
server.register_function(adder_function, 'add')

server.register_function(line_counter, 'line_counter')
# Run the server's main loop
server.serve_forever()