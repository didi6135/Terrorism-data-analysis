import logging
import os
from dotenv import load_dotenv
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, KafkaError

# Load environment variables
load_dotenv(verbose=True)

def init_topics():
    """
    Initializes Kafka topics based on environment variables.
    Creates topics if they do not already exist.
    """
    # Configure logging
    logging.basicConfig(
        filename='kafka_init.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Load Kafka settings from environment variables
    bootstrap_servers = os.environ.get('BOOTSTRAP_SERVERS')
    partitions_num = int(os.environ.get('PARTITIONS_NUM', 1))
    replication_num = int(os.environ.get('REPLICATION_NUM', 1))

    topics_name = [
        os.environ['ELASTICSEARCH_EVENT_DATA']

    ]

    # Filter out empty topic names
    topics_name = [topic for topic in topics_name if topic]

    # Prepare NewTopic objects
    topics = [
        NewTopic(
            name=topic_name.strip(),
            num_partitions=partitions_num,
            replication_factor=replication_num
        )
        for topic_name in topics_name
    ]

    client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    try:
        # Initialize Kafka admin client
        logging.info("KafkaAdminClient initialized successfully.")

        # Create topics
        response = client.create_topics(new_topics=topics, validate_only=False)
        logging.info(f"Topics created successfully: {response}")
        print(f"Topics created successfully: {response}")

    except TopicAlreadyExistsError as e:
        # Handle specific case where topics already exist
        logging.warning("Some topics already exist.")
        print("Warning: Some topics already exist.")
        logging.warning(e)

    except KafkaError as e:
        # Handle other Kafka-related errors
        logging.error(f"Kafka error: {str(e)}")
        print(f"Kafka error: {str(e)}")

    except Exception as e:
        # Catch all other errors
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

    finally:
        # Ensure the client is closed properly
        client.close()
        logging.info("KafkaAdminClient closed.")