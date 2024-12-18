import os

from dotenv import load_dotenv
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


load_dotenv(verbose=True)

def init_topics():
    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])

    topics_name = [

    ]

    topics = [
        NewTopic(
        name=topic_name.strip(),
        num_partitions=int(os.environ['PARTITIONS_NUM']),
        replication_factor=int(os.environ['REPLICATION_NUM'])
        )
        for topic_name in topics_name
    ]

    try:
        client.create_topics(topics)

    except TopicAlreadyExistsError as e:
        print(str(e))

    client.close()

init_topics()


