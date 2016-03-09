import rpyc
from customParser import parseObject
class MyService(rpyc.Service):
    def exposed_line_counter(self, fileobj):
    	eventLog = parseObject(fileobj)
        #linenum = len(fileobj.readlines())
        return eventLog

from rpyc.utils.server import ThreadedServer
t = ThreadedServer(MyService, port=11811)
t.start()