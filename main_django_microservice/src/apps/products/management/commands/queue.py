import json

from django.conf import settings
from django.core.management.base import BaseCommand

import pika

from apps.products.models import Product


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        url = settings.RABBITMQ_URL

        params = pika.URLParameters(url)

        connection = pika.BlockingConnection(params)

        channel = connection.channel()

        channel.queue_declare(queue='main')

        def callback(ch, method, properties, body):
            print("Received in main")
            data = json.loads(body)
            print(data)
            print(properties)

            try:
                if properties.content_type == 'product_created':
                    Product.objects.create(
                        id=data['id'],
                        title=data['title'],
                        image=data['image']
                    )
                elif properties.content_type == 'product_updated':
                    product = Product.objects.get(id=data['id'])
                    product.title = data['title']
                    product.image = data['image']
                    product.save()
                elif properties.content_type == 'product_deleted':
                    product = Product.objects.get(id=data)
                    product.delete()
            except Exception as e:
                print("Error processing message", e)

        channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

        print("Started Consuming")

        channel.start_consuming()

        print("Ended Consuming")

        channel.close()
