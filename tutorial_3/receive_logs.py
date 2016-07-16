#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)


def callback(ch, method, properties, body):
    print(' [x] Recieved message: %r ' % body)


channel.basic_consume(callback, queue=queue_name, no_ack=True)
print(' [x] Start to receive message')
channel.start_consuming()
