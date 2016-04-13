#!/usr/bin/env python
import pika
import os
import glob
import json
import sys
from customParser import parseText

os.chdir("log")
credentials = pika.PlainCredentials('ggsister', 'ggsister')
parameters = pika.ConnectionParameters('10.151.36.37',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='logs_manager', type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs_manager',queue=queue_name)

# #channel 2
# channel2 = connection.channel()
# channel.exchange_declare(exchange='hasil', type='direct')
# channel.basic_publish(exchange='hasil', routing_key='c', body=)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(" --- Receive request --- ")
	message = body
	response = parseText(message)
	print response

	# ch.basic_publish(exchange='',
 #                     routing_key=properties.reply_to,
 #                     properties=pika.BasicProperties(correlation_id = \
 #                                                         properties.correlation_id),
 #                     body=json.dumps(response))
	# ch.basic_ack(delivery_tag = method.delivery_tag)
	print(" --- Finish processing request --- ")

	# connection.close()
	connection = pika.BlockingConnection(parameters)
	channel2 = connection.channel()
	channel2.exchange_declare(exchange='result_manager', type='direct')
	channel2.basic_publish(exchange='result_manager', routing_key='c', body=json.dumps(response))
    #print(" [x] %r" % body)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

try:
    channel.start_consuming()

except KeyboardInterrupt:
    sys.exit(1)