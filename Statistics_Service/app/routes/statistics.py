from flask import Blueprint, jsonify, request, send_file

from Statistics_Service.app.repository.attack_type_repository import analyze_attack_target_correlation, \
    get_most_deadly_attack_types
from Statistics_Service.app.repository.city_repository import get_all_cities, calculate_average_victims_by_city
from Statistics_Service.app.repository.country_repository import get_all_countries, \
    calculate_average_victims_by_country
from Statistics_Service.app.repository.event_repository import get_event_trends_cleaned, get_monthly_trends, \
    get_yearly_trends, get_all_years_repo
from Statistics_Service.app.repository.group_repository import get_most_deadly_repo, get_top_5_groups_by_casualties
from Statistics_Service.app.repository.region_repository import get_all_regions, \
    calculate_average_victims_per_event_in_region
from Statistics_Service.app.services.plot_service import plot_monthly_trends, \
    plot_yearly_trends
from Statistics_Service.app.services.visualization_service import generate_map_file, generate_top_countries_map, \
    generate_heatmap, generate_top_groups_map, generate_map_for_victims_analysis, create_shared_target_map_by_region, \
    create_shared_target_map_by_country, generate_attack_strategy_map, generate_attack_strategy_map_by_country, \
    create_intergroup_activity_map_by_country, create_intergroup_activity_map_by_region, \
    generate_shared_event_groups_map

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.route("/most_deadly_attack_types", methods=["GET"])
def most_deadly_attack_types():

    try:
        top_5 = request.args.get("limit")
        print(top_5)
        limit = 5 if top_5 is None else int(top_5)

        attack_types = get_most_deadly_attack_types(limit)

        # Return the data as JSON
        return jsonify({"data": attack_types}), 200

    except Exception as e:
        # Handle errors and return a 500 response with an error message
        return jsonify({
            "error": "Failed to fetch most deadly attack types",
            "message": str(e)
        }), 500
##############################################
@statistics_bp.route("/regions", methods=["GET"])
def get_regions():
    try:
        regions = get_all_regions()
        return jsonify({"regions": regions}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch regions", "message": str(e)}), 500

@statistics_bp.route("/countries", methods=["GET"])
def get_countries():
    try:
        # region_id = request.args.get("region_id")
        countries = get_all_countries()
        return jsonify({"countries": countries}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch countries", "message": str(e)}), 500

@statistics_bp.route("/cities", methods=["GET"])
def get_cities():
    try:
        cities = get_all_cities()
        return jsonify({"cities": cities}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch cities", "message": str(e)}), 500

@statistics_bp.route('/avg_injured_by_origen', methods=["GET"])
def get_avg_injured_by_origen():
    try:
        origen_id = request.args.get("region_id")
        limit = request.args.get("limit")
        data = calculate_average_victims_per_event_in_region(origen_id, limit)
        if not data:
            return jsonify({"error": "No data found"}), 404

        map_file = generate_map_for_victims_analysis(data)
        return jsonify({"map_file": map_file}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to calculate average victims", "message": str(e)}), 500

@statistics_bp.route('/avg_injured_by_country', methods=["GET"])
def get_avg_injured_by_country():
    try:
        country_id = request.args.get("country_id")
        limit = request.args.get("limit")
        data = calculate_average_victims_by_country(country_id, limit)
        if not data:
            return jsonify({"error": "No data found"}), 404

        map_file = generate_map_for_victims_analysis(data)
        return jsonify({"map_file": map_file}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to calculate average victims", "message": str(e)}), 500

@statistics_bp.route('/avg_injured_by_city', methods=["GET"])
def get_avg_injured_by_city():
    try:
        city_id = request.args.get("city_id")
        limit = request.args.get("limit")
        data = calculate_average_victims_by_city(city_id, limit)
        if not data:
            return jsonify({"error": "No data found"}), 404

        map_file = generate_map_for_victims_analysis(data)
        return jsonify({"map_file": map_file}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to calculate average victims", "message": str(e)}), 500


@statistics_bp.route("/top_5_group_most_casualties", methods=["GET"])
def top_groups_by_casualties():
    """
    Returns the top 5 groups with the highest casualties.
    """
    try:
        top_groups = get_top_5_groups_by_casualties()
        return jsonify({"data": top_groups}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch top groups by casualties", "message": str(e)}), 500


@statistics_bp.route("/attack_target_correlation", methods=["GET"])
def get_attack_target_correlation():
    try:
        correlation_data = analyze_attack_target_correlation()

        return jsonify({"correlation": correlation_data}), 200
    except Exception as e:
        return jsonify({"error": "Failed to calculate correlation", "message": str(e)}), 500


@statistics_bp.route('/years', methods=["GET"])
def get_all_years():
    try:
        all_years = get_all_years_repo()
        return jsonify(all_years), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch all years", "message": str(e)}), 500


@statistics_bp.route('/event_trends_for_all_years', methods=["GET"])
def get_event_trends_for_all_years():
    try:

        yearly_df = get_yearly_trends()
        plot_file = plot_yearly_trends(yearly_df)
        return jsonify({
            "plot_file": plot_file
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate trends", "message": str(e)}), 500

@statistics_bp.route('/event_trends_for_specific_year', methods=["GET"])
def get_event_trends_for_specific_year():
    try:
        year_id = request.args.get("year_id", type=int)

        monthly_df = get_monthly_trends(year_id)
        plot_file = plot_monthly_trends(monthly_df, year_id)
        return jsonify({
            "plot_file": plot_file
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate trends", "message": str(e)}), 500


@statistics_bp.route("/most_active_group_by_some_region_or_all_region", methods=["GET"])
def get_top_groups_map():
    try:
        region_id = request.args.get("region_id", type=int)

        # Define the file path for saving the map
        map_file_path = "static/maps/top_groups_map.html"

        map_object = generate_top_groups_map(region_id)
        map_object.save(map_file_path)


        return jsonify({
            "map_file": map_file_path
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500

@statistics_bp.route('/top_group_with_shared_target_by_region', methods=["GET"])
def top_group_with_shared_target_by_region():
    try:
        # Extract region_id or country_id from the request
        region_id = request.args.get("region_id", type=int)

        # Define the file path for saving the map
        map_file_path = "static/maps/top_groups_shared_target_map.html"

        # Generate the map based on the region or country
        if region_id:
            map_object = create_shared_target_map_by_region(region_id)
        else:
            return jsonify({"error": "Either region_id or country_id must be provided"}), 400

        # Save the map as an HTML file
        map_object.save(map_file_path)

        # Return the map file path to the client
        return jsonify({
            "map_file": map_file_path
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500

@statistics_bp.route('/top_group_with_shared_target_by_country', methods=["GET"])
def top_group_with_shared_target_by_country():
    try:
        # Extract country_id
        country_id = request.args.get("country_id", type=int)
        # Define the file path for saving the map
        map_file_path = "static/maps/top_groups_shared_target_map.html"

        # Generate the map based on the region or country
        if country_id:
            map_object = create_shared_target_map_by_country(country_id)
        else:
            return jsonify({"error": "country_id must be provided"}), 400

        # Save the map as an HTML file
        map_object.save(map_file_path)

        # Return the map file path to the client
        return jsonify({
            "map_file": map_file_path
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route('/attack_strategy_map_region', methods=["GET"])
def attack_strategy_map():
    try:
        region_id = request.args.get("region_id", type=int)

        # יצירת מפה ושמירה בקובץ
        map_file_path = "static/maps/attack_strategy_map.html"
        map_object = generate_attack_strategy_map(region_id)
        map_object.save(map_file_path)

        # החזרת נתיב המפה ללקוח
        return jsonify({
            "map_file": map_file_path
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500



@statistics_bp.route('/attack_strategy_map_country', methods=["GET"])
def attack_strategy_map_by_country():
    try:
        country_id = request.args.get("country_id", type=int)
        print(country_id)
        map_file_path = "static/maps/attack_strategy_map_by_country.html"
        map_object = generate_attack_strategy_map_by_country(country_id)
        map_object.save(map_file_path)

        return jsonify({
            "map_file": map_file_path
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route('/unique_group_by_region', methods=["GET"])
def intergroup_activity_map_by_region():
    try:
        # Get the region ID from the request
        region_id = request.args.get("region_id", type=int)
        if not region_id:
            return jsonify({"error": "region_id is required"}), 400

        # Generate the map
        map_file_path = "static/maps/intergroup_activity_map_by_region.html"
        map_object = create_intergroup_activity_map_by_region(region_id)
        map_object.save(map_file_path)

        # Return the map file path to the client
        return jsonify({
            "map_file": map_file_path
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route('/unique_group_by_country', methods=["GET"])
def intergroup_activity_map_by_country():
    try:
        # Get the country ID from the request
        country_id = request.args.get("country_id", type=int)
        if not country_id:
            return jsonify({"error": "country_id is required"}), 400

        # Generate the map
        map_file_path = "static/maps/intergroup_activity_map_by_country.html"
        map_object = create_intergroup_activity_map_by_country(country_id)
        map_object.save(map_file_path)

        # Return the map file path to the client
        return jsonify({
            "map_file": map_file_path
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500
##############################################

@statistics_bp.route('/shared_event_groups_map', methods=["GET"])
def shared_event_groups_map():
    try:
        map_file_path = "static/maps/shared_events_map.html"

        map_object = generate_shared_event_groups_map()
        map_object.save(map_file_path)

        return jsonify({
            "map_file": map_file_path
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500







@statistics_bp.route("/most_deadly/<int:limit>", methods=["GET"])
def get_most_deadly(limit):
    try:
        limit = request.args.get("limit")

        most_deadly = get_most_deadly_repo(limit)

        return jsonify({"data": most_deadly}), 200

    except ValueError as ve:
        return jsonify({"error": "Invalid input", "message": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



@statistics_bp.route("/most_deadly/map", methods=["GET"])
def get_most_deadly_map():

    try:
        # Get the 'limit' query parameter (default to 5 if not provided)
        limit = request.args.get("limit", default=1000, type=int)

        # Generate the map file
        map_file = generate_map_file(limit=limit)

        # Serve the map file
        return send_file(map_file, as_attachment=False)

    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500


@statistics_bp.route("/top_countries/map", methods=["GET"])
def get_top_countries_map():
    """
    Endpoint to generate and return a map of the top 5 countries by event count.
    """
    try:
        # Generate the map
        map_file = generate_top_countries_map()

        # Serve the map file
        return send_file(map_file, as_attachment=False)

    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500



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









