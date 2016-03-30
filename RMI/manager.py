import rpyc
from customParser import sortByValue

proxy = rpyc.connect('localhost', 18861, config={'allow_public_attrs': True})

fileobj = open('messages')
eventLog = proxy.root.parser(fileobj)

for key, value in eventLog:
	print key, value