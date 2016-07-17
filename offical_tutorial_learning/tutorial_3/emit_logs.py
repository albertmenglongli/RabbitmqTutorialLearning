#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

import sys

message = ' '.join(sys.argv[1:]) or 'Info: Hello, world!'

channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

connection.close()

print(" [x] Sent %r" % message)
