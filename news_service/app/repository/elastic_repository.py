import json

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


def search_all_sources(keywords, limit=10):
    query = {
        "query": {
            "multi_match": {
                "query": keywords,
                "fields": ["title", "body", "location"]
            }
        },
        "_source": ["title", "body", "location", 'latitude', 'longitude', "dateTime", "source", "category"],
        "size": 1000  # Set a batch size for scrolling
    }

    client = get_elastic_client()
    response = client.search(index=ELASTIC_INDEX, body=query, scroll="2m")  # Initialize the scroll

    scroll_id = response["_scroll_id"]
    hits = response["hits"]["hits"]

    results = []

    # Collect results from the first batch
    results.extend([
        {
            "title": hit["_source"]["title"],
            "body": hit["_source"].get("body", ""),
            "location": hit["_source"].get("location", ""),
            "latitude": hit["_source"].get("latitude", ""),
            "longitude": hit["_source"].get("longitude", ""),
            "dateTime": hit["_source"].get("dateTime", ""),
            "source": hit["_source"].get("source", ""),
            "category": hit["_source"].get("category", ""),
        }
        for hit in hits
    ])

    # Continue scrolling until no hits are returned
    while len(hits) > 0 and len(results) < limit:
        response = client.scroll(scroll_id=scroll_id, scroll="2m")
        scroll_id = response["_scroll_id"]
        hits = response["hits"]["hits"]

        results.extend([
            {
                "title": hit["_source"]["title"],
                "body": hit["_source"].get("body", ""),
                "location": hit["_source"].get("location", ""),
                "latitude": hit["_source"].get("latitude", ""),
                "longitude": hit["_source"].get("longitude", ""),
                "dateTime": hit["_source"].get("dateTime", ""),
                "source": hit["_source"].get("source", ""),
                "category": hit["_source"].get("category", ""),
            }
            for hit in hits
        ])

    # Cleanup the scroll context
    client.clear_scroll(scroll_id=scroll_id)

    # Return only the requested number of results
    return results[:limit]



