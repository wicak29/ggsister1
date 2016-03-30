#!/usr/bin/env python
import pika
import os
import glob
import json
from customParser import parseText

os.chdir("log")

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(" --- Receive request --- ")
	fileName = body
	message = open(fileName, 'r').read()
	response = parseText(message)
	print response

	ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                     body=json.dumps(response))
	ch.basic_ack(delivery_tag = method.delivery_tag)
	print(" --- Finish processing request --- ")

    #-----------------------------------------
    #print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()