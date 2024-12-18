import json
from dotenv import load_dotenv
from kafka import KafkaConsumer
from kafka.errors import KafkaError


def create_consumer(topic, bootstrap_servers):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print(f"Consumer created for topic '{topic}''")
        return consumer
    except KafkaError as e:
        print(f"Failed to create Kafka consumer: {e}")
        return None