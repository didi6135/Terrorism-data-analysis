from flask import Blueprint, request, jsonify, render_template

from news_service.app.repository.elastic_repository import search_articles, search_all_sources
from news_service.app.repository.news_repository import process_and_store_article
from news_service.app.service.map_service import generate_map_for_keywords
from news_service.app.utils.news_api import fetch_articles_from_newsapi

news_routes = Blueprint('news_routes', __name__)



@news_routes.route('/keywords/search', methods=['GET'])
def search_keywords():
    try:
        keywords = request.args.get('keywords', '')
        limit = int(request.args.get('limit', 10))

        if not keywords:
            return jsonify({"error": "Missing 'keywords' parameter"}), 400

        map_path = generate_map_for_keywords(keywords, limit)
        if map_path:
            # Return the relative path to the static map
            return jsonify({"map_url": f"/static/maps/{map_path.split('/')[-1]}"})
        else:
            return jsonify({"error": "Map generation failed"}), 500

    except ValueError as ve:
        # Handle issues like invalid limit (e.g., non-integer)
        return jsonify({"error": f"Invalid parameter value: {str(ve)}"}), 400
    except Exception as e:
        # Catch unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



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
