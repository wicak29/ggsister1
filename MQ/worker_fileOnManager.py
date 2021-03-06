#worker file - file On Manager
#!/usr/bin/env python
from customParser import parseText
import pika
import json

credentials = pika.PlainCredentials('ggsister', 'ggsister')
parameters = pika.ConnectionParameters('10.151.36.37',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='fileOnManager')


def on_request(ch, method, props, body):
    n = body

    response = parseText(n)
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
channel.basic_consume(on_request, queue='fileOnManager')

print(" [x] Awaiting RPC requests")
channel.start_consuming()