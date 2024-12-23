import logging
import os

from dotenv import load_dotenv

from Data_Cleaning_Service.app.settings.kafka_settings.producer import producer_send_message

load_dotenv(verbose=True)

def elasticsearch_producer(data: dict):
    try:
        producer_send_message(
            topic=os.environ['ELASTICSEARCH_EVENT_DATA'],
            value=data,

        )
    except Exception as e:
        print(str(e))
        logging.error(str(e))
