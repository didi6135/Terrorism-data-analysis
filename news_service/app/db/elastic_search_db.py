from elasticsearch import Elasticsearch


def get_elastic_client():
    return Elasticsearch(
        hosts=["http://localhost:9200"],
        basic_auth=("elastic", "3uDiv6AS"),
        verify_certs=False,
    )

def create_index(index_name, mapping):
    client = get_elastic_client()
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")


news_mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "body": {"type": "text"},
            "category": {"type": "keyword"},
            "dateTime": {"type": "date"},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "url": {"type": "keyword"}
        }
    }
}

index_name = "news_articles"


