#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs_direct', exchange_type='direct')

import sys

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Info: Hello, world!'

channel.basic_publish(exchange='logs_direct',
                      routing_key=severity,
                      body=message)

connection.close()

print(" [x] Sent %r: %r" % (severity, message))
