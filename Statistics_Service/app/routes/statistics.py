from flask import Blueprint, jsonify, request, send_file

from Statistics_Service.app.repository.attack_type_repository import analyze_attack_target_correlation
from Statistics_Service.app.repository.event_repository import get_event_trends_cleaned, get_monthly_trends, \
    get_yearly_trends
from Statistics_Service.app.repository.group_repository import get_most_deadly_repo, get_top_5_groups_by_casualties
from Statistics_Service.app.services.plot_service import plot_event_trends_cleaned, plot_monthly_trends, \
    plot_yearly_trends
from Statistics_Service.app.services.visualization_service import generate_map_file, generate_top_countries_map, \
    generate_heatmap, generate_top_groups_map

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.route("/most_deadly/<int:limit>", methods=["GET"])
def get_top_5():
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