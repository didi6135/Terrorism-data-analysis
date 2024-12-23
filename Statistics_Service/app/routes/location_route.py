import json

from flask import Blueprint, jsonify

from Statistics_Service.app.db.redis_db import redis_client
from Statistics_Service.app.repository.city_repository import get_all_cities
from Statistics_Service.app.repository.country_repository import get_all_countries
from Statistics_Service.app.repository.event_repository import get_all_years_repo
from Statistics_Service.app.repository.region_repository import get_all_regions
from Statistics_Service.app.repository.target_type_repoisotory import get_all_target_types

location_bp = Blueprint('location', __name__)



def cache_or_fetch(key, fetch_function, expiration=3600):
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)

    data = fetch_function()
    redis_client.setex(key, expiration, json.dumps(data))
    return data


@location_bp.route("/regions", methods=["GET"])
def get_regions():
    try:
        regions = cache_or_fetch("regions", get_all_regions)
        return jsonify({"regions": regions}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch regions", "message": str(e)}), 500


@location_bp.route("/countries", methods=["GET"])
def get_countries():
    try:
        countries = cache_or_fetch("countries", get_all_countries)
        return jsonify({"countries": countries}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch countries", "message": str(e)}), 500


@location_bp.route("/cities", methods=["GET"])
def get_cities():
    try:
        cities = cache_or_fetch("cities", get_all_cities)
        return jsonify({"cities": cities}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch cities", "message": str(e)}), 500


@location_bp.route("/target_type", methods=["GET"])
def get_target_type():
    try:
        target_types = cache_or_fetch("target_types", get_all_target_types)
        return jsonify({"target_types": target_types}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch target types", "message": str(e)}), 500



@location_bp.route('/years', methods=["GET"])
def get_all_years():
    try:
        all_years = cache_or_fetch("all_years", get_all_years_repo)
        return jsonify(all_years), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch all years", "message": str(e)}), 500