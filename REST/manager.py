#REST - Manager Code

=======
import json
import urllib2

# request to REST web service
url = 'http://localhost:5000/parser'
response = urllib2.urlopen(url)

# print return value as json
print json.load(response)
