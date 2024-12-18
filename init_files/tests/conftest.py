import pytest
from elastic_transport import SecurityWarning
from elasticsearch import Elasticsearch
import warnings


warnings.filterwarnings("ignore", category=SecurityWarning)


@pytest.fixture(scope="module")
def es_client():
   client = Elasticsearch(
       ['http://localhost:9200'],
       basic_auth=("elastic", "123456"),
       verify_certs=False
   )
   yield client
   client.close()
