import os

import folium
from folium.plugins import HeatMap, MarkerCluster

from Statistics_Service.app.repository.attack_type_repository import get_attack_strategies_by_region, \
    get_attack_strategies_by_country
from Statistics_Service.app.repository.city_repository import calculate_average_victims_by_city
from Statistics_Service.app.repository.country_repository import get_top_5_countries_by_events, \
    get_unique_groups_by_country, calculate_average_victims_by_country
from Statistics_Service.app.repository.event_repository import get_events_with_coordinates_and_victims
from Statistics_Service.app.repository.group_repository import get_top_events_with_coordinates, \
    get_top_groups_by_region, get_groups_with_shared_targets_by_region, \
    get_groups_with_shared_targets_by_country, get_groups_with_shared_events
from Statistics_Service.app.repository.region_repository import get_unique_groups_by_region, \
    calculate_average_victims_by_region


###################################################
def generate_map_for_victims_analysis(type_of, id_value, limit, output_file="victims_analysis_map.html"):
    # Map type to corresponding calculation function
    calculation_functions = {
        "region": calculate_average_victims_by_region,
        "country": calculate_average_victims_by_country,
        "city": calculate_average_victims_by_city
    }

    # Validate type and get the corresponding function
    if type_of not in calculation_functions:
        raise ValueError(f"Invalid type '{type_of}'. Must be 'region', 'country', or 'city'.")

    # Call the corresponding calculation function
    data = calculation_functions[type_of](id_value, limit)
    if not data:
        return None

    # Define save directory and ensure it exists
    save_dir = os.path.join("static", "maps")
    os.makedirs(save_dir, exist_ok=True)

    # Create the map
    base_map = folium.Map(location=[data[0]["latitude"], data[0]["longitude"]], zoom_start=5)
    for event in data:
        folium.CircleMarker(
            location=[event["latitude"], event["longitude"]],
            radius=max(3, event["score"] / 50),
            color=("green" if event["score"] == 0 else "orange" if event["score"] <= 30 else "red"),
            fill=True, fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>Event:</b> {event['event_description']}<br>"
                f"<b>Location Name:</b> {event.get('region_name') or event.get('country_name') or event.get('city_name', 'N/A')}<br>"
                f"<b>Average Injured:</b> {event['average_injured']}<br>"
                f"<b>Average Killed:</b> {event['average_killed']}<br>"
                f"<b>Score:</b> {event['score']}",
                max_width=300
            ),
        ).add_to(base_map)

    # Save the map with a dynamic filename
    path = os.path.join(save_dir, f'{type_of}_{id_value}_limit_{limit}_{output_file}')
    base_map.save(path)
    return path


def generate_top_groups_map(region_id=None, output_file="top_groups_map.html"):
    # Fetch top groups and use the predefined coordinates
    top_groups = get_top_groups_by_region(region_id)

    # Use predefined coordinates
    region_coordinates = {
        "Central America & Caribbean": {"latitude": 15.0, "longitude": -90.0},
        "North America": {"latitude": 54.5260, "longitude": -105.2551},
        "Southeast Asia": {"latitude": 13.4125, "longitude": 103.8667},
        "Western Europe": {"latitude": 48.8566, "longitude": 2.3522},
        "East Asia": {"latitude": 35.8617, "longitude": 104.1954},
        "South America": {"latitude": -14.2350, "longitude": -51.9253},
        "Eastern Europe": {"latitude": 55.3781, "longitude": 37.6173},
        "Sub-Saharan Africa": {"latitude": -1.9403, "longitude": 29.8739},
        "Middle East & North Africa": {"latitude": 24.2155, "longitude": 45.0792},
        "Australasia & Oceania": {"latitude": -25.2744, "longitude": 133.7751},
        "South Asia": {"latitude": 20.5937, "longitude": 78.9629},
        "Central Asia": {"latitude": 48.0196, "longitude": 66.9237},
        "Unknown": {"latitude": 0.0, "longitude": 0.0}
    }

    # Initialize a world map
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    # Add markers for each region
    for region, groups in top_groups.items():
        if coord := region_coordinates.get(region):
            popup_content = f"<strong>Top Groups in {region}</strong><br><ol>"
            popup_content += "".join(f"<li>{g['group_name']} ({g['event_count']} events)</li>" for g in groups)
            popup_content += "</ol>"

            # Add the marker to the map
            folium.Marker(
                location=[coord["latitude"], coord["longitude"]],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"{region} (Click for details)"
            ).add_to(world_map)

    # Define the save path
    save_dir = os.path.join("static", "maps")
    path = os.path.join(save_dir, f'{region_id}_{output_file}')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save the map
    world_map.save(path)
    return path


def create_shared_target_map(entity_id, entity_type="region", output_file="top_groups_shared_target_map.html"):

    # Fetch shared targets based on entity type
    if entity_type == "region":
        shared_targets = get_groups_with_shared_targets_by_region(entity_id)
    elif entity_type == "country":
        shared_targets = get_groups_with_shared_targets_by_country(entity_id)
    else:
        raise ValueError("Invalid entity_type. Must be 'region' or 'country'.")

    # Create base map and cluster
    shared_map = folium.Map(location=[20, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(shared_map)

    # Add markers
    for target in shared_targets:
        popup_content = (
            f"<strong>{target['target_name']}</strong><br>"
            f"<b>Event Count:</b> {target['event_count']}<br>"
            f"<b>Groups:</b><ul>{''.join(f'<li>{group}</li>' for group in target['groups'])}</ul>"
        )
        folium.Marker(
            location=[target["latitude"], target["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{target['target_name']} ({target['event_count']} events)"
        ).add_to(marker_cluster)

    # Handle save directory
    save_dir = os.path.join("static", "maps")
    path = os.path.join(save_dir, f"{entity_type}_{entity_id}_{output_file}")
    os.makedirs(save_dir, exist_ok=True)

    # Save map
    shared_map.save(path)
    return path


####################################################



def generate_map_file(limit=5, output_file="top_events_map.html"):

    events = get_top_events_with_coordinates(limit=limit)
    # Handle case when no events are found
    if not events:
        print("No events found to display on the map.")
        return None

    # Create a base map (centered at the first event)
    first_event = events[0]
    base_map = folium.Map(location=[first_event["latitude"], first_event["longitude"]], zoom_start=5)

    # Add markers for each event
    for event in events:

        if event["latitude"] is not None and event["longitude"] is not None:
            folium.CircleMarker(
                location=[event["latitude"], event["longitude"]],
                radius= 10 if event['score'] == 0 else event["score"] / 100,  # Scale radius based on casualties
                color=(
                    "green" if event["score"] == 0 else
                    "orange" if 0 < event["score"] <= 30 else
                    "red"
                ),
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(
                    f""
                    f"<b>{event['event_description']}</b>"
                    f"</b><br> <b>Total deadly:</b> {event['total_killed']}"
                    f"</b><br> <b>Total injured:</b> {event['total_injured']}"
                    f"<br> <b>Score:</b> {event['score']}"

                    , max_width=300
                ),
            ).add_to(base_map)

    # Save the map as an HTML file
    base_map.save(output_file)
    print(f"Map generated and saved as '{output_file}'")
    return output_file


def generate_top_countries_map(output_file="top_countries_map.html"):

    countries = get_top_5_countries_by_events()
    # Create a base map
    base_map = folium.Map(location=[20, 0], zoom_start=2)

    # Add markers for each country
    for country in countries:
        name = country["country_name"]
        count = country["event_count"]

        if name in countries:
            folium.CircleMarker(
                location=countries[name],
                radius=count / 10,  # Scale radius based on event count
                color="red" if count > 100 else "orange",  # Conditional coloring
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>{name}</b><br>Event Count: {count}", max_width=300
                ),
            ).add_to(base_map)

    # Save the map as an HTML file
    base_map.save(output_file)
    print(f"Map generated and saved as '{output_file}'")
    return output_file


def generate_heatmap(output_file="heatmap.html"):
    """
    Generates a heatmap based on event locations and total victims.
    """
    # Get event data
    events = get_events_with_coordinates_and_victims()

    # Filter valid coordinates
    heat_data = [
        [event["latitude"], event["longitude"], event["total_victims"]]
        for event in events
        if event["latitude"] != 0.0 and event["longitude"] != 0.0
    ]

    if not heat_data:
        raise ValueError("No valid data for heatmap generation.")

    # Create a base map
    base_map = folium.Map(location=[20, 0], zoom_start=2)

    # Add heatmap
    HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(base_map)

    # Save the map as an HTML file
    base_map.save(output_file)
    print(f"Heatmap generated and saved as '{output_file}'")
    return output_file







#####################################################







def generate_attack_strategy_map(region_id=None):
    """
    Generates a map with markers for attack strategies by region or globally.
    """
    data = get_attack_strategies_by_region(region_id)

    # Create base map
    base_map = folium.Map(location=[20, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(base_map)

    for item in data:
        # Extract details
        latitude = item["latitude"]
        longitude = item["longitude"]
        region_name = item["region_name"]
        attack_type = item["attack_type"]
        unique_group_count = item["unique_group_count"]
        group_names = item["group_names"]

        # Prepare popup content
        popup_content = f"""
        <strong>{region_name}</strong><br>
        <strong>Attack Type:</strong> {attack_type}<br>
        <strong>Unique Groups:</strong> {unique_group_count}<br>
        <strong>Groups:</strong> {", ".join(group_names)}
        """

        # Add marker to map
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{attack_type} ({unique_group_count} groups)"
        ).add_to(marker_cluster)

    return base_map


def generate_attack_strategy_map_by_country(country_id=None):
    """
    Generates a map with markers for attack strategies by country or globally.
    """
    data = get_attack_strategies_by_country(country_id)

    # Create base map
    base_map = folium.Map(location=[20, 0], zoom_start=2)
    marker_cluster = folium.plugins.MarkerCluster().add_to(base_map)

    for item in data:
        # Extract details
        latitude = item["latitude"]
        longitude = item["longitude"]
        country_name = item["country_name"]
        attack_type = item["attack_type"]
        unique_group_count = item["unique_group_count"]
        group_names = item["group_names"]

        # Prepare popup content
        popup_content = f"""
        <strong>{country_name}</strong><br>
        <strong>Attack Type:</strong> {attack_type}<br>
        <strong>Unique Groups:</strong> {unique_group_count}<br>
        <strong>Groups:</strong> {", ".join(group_names)}
        """

        # Add marker to map
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{attack_type} ({unique_group_count} groups)"
        ).add_to(marker_cluster)

    return base_map



def create_intergroup_activity_map_by_country(country_id):
    """
    Create a map showing intergroup activity for a specific country.
    """
    # Retrieve data for the specific country
    data = get_unique_groups_by_country(country_id)

    # Create a base map
    base_map = folium.Map(location=[9.145, 40.489673], zoom_start=5)  # Adjust coordinates to focus on Africa

    # Add markers to the map
    for item in data:
        latitude = item["latitude"]
        longitude = item["longitude"]
        country_name = item["country_name"]
        unique_group_count = item["unique_group_count"]
        group_names = item["group_names"]

        # Create popup content
        popup_content = f"""
        <strong>{country_name}</strong><br>
        <strong>Unique Group Count:</strong> {unique_group_count}<br>
        <strong>Groups:</strong>
        <ul>
        {''.join(f"<li>{group}</li>" for group in group_names)}
        </ul>
        """

        # Add marker to the map
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{country_name} ({unique_group_count} groups)"
        ).add_to(base_map)

    return base_map


def create_intergroup_activity_map_by_region(region_id):
    """
    Create a map showing intergroup activity for a specific region.
    """
    # Retrieve data for the specific region
    data = get_unique_groups_by_region(region_id)

    # Create a base map
    base_map = folium.Map(location=[20, 0], zoom_start=3)  # Adjust coordinates to focus on regions globally

    # Add markers to the map
    for item in data:
        latitude = item["latitude"]
        longitude = item["longitude"]
        region_name = item["region_name"]
        unique_group_count = item["unique_group_count"]
        group_names = item["group_names"]

        # Create popup content
        popup_content = f"""
        <strong>{region_name}</strong><br>
        <strong>Unique Group Count:</strong> {unique_group_count}<br>
        <strong>Groups:</strong>
        <ul>
        {''.join(f"<li>{group}</li>" for group in group_names)}
        </ul>
        """

        # Add marker to the map
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{region_name} ({unique_group_count} groups)"
        ).add_to(base_map)

    return base_map



def generate_shared_event_groups_map():

    shared_events = get_groups_with_shared_events()

    shared_events_map = folium.Map(location=[20, 0], zoom_start=2)

    marker_cluster = folium.plugins.MarkerCluster().add_to(shared_events_map)

    for event in shared_events:
        event_id = event["event_id"]
        description = event["event_description"]
        latitude = event["latitude"]
        longitude = event["longitude"]
        location = event["location"]
        groups = event["groups"]

        popup_content = f"""
        <strong>Event ID:</strong> {event_id}<br>
        <strong>Description:</strong> {description}<br>
        <strong>Location:</strong> {location}<br>
        <strong>Groups:</strong>
        <ul>
        {''.join([f"<li>{group}</li>" for group in groups])}
        </ul>
        """

        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"Event ID: {event_id}"
        ).add_to(marker_cluster)

    return shared_events_map
