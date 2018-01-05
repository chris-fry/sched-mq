#!/usr/bin/env python
import pika

host = 'localhost'
queue = 'employee'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue=queue)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue=queue,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
