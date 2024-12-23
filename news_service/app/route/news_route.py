from flask import Blueprint, request, jsonify, render_template

from news_service.app.repository.elastic_repository import search_articles, search_all_sources, \
    search_real_time_articles
from news_service.app.repository.news_repository import process_and_store_article
from news_service.app.service.map_service import generate_map_for_keywords, generate_map_for_realtime, \
    generate_map_for_results, generate_map_for_combined_search
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


@news_routes.route('/real_time/search', methods=['GET'])
def search_real_time_news():
    try:
        keywords = request.args.get('keywords', '')
        limit = int(request.args.get('limit', 10))

        if not keywords:
            return jsonify({"error": "Missing 'keywords' parameter"}), 400

        results = generate_map_for_realtime(keywords, limit)
        return jsonify(results), 200

    except ValueError as ve:
        return jsonify({"error": f"Invalid parameter value: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



@news_routes.route('/historic/search', methods=['GET'])
def search_historic():
    """
    Endpoint to search for historical articles.
    """
    try:
        keywords = request.args.get('keywords', '')
        limit = int(request.args.get('limit', 10))

        if not keywords:
            return jsonify({"error": "Missing 'keywords' parameter"}), 400

        map_path = generate_map_for_results(keywords, limit, output_file="historic_map.html")
        if not map_path:
            return jsonify({"error": "No valid data found to generate the map."}), 404

        # Return the map URL
        return jsonify({"map_url": f"/{map_path}"})

    except ValueError as ve:
        return jsonify({"error": f"Invalid parameter value: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@news_routes.route('/combined/search', methods=['GET'])
def search_combined():
    """
    Endpoint to search for articles with date filtering.
    """
    try:
        keywords = request.args.get('keywords', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        limit = int(request.args.get('limit', 10))
        # Validate parameters
        print(start_date, end_date)
        if not keywords:
            return jsonify({"error": "Missing 'keywords' parameter"}), 400
        if not start_date or not end_date:
            return jsonify({"error": "Both 'start_date' and 'end_date' parameters are required"}), 400

        # Generate map with results
        result = generate_map_for_combined_search(keywords, start_date, end_date, limit, output_file="combined_map.html")
        if not result:
            return jsonify({"error": "No data found for the given search criteria."}), 404

        # Return the map URL
        return jsonify({"map_url": f"/{result}"})

    except ValueError as ve:
        return jsonify({"error": f"Invalid parameter value: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

