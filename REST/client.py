import urllib
import urllib2
import os
import json
import requests
import glob

os.chdir('../log/')
# log = open('messages').read().encode('latin1')

# res = requests.post('http://localhost:5000/rest/parse', json={"log": log})
# if res.ok:
#     print res.json()
eventLogs = []
events = {}

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

proxy_handler = urllib2.ProxyHandler({'https': 'http://vessa.rizky12%40mhs.if.its.ac.id:makimaki@proxy.its.ac.id:8080'})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

url = 'http://127.0.0.1:5000/rest/parse'

req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')

params = urllib.urlencode({
  'log' : open('messages.1').read()
})

response = urllib2.urlopen(req, json.dumps(params))
hasil = json.load(response)
json_res = json.dumps(hasil)
ures = json_loads_byteified(json_res)
test = len(ures['res'])

for i in range (0,test):
	eventLogs.append(ures['res'][i])
	print ures['res'] [i]

# print eventLogs
for event in eventLogs:
	for key, value in event:
		if key in events:
			events[key] = events[key] + value
		else:
			events[key] = value

#fungsi mengurutkan 10 teratas
flag = 1
topTen = sorted(events.item(), key = lambda t:t[1], reverse=True)
for key, value in topTen:
	print key, ' ', value
	flag+=1
	if (flag > 10):
		break