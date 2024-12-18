import json
import os

from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError

load_dotenv(verbose=True)


def create_producer():
    producer = KafkaProducer(
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer


def producer_send_message(topic, value, key):
    try:
        producer = create_producer()
        future = producer.send(
            topic,
            value=value

        )
        result = future.get(timeout=10)
        producer.flush()
        print(f"Message sent to {topic}: {result}")

    except KafkaError as e:
        print(f"Failed to send message: {e}")
