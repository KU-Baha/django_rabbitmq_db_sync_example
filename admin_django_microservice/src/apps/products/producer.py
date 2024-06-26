import json

import pika
from django.conf import settings

url = settings.RABBITMQ_URL

params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange="", routing_key="main", body=json.dumps(body), properties=properties)
