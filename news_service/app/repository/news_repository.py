from news_service.app.repository.classification import classify_article, extract_location
from news_service.app.repository.elastic_repository import save_article_to_elastic
from news_service.app.repository.geocoding import get_coordinates


def process_and_store_article(article):
    try:
        # Extract basic fields
        title = article.get("title", "")
        body = article.get("body", "")
        date_time = article.get("dateTime", "")
        url = article.get("url", "")
        source = article.get("source", {}).get("title", "Unknown")

        # Step 1: Classify the article
        category = classify_article(title, body)

        # Step 2: Extract location and coordinates for relevant categories
        if category in ["Historical Terror Event", "Current Terror Event"]:
            location = extract_location(title, body)
            print(f'location: {location}')
            if location:
                coordinates = get_coordinates(location)
            else:
                location = "Global"
                coordinates = {"latitude": None, "longitude": None}
        else:
            location = "Global"
            coordinates = {"latitude": None, "longitude": None}

        # Step 3: Create processed article structure
        processed_article = {
            "title": title,
            "body": body,
            "category": category,
            "location": location,
            "latitude": coordinates.get("latitude"),
            "longitude": coordinates.get("longitude"),
            "dateTime": date_time,
            "url": url,
            "source": source
        }


        print(f"Processed article data: {processed_article}")  # Debugging

        # Step 4: Save to ElasticSearch
        save_article_to_elastic(processed_article)

        return processed_article

    except Exception as e:
        print(f"Error processing article: {e}")
        return None



