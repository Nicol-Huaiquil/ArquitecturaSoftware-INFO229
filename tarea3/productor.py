#!/usr/bin/env python
import pika
import uuid

class wikipediaClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call1(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_resumen',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

    def call2(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_contador',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)


mwikipedia = wikipediaClient()
mensaje = input("Escriba mensaje a buscar en Wikipedia: ")

print("Enviando mensaje")
response1 = mwikipedia.call1(mensaje)
response2 = mwikipedia.call2(mensaje)
print("Resumen:\n %r \n" % response1)
print("Contador: %r" % response2)
