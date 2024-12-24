from news_service.app.repository.classification import classify_article, extract_location
from news_service.app.repository.elastic_repository import save_article_to_elastic
from news_service.app.repository.geocoding import get_coordinates
from datetime import datetime

def process_and_store_article(article):
    try:
        title = article.get("title", "")
        body = article.get("body", "")
        raw_date_time = article.get("dateTime", "")
        url = article.get("url", "")
        source = article.get("source", {}).get("title", "Unknown")

        # Normalize the date
        # try:
        #     normalized_date = datetime.strptime(raw_date_time, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
        # except ValueError:
        #     normalized_date = "1970-01-01T00:00:00Z"

        # Classify the article
        category = classify_article(title, body)

        # Extract location and coordinates
        if category in ["Historical Terror Event", "Current Terror Event"]:
            print('this is history or current event')
            location = extract_location(title, body)
            print(f'location: {location}')
            coordinates = get_coordinates(location) if location else {"latitude": None, "longitude": None}
        else:
            location = "Global"
            coordinates = {"latitude": None, "longitude": None}

        processed_article = {
            "title": title,
            "body": body,
            "category": category,
            "location": location,
            "latitude": coordinates.get("latitude"),
            "longitude": coordinates.get("longitude"),
            "dateTime": raw_date_time,
            "url": url,
            "source": source
        }

        save_article_to_elastic(processed_article)
        return processed_article

    except Exception as e:
        print(f"Error processing article: {e}")
        return None



