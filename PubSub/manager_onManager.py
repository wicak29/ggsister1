#!/usr/bin/env python
import pika
import sys
import os
import json
import timeit
import glob

os.chdir("log")

eventLogs = []
flag = 0
events = {}

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs',type='fanout')

#--------------------------------------------------------------------------
# def on_response(self, ch, method, props, body):
#         if self.corr_id == props.correlation_id:
#             self.response = json.loads(body)

# result = channel.queue_declare(exclusive=True)
# queue_name = result.method.queue
# channel.basic_consume(on_response, no_ack=True, queue=callback_queue
#---------------------------------------------------------------------------

start = timeit.default_timer()

count_mess = 0

for file in glob.glob("*.*"):
    n = open(file,'r').read()
    # print(" [x] fib(30)")   
    message = n
    count_mess +=1
    #print count_mess

    #message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs_manager', routing_key='', body=message)

#----------------------------------------------------------------------------------
channel2 = connection.channel()
channel2.exchange_declare(exchange='result_manager', type='direct')
result = channel2.queue_declare(exclusive=True)
queue_name = result.method.queue
channel2.queue_bind(exchange='result_manager', routing_key='c', queue=queue_name)

def callback(ch, method, properties, body):
    body = json.loads(body)
    # print " [x] %r" % (body)
    eventLogs.append(body)
    global flag 
    flag = flag + 1
    print flag
    if flag >= count_mess :
        channel2.stop_consuming()

channel2.basic_consume(callback, queue=queue_name, no_ack=True)

channel2.start_consuming()

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