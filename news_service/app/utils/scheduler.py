import schedule
import time
from news_service.app.utils.news_api import fetch_articles_from_newsapi
from news_service.app.repository.news_repository import process_and_store_article

# Global variable to keep track of the current page
articles_page = 3


def fetch_and_process_news():
    """
    Fetch articles from NewsAPI, process them, and store in ElasticSearch.
    """
    global articles_page  # Access the global variable
    try:
        keyword = "terror attack"

        print(f"Fetching news articles from page {articles_page}...")
        articles = fetch_articles_from_newsapi(keyword, articles_page)

        if not articles:
            print(f"No more articles found on page {articles_page}. Restarting from page 1.")
            articles_page = 1  # Reset to the first page
            return

        processed_articles = []
        for article in articles:
            processed_article = process_and_store_article(article)
            processed_articles.append(processed_article)

        print(f"Processed and saved {len(processed_articles)} articles.")

        # Increment the page for the next batch
        articles_page += 1

    except Exception as e:
        print(f"Error fetching or processing articles: {e}")




