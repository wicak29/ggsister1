import urllib
import urllib2
import os
import json
import glob
import timeit
import threading
import time

eventLogs = []
events = {}
threads = []

os.chdir('log/')
# log = open('messages').read().encode('latin1')

# res = requests.post('http://localhost:5000/rest/parse', json={"log": log})
# if res.ok:
#     print res.json()


proxy_handler = urllib2.ProxyHandler({'https': 'http://vessa.rizky12%40mhs.if.its.ac.id:makimaki@proxy.its.ac.id:8080'})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

serverList = [
	'http://localhost:5000/rest/parse',
	'http://localhost:5001/rest/parse',
	'http://localhost:5000/rest/parse',
	'http://localhost:5001/rest/parse',
	# 'http://localhost:5000/rest/parse',
	# 'http://localhost:5000/rest/parse',
]
serverCount = len(serverList)

def parsing(url, fileName,threadNo):
	req = urllib2.Request(url)
	req.add_header('Content-Type', 'application/json')

	print "Thread #" + str(threadNo) + " Processing file : " + fileName
	fileContent = open(file).read()
	params = urllib.urlencode({
	  'log' : fileContent
	})
	response = json.load(urllib2.urlopen(req, json.dumps(params)))
	eventLogs.append(response)

i = 0

start = timeit.default_timer()

for file in glob.glob("*"):
	t = threading.Thread(target=parsing,args=(serverList[i%serverCount],file,i%serverCount,))
	t.start()
	threads.append(t)

	time.sleep(0.005)
	i=i+1

	if (i%serverCount == 0):
		for thread in threads:
			thread.join()

		del threads[:]

for thread in threads:
	thread.join()

print len(eventLogs)

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
