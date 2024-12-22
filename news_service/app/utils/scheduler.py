import schedule
import time
from news_service.app.utils.news_api import fetch_articles_from_newsapi
from news_service.app.repository.news_repository import process_and_store_article

def fetch_and_process_news():
    """
    Fetch articles from NewsAPI, process them, and store in ElasticSearch.
    """
    try:
        keyword = "terror attack"
        page = 1

        print("Fetching news articles...")
        articles = fetch_articles_from_newsapi(keyword, page)

        processed_articles = []
        for article in articles:
            processed_article = process_and_store_article(article)
            processed_articles.append(processed_article)

        print(f"Processed and saved {len(processed_articles)} articles.")
    except Exception as e:
        print(f"Error fetching or processing articles: {e}")

# Schedule the task every 2 minutes
schedule.every(2).minutes.do(fetch_and_process_news)

