import json
import logging
import pika
import time

from src.DataBase.engine import SessionLocal
from src.DataBase.models import AudioScript
from src.Balance.balance import BalanceRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_HOST = "rabbitmq"
QUEUE_RESULTS = "ml_results"


def connect():
    while True:
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
        except pika.exceptions.AMQPConnectionError:
            logger.warning("RabbitMQ not ready, retrying...")
            time.sleep(5)


def callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info(f"Saving result for task {data['task_id']}")

    session = SessionLocal()

    try:
        balance_repo = BalanceRepository(session)
        cost = int(data["duration"]) * 10

        if not balance_repo.has_enough_credits(data["user_id"], cost):
            raise Exception(f"Not enough balance, required {cost} credits")
        script = AudioScript(
            user_id=data["user_id"],
            audio_name=data["audio_name"],
            duration=data["duration"],
            content=data["content"]
        )
        session.add(script)
        balance_repo.decrease_balance(
            user_id=data["user_id"],
            amount=cost
        )

        session.commit()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        session.rollback()
        logger.exception(e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    finally:
        session.close()


def start_result_consumer():
    connection = connect()
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_RESULTS, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=QUEUE_RESULTS,
        on_message_callback=callback
    )

    logger.info("Result consumer started")
    channel.start_consuming()
