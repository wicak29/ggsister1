from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sys

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()
print("Listening on port 8000...")

#inisialisasi pemisah kata dan karakter
stopWord = ['for', 'from', 'to', 'with', 'after', 'at']
forbiddenChar = [';', ':', ',', '(']

#definisi fungsi
def parseLine(lineText):
	logDetails = lineText.split()[5:]
	eventName = ''
	for word in logDetails:
		
		if (word in stopWord):
			break;

		if ('(' in word):
			stopChar = word.index('(')
			if stopChar != 0:
				eventName = eventName + ' ' + word[0:stopChar]
			break;

		if (';' in word) or (':' in word) or (',' in word):
			word = word[:-1]
			eventName = eventName + ' ' + word
			break;

		if "'" in word:
			break;

		eventName = eventName + ' ' + word

	return eventName

def parseFile(logFile):
	eventLog = {}

	with open(logFile) as log:
		for line in log:
			eventName = parseLine(line);
			if eventName in eventLog:
				eventLog[eventName] = eventLog[eventName] + 1
			else:
				eventLog[eventName] = 1

	eventLog = sortByValue(eventLog)
	for key, value in eventLog:
		print (key, value)

	return eventLog

def sortByValue(dict):
	result = sorted(dict.items(), key = lambda t:t[1])
	return result

server.register_function(parseLine, 'parseLine')
server.register_function(parseFile, 'parseFile')
server.register_function(sortByValue, 'sortByValue')

# Run the server's main loop
server.serve_forever()