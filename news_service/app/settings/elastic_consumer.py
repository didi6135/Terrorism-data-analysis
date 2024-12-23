import os
from dotenv import load_dotenv

from news_service.app.repository.elastic_repository import insert_new_event_elasticsearch
from news_service.app.settings.consumer import create_consumer

load_dotenv(verbose=True)
topic = os.environ['ELASTICSEARCH_EVENT_DATA']
bootstrap_servers = os.environ['BOOTSTRAP_SERVERS']

def get_event_from_data_cleaning_consumer():
    consume = create_consumer(topic, bootstrap_servers)

    for message in consume:
        try:
            insert_new_event_elasticsearch(message.value)
            print(f'Received- {message.key}: {message.value}')
        except Exception as e:
            print(f"Failed to insert message: {e}")
            continue
