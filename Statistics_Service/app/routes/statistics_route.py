import json

from flask import Blueprint, jsonify, request, send_file

from Statistics_Service.app.db.redis_db import redis_client
from Statistics_Service.app.repository.attack_type_repository import analyze_attack_target_correlation, \
    get_most_deadly_attack_types

from Statistics_Service.app.repository.group_repository import  get_top_5_groups_by_casualties

from Statistics_Service.app.services.plot_service import plot_monthly_trends, \
    plot_yearly_trends, plot_groups_by_target_type
from Statistics_Service.app.services.visualization_service import \
    generate_heatmap, generate_top_groups_map, generate_map_for_victims_analysis \
    , generate_attack_strategy_map, \
    generate_shared_event_groups_map, create_shared_target_map, create_intergroup_activity_map

statistics_bp = Blueprint("statistics", __name__)


def get_cached_data(cache_key):
    """Retrieve cached data from Redis."""
    cached_data = redis_client.get(cache_key)
    return json.loads(cached_data) if cached_data else None

def set_cache_data(cache_key, data, expiration=3600):
    """Set data in Redis with an expiration time."""
    redis_client.setex(cache_key, expiration, json.dumps(data))


@statistics_bp.route("/most_deadly_attack_types", methods=["GET"])
def most_deadly_attack_types():
    try:
        limit = request.args.get("limit", type=int, default=10)

        cache_key = f"most_deadly_attack_types:{limit}"
        cached_data = redis_client.get(cache_key)
        # cached_data = get_cached_data(cache_key)

        if cached_data:
            return jsonify({"data": json.loads(cached_data)}), 200

        attack_types = get_most_deadly_attack_types(limit)
        set_cache_data(cache_key, attack_types)

        redis_client.setex(cache_key, 3600, json.dumps(attack_types))
        return jsonify({"data": attack_types}), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch most deadly attack types",
            "message": str(e)
        }), 500


@statistics_bp.route('/avg_injured_by_origen', methods=["GET"])
def get_avg_injured_by_origen():
    try:
        region_id = request.args.get("region_id")
        limit = request.args.get("limit", type=int)

        if not region_id:
            return jsonify({"error": "Missing 'region_id' parameter"}), 400

        cache_key = f"avg_injured:{region_id}:{limit}"
        if cached := redis_client.get(cache_key):
            return jsonify(json.loads(cached)), 200

        result = {"map_file": generate_map_for_victims_analysis('region', region_id, limit)}
        redis_client.setex(cache_key, 3600, json.dumps(result))
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Failed to calculate average victims", "message": str(e)}), 500


@statistics_bp.route('/avg_injured_by_country', methods=["GET"])
def get_avg_injured_by_country():
    try:
        country_id = request.args.get("country_id")
        limit = request.args.get("limit", type=int)

        if not country_id:
            return jsonify({"error": "Missing 'country_id' parameter"}), 400

        cache_key = f"avg_injured:country:{country_id}:{limit}"
        if cached := redis_client.get(cache_key):
            return jsonify(json.loads(cached)), 200

        result = {"map_file": generate_map_for_victims_analysis('country', country_id, limit)}
        redis_client.setex(cache_key, 3600, json.dumps(result))
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Failed to calculate average victims", "message": str(e)}), 500


@statistics_bp.route('/avg_injured_by_city', methods=["GET"])
def get_avg_injured_by_city():
    try:
        city_id = request.args.get("city_id")
        limit = request.args.get("limit", type=int)

        if not city_id:
            return jsonify({"error": "Missing 'city_id' parameter"}), 400

        cache_key = f"avg_injured:city:{city_id}:{limit}"
        if cached := redis_client.get(cache_key):
            return jsonify(json.loads(cached)), 200

        result = {"map_file": generate_map_for_victims_analysis('city', city_id, limit)}
        redis_client.setex(cache_key, 3600, json.dumps(result))
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Failed to calculate average victims", "message": str(e)}), 500


@statistics_bp.route("/top_5_group_most_casualties", methods=["GET"])
def top_groups_by_casualties():
    """
    Returns the top 5 groups with the highest casualties.
    """
    try:
        cache_key = "top_5_groups_casualties"
        if cached := redis_client.get(cache_key):
            return jsonify({"data": json.loads(cached)}), 200

        data = get_top_5_groups_by_casualties()
        redis_client.setex(cache_key, 3600, json.dumps(data))  # Cache for 1 hour
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch top groups by casualties", "message": str(e)}), 500


@statistics_bp.route("/attack_target_correlation", methods=["GET"])
def get_attack_target_correlation():
    try:
        cache_key = "attack_target_correlation"
        if cached := redis_client.get(cache_key):
            return jsonify({"correlation": json.loads(cached)}), 200

        data = analyze_attack_target_correlation()
        redis_client.setex(cache_key, 3600, json.dumps(data))  # Cache for 1 hour
        return jsonify({"correlation": data}), 200
    except Exception as e:
        return jsonify({"error": "Failed to calculate correlation", "message": str(e)}), 500


@statistics_bp.route('/event_trends_for_all_years', methods=["GET"])
def get_event_trends_for_all_years():
    try:
        cache_key = "event_trends_all_years"
        if cached := redis_client.get(cache_key):
            return jsonify({"plot_file": json.loads(cached)}), 200

        plot_file = plot_yearly_trends()
        redis_client.setex(cache_key, 3600, json.dumps(plot_file))
        return jsonify({"plot_file": plot_file}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate trends", "message": str(e)}), 500


@statistics_bp.route('/event_trends_for_specific_year', methods=["GET"])
def get_event_trends_for_specific_year():
    try:
        year_id = request.args.get("year_id", type=int)
        if not year_id:
            return jsonify({"error": "Missing 'year_id' parameter"}), 400

        cache_key = f"monthly_trends:{year_id}"
        if cached := redis_client.get(cache_key):
            return jsonify({"plot_file": json.loads(cached)}), 200

        plot_file = plot_monthly_trends(year_id)
        redis_client.setex(cache_key, 3600, json.dumps(plot_file))  # Cache for 1 hour
        return jsonify({"plot_file": plot_file}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate trends", "message": str(e)}), 500


@statistics_bp.route("/most_active_group_by_some_region_or_all_region", methods=["GET"])
def get_top_groups_map():
    try:
        region_id = request.args.get("region_id", type=int)
        cache_key = f"top_groups_map:{region_id or 'all'}"

        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        map_file_path = generate_top_groups_map(region_id)
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))
        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route('/top_group_with_shared_target_by_region', methods=["GET"])
def top_group_with_shared_target_by_region():
    try:
        region_id = request.args.get("region_id", type=int)
        if not region_id:
            return jsonify({"error": "region_id must be provided"}), 400

        cache_key = f"shared_target_map:{region_id}"
        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        map_file_path = create_shared_target_map(region_id, 'region')
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))  # Cache for 1 hour
        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route('/top_group_with_shared_target_by_country', methods=["GET"])
def top_group_with_shared_target_by_country():
    try:
        country_id = request.args.get("country_id", type=int)
        if not country_id:
            return jsonify({"error": "country_id must be provided"}), 400

        cache_key = f"shared_target_map:country:{country_id}"
        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        map_file_path = create_shared_target_map(country_id, 'country')
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))  # Cache for 1 hour
        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500
####################################################################






@statistics_bp.route('/attack_strategy_map_region', methods=["GET"])
def attack_strategy_map():
    try:
        region_id = request.args.get("region_id", type=int)
        cache_key = f"attack_strategy_map:region{region_id or 'all'}"

        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        map_file_path = generate_attack_strategy_map(entity_id=region_id, entity_type="region")
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))  # Cache for 1 hour
        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500




@statistics_bp.route('/attack_strategy_map_country', methods=["GET"])
def attack_strategy_map_by_country():
    try:
        country_id = request.args.get("country_id", type=int)
        if not country_id:
            return jsonify({"error": "country_id must be provided"}), 400

        cache_key = f"attack_strategy_map:country:{country_id}"
        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        # Generate and save map
        map_file_path = generate_attack_strategy_map(entity_id=country_id, entity_type="country")
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))  # Cache for 1 hour

        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500



@statistics_bp.route('/unique_group_by_region', methods=["GET"])
def intergroup_activity_map_by_region():
    try:
        region_id = request.args.get("region_id", type=int)
        if not region_id:
            return jsonify({"error": "region_id is required"}), 400

        cache_key = f"intergroup_activity_map:region:{region_id}"
        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        map_file_path = create_intergroup_activity_map(region_id, "region")
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))  # Cache for 1 hour

        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route('/unique_group_by_country', methods=["GET"])
def intergroup_activity_map_by_country():
    try:
        country_id = request.args.get("country_id", type=int)
        if not country_id:
            return jsonify({"error": "country_id is required"}), 400

        cache_key = f"intergroup_activity_map:country:{country_id}"
        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        map_file_path = create_intergroup_activity_map(country_id, "country")
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))  # Cache for 1 hour

        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500




@statistics_bp.route('/shared_event_groups_map', methods=["GET"])
def shared_event_groups_map():
    try:
        cache_key = "shared_event_groups_map"
        if cached := redis_client.get(cache_key):
            return jsonify({"map_file": json.loads(cached)}), 200

        map_file_path = generate_shared_event_groups_map()
        redis_client.setex(cache_key, 3600, json.dumps(map_file_path))  # Cache for 1 hour

        return jsonify({"map_file": map_file_path}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route('/groups_with_prefer_target_type', methods=["GET"])
def groups_by_target_type_plot():
    try:
        target_type_id = request.args.get("target_type_id", type=int)
        if not target_type_id:
            return jsonify({"error": "target_type_id is required"}), 400

        cache_key = f"groups_by_target_type_plot:{target_type_id}"
        if cached := redis_client.get(cache_key):
            return jsonify({"plot_file": json.loads(cached)}), 200

        plot_file = plot_groups_by_target_type(target_type_id)
        redis_client.setex(cache_key, 3600, json.dumps(plot_file))  # Cache for 1 hour

        return jsonify({"plot_file": plot_file}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate plots", "message": str(e)}), 500

##############################################



@statistics_bp.route("/heatmap", methods=["GET"])
def get_heatmap():
    """
    Endpoint to generate and return the heatmap.
    """
    try:
        # Generate the heatmap
        map_file = generate_heatmap()

        # Serve the map file
        return send_file(map_file, as_attachment=False)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to generate heatmap", "message": str(e)}), 500









