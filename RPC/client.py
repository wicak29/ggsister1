import xmlrpclib
import sys
import json
#import time

import glob
import os
import threading
import timeit
from collections import OrderedDict


array = []
proxy = []
eventLogs = []
events = {}
counter = 0

#s = xmlrpc.client.ServerProxy('http://localhost:8000')
#start = time.time()
#s.parseFile('messages.1')

#-------------------------------------------------------------------------

def parsing(worker,file):
	result = worker.line_counter(file)
	result = json.loads(result)
	eventLogs.append(result)

# menghitung worker yang ada
workers=0
with open ("workers.txt", "r") as wrk:
	for line in wrk:
		array.append(line)
		workers=workers+1

for line in array:
	print ("http://"+line.rstrip('\n').split(';',1)[0])
	worker = xmlrpclib.ServerProxy("http://"+line.rstrip('\n'), allow_none=True)
	print(worker.add(2,3))  # Returns 5
	# worker = xmlrpc.client.ServerProxy(line)
	proxy.append(worker)


i=0
os.chdir("log")
start = timeit.default_timer()
threads = []
for file in glob.glob("*.*"):
	filetxt = open(file).read()
	result = proxy[i%workers].line_counter(filetxt)
	result = json.loads(result)
	eventLogs.append(result)
	# t = threading.Thread(target=parsing,args=(proxy[i%workers],file,));
	# t.start()
	# threads.append(t)
	i=i+1

for thread in threads:
	thread.join()

for event in eventLogs:
	for key, value in event:
		if key in events:
			events[key] = events[key] + value
		else:
			events[key] = value

stop = timeit.default_timer()
print (" Waktu komputasi yang dibutuhkan : ", (stop - start))

flag = 1
topTen = sorted(events.items(), key = lambda t:t[1], reverse=True)
for key, value in topTen:
	print (key,' ',value)
	flag+=1
	if (flag > 10):
		break;
#---------------------------------------------------------------------------
# Print list of available methods
#print(s.system.listMethods())

# print time spent
#print("%s seconds" % (time.time() - start))
