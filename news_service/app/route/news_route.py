from flask import Blueprint, request, jsonify
from news_service.app.service.map_service import generate_map

news_routes = Blueprint('news_routes', __name__)

def validate_and_generate_map(search_type, **kwargs):
    """
    Helper function to validate parameters and generate a map.
    """
    try:
        keywords = kwargs.get('keywords', '')
        limit = kwargs.get('limit', 100)
        start_date = kwargs.get('start_date', '')
        end_date = kwargs.get('end_date', '')

        if not keywords:
            return jsonify({"error": "Missing 'keywords' parameter"}), 400

        if search_type == "combined" and (not start_date or not end_date):
            return jsonify({"error": "Both 'start_date' and 'end_date' parameters are required"}), 400

        map_path = generate_map(search_type, keywords, limit, start_date, end_date, kwargs.get('output_file'))
        if not map_path:
            return jsonify({"error": "No valid data found to generate the map."}), 404

        return jsonify({"map_url": f"/{map_path}"})
    except ValueError as ve:
        return jsonify({"error": f"Invalid parameter value: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@news_routes.route('/keywords/search', methods=['GET'])
def search_keywords():
    return validate_and_generate_map('all',
                                     keywords=request.args.get('keywords', ''),
                                     limit=request.args.get('limit', 100),
                                     output_file='keywords_map.html')

@news_routes.route('/real_time/search', methods=['GET'])
def search_real_time_news():
    return validate_and_generate_map('realtime',
                                     keywords=request.args.get('keywords', ''),
                                     limit=request.args.get('limit', 100),
                                     output_file='realtime_map.html')

@news_routes.route('/historic/search', methods=['GET'])
def search_historic():
    return validate_and_generate_map('historic',
                                     keywords=request.args.get('keywords', ''),
                                     limit=request.args.get('limit', 100),
                                     output_file='historic_map.html')

@news_routes.route('/combined/search', methods=['GET'])
def search_combined():
    return validate_and_generate_map('combined',
                                     keywords=request.args.get('keywords', ''),
                                     start_date=request.args.get('start_date', ''),
                                     end_date=request.args.get('end_date', ''),
                                     output_file='combined_map.html')
