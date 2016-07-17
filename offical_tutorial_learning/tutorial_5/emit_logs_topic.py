#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs_topic', exchange_type='topic')

import sys

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello, world!'

channel.basic_publish(exchange='logs_topic',
                      routing_key=routing_key,
                      body=message)

connection.close()

print(" [x] Sent %r: %r" % (routing_key, message))
