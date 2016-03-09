import rpyc
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

def parsing(worker,file):
	fileobj = open(file)
	eventLogs.append(worker.root.line_counter(fileobj))
	
workers=0
with open ("workers.txt", "r") as wrk:
	for line in wrk:
		array.append(line)
		workers=workers+1

for line in array:
	worker = rpyc.connect(line.rstrip('\n').split(':',1)[0], int(line.rstrip('\n').split(':',1)[1]), config={'allow_public_attrs': True})		
	proxy.append(worker)


i=0
os.chdir("log")
start = timeit.default_timer()
threads = []
for file in glob.glob("*.*"):
	# fileobj = open(file)
	# linecount = proxy[i%workers].root.line_counter(fileobj)
	# print linecount
	t = threading.Thread(target=parsing,args=(proxy[i%workers],file,))
	t.start()
	threads.append(t)
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
print " Waktu komputasi yang dibutuhkan : ", (stop - start)

flag = 1
topTen = sorted(events.items(), key = lambda t:t[1], reverse=True)
for key, value in topTen:
	print key,' ',value
	flag+=1
	if (flag > 10):
		break;
# for line in proxy:



# proxy[1] = rpyc.connect('localhost', 18861, config={'allow_public_attrs': True})
# fileobj = open('testfile.txt')
# linecount = proxy.root.line_counter(fileobj)
# print 'The number of lines in the file was', linecount