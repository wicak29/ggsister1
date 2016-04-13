#SOAP - Worker Code
import SOAPpy
from customParser import parseText
import json

def parse(textLog):
	print "\n------------------------------ Processing request ------------------------------\n"
	print textLog
	jsonify = json.loads(textLog, encoding='latin1')
	eventLog = parseText(jsonify)
	print "\n---------------------------- END Processing request ----------------------------\n"

	return eventLog

serverName = "localhost"
serverPort = 8083

server = SOAPpy.SOAPServer((serverName, serverPort))
server.registerFunction(parse)
print "Serving SOAP on " + serverName + " port " + str(serverPort)
server.serve_forever()