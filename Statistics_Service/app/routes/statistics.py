from flask import Blueprint, jsonify, request, send_file

from Statistics_Service.app.repository.attack_type_repository import analyze_attack_target_correlation, \
    get_most_deadly_attack_types
from Statistics_Service.app.repository.city_repository import get_cities_by_country, calculate_average_victims_by_city
from Statistics_Service.app.repository.country_repository import get_countries_by_region, \
    calculate_average_victims_by_country
from Statistics_Service.app.repository.event_repository import get_event_trends_cleaned, get_monthly_trends, \
    get_yearly_trends
from Statistics_Service.app.repository.group_repository import get_most_deadly_repo, get_top_5_groups_by_casualties
from Statistics_Service.app.repository.region_repository import get_all_regions, calculate_average_victims_by_region
from Statistics_Service.app.services.plot_service import plot_event_trends_cleaned, plot_monthly_trends, \
    plot_yearly_trends
from Statistics_Service.app.services.visualization_service import generate_map_file, generate_top_countries_map, \
    generate_heatmap, generate_top_groups_map

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



@statistics_bp.route("/countries/<int:region_id>", methods=["GET"])
def get_countries(region_id):
    try:
        countries = get_countries_by_region(region_id)
        return jsonify({"countries": countries}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch countries", "message": str(e)}), 500



@statistics_bp.route("/cities/<int:country_id>", methods=["GET"])
def get_cities(country_id):
    try:
        cities = get_cities_by_country(country_id)
        return jsonify({"cities": cities}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch cities", "message": str(e)}), 500


@statistics_bp.route("/average_victims", methods=["GET"])
def get_average_victims():
    try:
        level = request.args.get("level")
        level_id = request.args.get("id", type=int)

        if level == "region":
            data = calculate_average_victims_by_region(level_id)
        elif level == "country":
            data = calculate_average_victims_by_country(level_id)
        elif level == "city":
            data = calculate_average_victims_by_city(level_id)
        else:
            raise ValueError("Invalid level. Use 'region', 'country', or 'city'.")

        return jsonify({"data": data}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to calculate average victims", "message": str(e)}), 500

##############################################

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

@statistics_bp.route("/top_groups_map", methods=["GET"])
def get_top_groups_map():

    try:
        map_file_path = "top_groups_map.html"
        map_object = generate_top_groups_map()
        map_object.save(map_file_path)

        return send_file(
            map_file_path,
            mimetype="text/html",
            as_attachment=False
        )
    except Exception as e:
        return jsonify({"error": "Failed to generate map", "message": str(e)}), 500

@statistics_bp.route("/attack_target_correlation", methods=["GET"])
def get_attack_target_correlation():

    try:

        correlation_data = analyze_attack_target_correlation()

        return jsonify({"correlation": correlation_data}), 200
    except Exception as e:
        return jsonify({"error": "Failed to calculate correlation", "message": str(e)}), 500

@statistics_bp.route("/event_trends", methods=["GET"])
def get_event_trends_endpoint():

    try:
        year = request.args.get("year", type=int, default=None)

        if year:
            monthly_df = get_monthly_trends(year)
            plot_monthly_trends(monthly_df, year)
            return jsonify({
                "monthly_trends": monthly_df.to_dict(orient="records")
            }), 200
        else:
            yearly_df = get_yearly_trends()
            plot_yearly_trends(yearly_df)
            return jsonify({
                "yearly_trends": yearly_df.to_dict(orient="records")
            }), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate trends", "message": str(e)}), 500


@statistics_bp.route("/top_groups_by_casualties", methods=["GET"])
def top_groups_by_casualties():
    """
    Returns the top 5 groups with the highest casualties.
    """
    try:
        top_groups = get_top_5_groups_by_casualties()
        return jsonify({"data": top_groups}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch top groups by casualties", "message": str(e)}), 500