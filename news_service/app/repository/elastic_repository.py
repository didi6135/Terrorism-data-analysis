from news_service.app.db.elastic_search_db import get_elastic_client
from news_service.app.utils.config import ELASTIC_INDEX


def save_article_to_elastic(article):
    try:
        client = get_elastic_client()
        client.index(index=ELASTIC_INDEX, document=article)
    except Exception as e:
        print(f"Error saving to Elasticsearch: {e}")


def search_articles(query, limit=10):
    client = get_elastic_client()
    response = client.search(index=ELASTIC_INDEX, body={"query": query, "size": limit})
    return response['hits']['hits']



