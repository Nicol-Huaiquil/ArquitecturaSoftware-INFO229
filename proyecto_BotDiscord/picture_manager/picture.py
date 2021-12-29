import os, time
import pika
from googleapiclient.discovery import build
import random

########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="picture", durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="picture")


##########################################################

api_key = "AIzaSyDkoh5OwDDIk0lWVsn781gUhe0vrxaGd_8"
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))

	search = body.decode("UTF-8")
	ran = random.randint(0,9)
	resource = build("customsearch", "v1", developerKey=api_key).cse()
	result = resource.list(
		q=f"{search}", cx="bd4ed8fe7aa378954", searchType="image"
	).execute()
	url = result["items"][ran]["link"]
	result = url
	channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result+" espacio "+search+" espacio "+"result")

channel.basic_consume(
	queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()