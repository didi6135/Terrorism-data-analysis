import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv(verbose=True)


def connect_to_elasticsearch():
    es = Elasticsearch(os.environ['ELASTIC_SEARCH_URI'])
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Failed to connect to Elasticsearch")
    return es
