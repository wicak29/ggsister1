#!/usr/bin/env python
import pika
import json
from customParser import parseText
import os

os.chdir("log")

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):

    print(" --- Receive request --- ")
    fileName = body

    message = open(fileName, 'r').read()

    response = parseText(message)
    print response

    print(" --- Send result back to the manager --- ")

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(" --- Finish processing request --- ")

    print(" [x] Awaiting requests")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting requests")
channel.start_consuming()
