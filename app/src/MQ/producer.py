import json
import pika

RABBIT_URL = "amqp://guest:guest@rabbitmq:5672/"

def publish_task(task: dict):
    connection = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
    channel = connection.channel()

    channel.queue_declare(queue="ml_tasks", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="ml_tasks",
        body=json.dumps(task),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
