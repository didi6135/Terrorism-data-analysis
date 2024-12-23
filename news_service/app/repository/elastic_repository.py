import json
import math
from datetime import datetime

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



def search_real_time_articles(keywords, limit=10):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {
                        "query": keywords,
                        "fields": ["title", "body", "location"]
                    }},
                    {"term": {"category": "Current Terror Event"}}
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

def search_historic_articles(keywords, limit=10):
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
                    {"term": {"category": "Historical Terror Event"}}
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


def generate_date_formats(date_str):
    """
    Convert the input date into multiple formats for matching.
    """
    formats = [
        "%Y-%m-%d",  # e.g., 1970-01-03
        "%m/%d/%Y",  # e.g., 1/3/1970
        "%b %d, %Y",  # e.g., Jan 3, 1970
        "%d/%m/%Y"   # e.g., 03/01/1970
    ]
    date_variants = []
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            date_variants.append(parsed_date.strftime(fmt))
        except ValueError:
            pass
    return date_variants

def search_combined_articles(keywords, start_date, end_date, limit=10):
    """
    Search for articles within a date range for a `text`-based `dateTime` field.
    """
    start_formats = generate_date_formats(start_date)
    end_formats = generate_date_formats(end_date)

    # Generate should clauses for all possible date formats
    date_queries = []
    for start, end in zip(start_formats, end_formats):
        date_queries.append({
            "bool": {
                "must": [
                    {"range": {"dateTime": {"gte": start, "lte": end}}}
                ]
            }
        })

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
                "should": date_queries,
                "minimum_should_match": 1
            }
        },
        "_source": ["title", "body", "location", "latitude", "longitude", "dateTime", "source"],
        "size": limit
    }

    try:
        response = get_elastic_client().search(index=ELASTIC_INDEX, body=query)
    except Exception as e:
        print(f"Error querying Elasticsearch: {e}")
        return []

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

print(search_combined_articles(
    keywords="Educational",
    start_date="1/3/1970",
    end_date="1/6/2000"
))

# print(search_historic_articles('Hijacking'))



def sanitize_event(event):
    sanitized_event = {}
    for key, value in event.items():
        if isinstance(value, float) and math.isnan(value):
            sanitized_event[key] = None
        else:
            sanitized_event[key] = value
    return sanitized_event


def insert_new_event_elasticsearch(event):
    event = sanitize_event(event)
    new_event = {
        "title": f"{event.get('attacktype1_txt', 'Unknown')}, {event.get('targtype1_txt', 'Unknown')}, {event.get('gname1', 'Unknown')}",
        "dateTime": event.get('date'),
        "country": f"{event.get('region_txt', 'Unknown')}, {event.get('country_txt', 'Unknown')}, {event.get('city', 'Unknown')}",
        "longitude": event.get('longitude'),
        "latitude": event.get('latitude'),
        "category": "Historical Terror Event",
        "body": event.get('summary', "No summary available"),
    }
    print(new_event)
    try:
        save_article_to_elastic(new_event)
    except Exception as e:
        print(f"Error saving to Elasticsearch: {e}")

