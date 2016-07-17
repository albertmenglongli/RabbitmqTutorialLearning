#!/Users/limenglong/.virtualenvs/rabbitmq/bin/python
import pika
import sys
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, queue=self.callback_queue, no_ack=True)

    def on_response(self, ch, method, properties, body):
        if properties.correlation_id == self.correlation_id:
            self.response = body

    def call(self, number):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   body=str(number),
                                   properties=pika.BasicProperties(correlation_id=self.correlation_id,
                                                                   reply_to=self.callback_queue))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


numbers = [int(i) for i in sys.argv[1:]] if len(sys.argv) > 1 else [30]

fibonacci_rpc = FibonacciRpcClient()

for number in numbers:
    print(" [x] Requesting fib(%s)" % number)
    response = fibonacci_rpc.call(number)
    print(" [.] Got %r for %s" % (response, number))
