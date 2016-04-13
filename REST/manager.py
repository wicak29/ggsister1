import urllib
import urllib2
import os
import json
import requests

os.chdir('../log/')
# log = open('messages').read().encode('latin1')

# res = requests.post('http://localhost:5000/rest/parse', json={"log": log})
# if res.ok:
#     print res.json()


proxy_handler = urllib2.ProxyHandler({'https': 'http://vessa.rizky12%40mhs.if.its.ac.id:makimaki@proxy.its.ac.id:8080'})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

url = 'http://127.0.0.1:5000/rest/parse'

req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')



params = urllib.urlencode({
  'log' : open('messages').read()
})
response = urllib2.urlopen(req, json.dumps(params))