import json
import math
from datetime import datetime

from news_service.app.db.elastic_search_db import get_elastic_client
from news_service.app.service.date_service import random_date_between
from news_service.app.service.event_service import sanitize_event
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



def search_all_sources(keywords, limit=100):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": keywords,
                            "fields": ["title", "body", "location"]
                        }
                    }
                ],
                "filter": [
                    { "exists": { "field": "latitude" } },
                    { "exists": { "field": "longitude" } }
                ]
            }
        },
        "_source": ["title", "body", "location", "latitude", "longitude", "dateTime", "source", "category"],
        "size": limit
    }

    try:
        client = get_elastic_client()
        response = client.search(index=ELASTIC_INDEX, body=query)

        # Extract and return results
        results = [
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
            for hit in response["hits"]["hits"]
        ]
        print(f"Results returned: {len(results)}")
        return results
    except Exception as e:
        print(f"Error querying Elasticsearch: {e}")
        return []




def search_real_time_articles(keywords, limit=1000):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                        "query": keywords,
                        "fields": ["title", "body", "location"]
                    }},
                    {
                        "term": {
                            "category.keyword": "Current Terror Event"
                        }
                    }
                ]
            }
        },
        "_source": ["title", "body", "location", "latitude", "longitude", "dateTime", "source", "category"],
        "size": limit
    }

    response = get_elastic_client().search(index=ELASTIC_INDEX, body=query)
    results = [
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
        for hit in response["hits"]["hits"]
    ]
    return results




def search_historic_articles(keywords, limit=1000):
    """
    Perform a search in historical articles based on the given keywords.
    """
    query = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {
                        "query": keywords,
                        "fields": ["title", "body", "location"]
                    }},
                    {"term": {"category.keyword": "Historical Terror Event"}}
                ]
            }
        },
        "_source": ["title", "body", "location", "latitude", "longitude", "dateTime", "source"],
        "size": limit
    }

    response = get_elastic_client().search(index=ELASTIC_INDEX, body=query)
    results = [
        {
            "title": hit["_source"]["title"],
            "body": hit["_source"].get("body", ""),
            "location": hit["_source"].get("location", ""),
            "latitude": hit["_source"].get("latitude", ""),
            "longitude": hit["_source"].get("longitude", ""),
            "dateTime": hit["_source"].get("dateTime", ""),
            "source": hit["_source"].get("source", ""),
        }
        for hit in response["hits"]["hits"]
    ]
    return results


def search_combined_articles(keywords, start_date, end_date):
    """
    Search for articles within a specific date range in ISO 8601 format (e.g., "2024-12-20T21:24:07Z").
    """
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": keywords,
                            "fields": ["title", "body", "location"],

                        }
                    },
                    {
                        "range": {
                            "dateTime": {
                                "gte": start_date,
                                "lte": end_date
                            }
                        }
                    }
                ]
            }
        },
        "_source": ["title", "body", "location", "latitude", "longitude", "dateTime", "source"],
        "size": 1000
    }

    try:
        # Execute the search query
        response = get_elastic_client().search(index=ELASTIC_INDEX, body=query)
        # Format and return the results
        return [
            {
                "title": hit["_source"]["title"],
                "body": hit["_source"].get("body", ""),
                "location": hit["_source"].get("location", ""),
                "latitude": hit["_source"].get("latitude", ""),
                "longitude": hit["_source"].get("longitude", ""),
                "dateTime": hit["_source"].get("dateTime", ""),
                "source": hit["_source"].get("source", ""),
            }
            for hit in response["hits"]["hits"]
        ]
    except Exception as e:
        print(f"Error querying Elasticsearch: {e}")
        return []




def insert_new_event_elasticsearch(event):
    event = sanitize_event(event)

    # Normalize the date or generate a random one
    raw_date = event.get('date')
    if raw_date:
        try:
            normalized_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            normalized_date = random_date_between().strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        normalized_date = random_date_between().strftime("%Y-%m-%dT%H:%M:%SZ")

    new_event = {
        "title": f"{event.get('attacktype1_txt', 'Unknown')}, {event.get('targtype1_txt', 'Unknown')}, {event.get('gname1', 'Unknown')}",
        "dateTime": normalized_date,
        "country": f"{event.get('region_txt', 'Unknown')}, {event.get('country_txt', 'Unknown')}, {event.get('city', 'Unknown')}",
        "longitude": event.get('longitude'),
        "latitude": event.get('latitude'),
        "category": "Historical Terror Event",
        "body": event.get('summary', "No summary available"),
    }

    try:
        save_article_to_elastic(new_event)
    except Exception as e:
        print(f"Error saving to Elasticsearch: {e}")


