#SOAP - Manager Code
import SOAPpy
import os
import json
import timeit
import glob
import threading

eventLogs = []
events = {}
threads = []
proxy = []
serverList = [
	'http://localhost:8080',
	'http://localhost:8081',
	'http://localhost:8082',
	'http://localhost:8083',
]
workers = 0

for url in serverList:
	workers += 1
	server = SOAPpy.SOAPProxy(url)
	proxy.append(server)

start = timeit.default_timer()
os.chdir("log")

def parsing(worker, file):
    textLog = open(file,'r').read()
    jsonify = json.dumps(textLog, encoding='latin1')
    print "Processing file : " + file + "\n"
    eventLogs.append(worker.parse(jsonify))

i = 0
for file in glob.glob("*"):
	t = threading.Thread(target=parsing,args=(proxy[i%workers],file,))
	t.start()
	threads.append(t)
	i=i+1

	if (i%workers == workers):
		for thread in threads:
			thread.join()

		del threads[:]

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
