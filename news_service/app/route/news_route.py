from flask import Blueprint, request, jsonify

from news_service.app.repository.elastic_repository import search_articles
from news_service.app.repository.news_repository import process_and_store_article
from news_service.app.utils.news_api import fetch_articles_from_newsapi

news_routes = Blueprint('news_routes', __name__)

@news_routes.route('/create', methods=['GET'])
def create_news():
    """
    Fetch articles from NewsAPI, process them, and store in ElasticSearch.
    """
    keyword = request.args.get('keyword', 'terror attack')
    page = int(request.args.get('page', 1))

    articles = fetch_articles_from_newsapi(keyword, page)

    processed_articles = []
    for article in articles:
        processed_article = process_and_store_article(article)
        processed_articles.append(processed_article)

    return jsonify({"message": f"Processed and saved {len(processed_articles)} articles."})

@news_routes.route('/search', methods=['POST'])
def search_news_articles():
    """
    Search for articles in ElasticSearch.
    """
    query = request.json.get("query", {"match_all": {}})
    limit = int(request.json.get("limit", 10))

    articles = search_articles(query, limit)
    return jsonify(articles)

@news_routes.route('/keywords/search', methods=['GET'])
def search_keywords():
    """
    Endpoint for searching by keywords (Under construction).
    """
    return jsonify({"message": "Keyword search endpoint under construction"})

@news_routes.route('/historic/search', methods=['GET'])
def search_historic_articles():
    """
    Endpoint for searching historical data (Under construction).
    """
    return jsonify({"message": "Historical data search endpoint under construction"})

@news_routes.route('/combined/search', methods=['GET'])
def combined_search_articles():
    """
    Endpoint for combined search across multiple data sources (Under construction).
    """
    return jsonify({"message": "Combined search endpoint under construction"})
