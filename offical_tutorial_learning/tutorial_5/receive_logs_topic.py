#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='logs_topic', exchange_type='topic')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

routing_keys = sys.argv[1:]
if not routing_keys:
    sys.stderr.write("Usage: %s [Routing Keys]\n" % sys.argv[0])
    sys.exit(1)

for routing_key in routing_keys:
    channel.queue_bind(exchange='logs_topic', routing_key=routing_key, queue=queue_name)


def callback(ch, method, properties, body):
    print(' [x] Recieved message: %r %r ' % (method.routing_key, body))


channel.basic_consume(callback, queue=queue_name, no_ack=True)
print(' [x] Start to receive message')
channel.start_consuming()
