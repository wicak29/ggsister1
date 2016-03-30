#!/usr/bin/env python
import pika
import sys
import os
import timeit
import glob

os.chdir("log")

eventLogs = []
events = {}

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

# result = channel.queue_declare(exclusive=True)
# callback_queue = result.method.queue
# channel.basic_consume(on_response, no_ack=True, queue=callback_queue)

start = timeit.default_timer()

for fileName in glob.glob("*.*"):
    print(" [x] Memproses file . . .")
    message = fileName
    eventLogs.append(fileName)
    #message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs',
	                      routing_key='',
	                      body=message)
#print(" [x] Sent %r" % message)

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


connection.close()