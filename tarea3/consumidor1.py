#!/usr/bin/env python
import pika
import wikipedia

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_resumen')

def on_request(ch, method, props, body):
    print("Enviando resumen \n")
    wikipedia.set_lang("es")
    response = wikipedia.summary(body.decode(), auto_suggest=False)
    #response = "a"
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_resumen', on_message_callback=on_request)

print("Esperando consulta")
channel.start_consuming()
