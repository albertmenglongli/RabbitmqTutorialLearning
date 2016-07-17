#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='logs_direct', exchange_type='direct')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='logs_direct', routing_key=severity, queue=queue_name)


def callback(ch, method, properties, body):
    print(' [x] Recieved message: %r %r ' % (body, method.routing_key))


channel.basic_consume(callback, queue=queue_name, no_ack=True)
print(' [x] Start to receive message')
channel.start_consuming()
