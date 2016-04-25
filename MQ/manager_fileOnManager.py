#manager file - file On Manager
#!/usr/bin/env python
import pika
import uuid
import os
import glob
import json
import timeit

eventLogs = []
events = {}
class MessageParserWorker(object):
    def __init__(self):
        credentials = pika.PlainCredentials('ggsister', 'ggsister')
        parameters = pika.ConnectionParameters('localhost',
                                               5672,
                                               '/',
                                               credentials)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='fileOnManager',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

ParserWorker = MessageParserWorker()

start = timeit.default_timer()

os.chdir("log")

for file in glob.glob("*.*"):
    n = open(file,'r').read()
    # print(" [x] fib(30)")
    eventLogs.append(ParserWorker.call(n))

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
