import json
import time
import os
import logging
import pika
import whisper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
QUEUE_TASKS = "ml_tasks"
QUEUE_RESULTS = "ml_results"

logger.info("Loading Whisper model (openai/whisper)...")
model = whisper.load_model("tiny")
logger.info("Whisper model loaded")


def connect_rabbitmq():
    while True:
        try:
            logger.info("Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    heartbeat=600
                )
            )
            logger.info("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            logger.warning("RabbitMQ not ready, retrying in 5s...")
            time.sleep(5)


def transcribe(audio_path: str):
    result = model.transcribe(audio_path)
    text = result["text"]
    duration = result["segments"][-1]["end"] if result["segments"] else 0
    return text, duration


connection = connect_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue=QUEUE_TASKS, durable=True)
channel.queue_declare(queue=QUEUE_RESULTS, durable=True)


def callback(ch, method, properties, body):
    task = json.loads(body)
    logger.info(f"Processing task {task['task_id']}")

    text, duration = transcribe(task["audio_path"])

    result = {
        "task_id": task["task_id"],
        "user_id": task["user_id"],
        "audio_name": task["audio_name"],
        "content": text,
        "duration": duration
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_RESULTS,
        body=json.dumps(result),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_TASKS, on_message_callback=callback)

logger.info("Whisper worker started")
channel.start_consuming()
