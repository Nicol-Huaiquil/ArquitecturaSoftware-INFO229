import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import threading
import pika

from googleapiclient.discovery import build
import random


############ CONEXION RABBITMQ ##############

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channelMQ = connection.channel()

#Creamos el exchange 'cartero' de tipo 'fanout'
channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#############################################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

api_key = "AIzaSyDkoh5OwDDIk0lWVsn781gUhe0vrxaGd_8"

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    for channel in bot.get_all_channels():
        print(channel)
        print(channel.id)

    channel = bot.get_channel(913706828502814760)
    await channel.send('¡Hola!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'pizza' or message.content == 'cerveza' or message.content == 'donuts':
        response = "!mmm..."+message.content+"!"
        await message.channel.send(response)

    await bot.process_commands(message)

@bot.command(name='birthday', help='Muestra el cumpleaños de lo que se pasa en el parametro. Ejemplo: !birthday MatthieuVernier')
async def cumpleaños(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)

    channelMQ.basic_publish(exchange='cartero', routing_key="birthday", body=message)

@bot.command(name='add-birthday', help='Añade un cumpleaños. Ejemplo: !birthday MatthieuVernier 1985-02-13')
async def cumpleaños(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="birthday", body=message)

@bot.command(name='picture', help='Muestra la imagen que se pasa en el parametro. Ejemplo: !picture bosque')
async def showpic(ctx, *, search):
    message =  search
    print("send a new mesage to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="picture", body=message)

"""
@bot.command(name='picture', help='Muestra la imagen que se pasa en el parametro. Ejemplo: !picture bosque')
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="bd4ed8fe7aa378954", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Resuldado de ({search})")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)
"""

############ CONSUMER ###############

import threading
import asyncio

def writer(bot):
    """thread worker function"""
    print('Worker')

    HOST = os.environ['RABBITMQ_HOST']

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channelMQ = connection.channel()

    #Creamos el exchange 'cartero' de tipo 'fanout'
    channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

    #Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
    result = channelMQ.queue_declare(queue="discord_writer", durable=True)
    queue_name = result.method.queue

    #La cola se asigna a un 'exchange'
    channelMQ.queue_bind(exchange='cartero', queue=queue_name, routing_key="discord_writer")


    print(' [*] Waiting for messages. To exit press CTRL+C')

    async def write(message):
        channel = bot.get_channel(908505071887732768) #ID canal de texto INFO104_2021
        if(message.find("result") != (-1)):
            search = message.split(" espacio ")
            embed1 = discord.Embed(title=f"Resuldado de {search[1]}")
            embed1.set_image(url=search[0])
            await channel.send(embed=embed1)
        else:
            await channel.send(message)

    def callback(ch, method, properties, body):
        message=body.decode("UTF-8")
        print(message)

        bot.loop.create_task(write(message))

    channelMQ.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channelMQ.start_consuming()

t = threading.Thread(target=writer, args=[bot])
t.start()

########################################
bot.run(TOKEN)