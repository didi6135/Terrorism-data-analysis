import os

import folium
from folium.plugins import HeatMap, MarkerCluster

from Statistics_Service.app.repository.attack_type_repository import get_attack_strategies_by_region, \
    get_attack_strategies_by_country
from Statistics_Service.app.repository.country_repository import get_top_5_countries_by_events, \
    get_unique_groups_by_country
from Statistics_Service.app.repository.event_repository import get_events_with_coordinates_and_victims
from Statistics_Service.app.repository.group_repository import get_top_events_with_coordinates, \
    get_top_groups_by_region, get_region_coordinates, get_groups_with_shared_targets_by_region, \
    get_groups_with_shared_targets_by_country
from Statistics_Service.app.repository.region_repository import get_unique_groups_by_region


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


def generate_top_groups_map(region_id=None):
    """
    Generate a map showing the top 5 most active groups by region or for a specific region.
    """
    # Fetch data
    top_groups_by_region = get_top_groups_by_region(region_id)
    region_coordinates = get_region_coordinates()

    # Create base map
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    for region, groups in top_groups_by_region.items():
        # Get region coordinates
        coordinates = region_coordinates.get(region, None)
        if not coordinates:
            continue

        # Prepare popup content
        popup_content = f"<strong>Top Groups in {region}</strong><br>"
        popup_content += "<ol>"
        for group in groups:
            popup_content += f"<li>{group['group_name']} ({group['event_count']} events)</li>"
        popup_content += "</ol>"

        # Add marker to map
        folium.Marker(
            location=[coordinates["latitude"], coordinates["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{region} (Click for details)"
        ).add_to(world_map)

    return world_map



def generate_map_for_victims_analysis(data, output_file="victims_analysis_map.html"):
    if not data:
        print("No data provided to generate the map.")
        return None

    # Ensure the directory exists
    save_dir = "static/maps/"
    os.makedirs(save_dir, exist_ok=True)

    # Full path to save the file
    full_output_path = os.path.join(save_dir, output_file)

    # Create a base map (centered at the first event)
    first_event = data[0]
    base_map = folium.Map(location=[first_event["latitude"], first_event["longitude"]], zoom_start=5)

    # Add markers for each event
    for event in data:
        if event["latitude"] is not None and event["longitude"] is not None:
            folium.CircleMarker(
                location=[event["latitude"], event["longitude"]],
                radius=10 if event['score'] == 0 else event["score"] / 100,  # Scale radius based on casualties
                color=(
                    "green" if event["score"] == 0 else
                    "orange" if 0 < event["score"] <= 30 else
                    "red"
                ),
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>Event:</b> {event['event_description']}<br>"
                    f"<b>Region:</b> {event.get('region_name', 'N/A')}<br>"
                    f"<b>Country:</b> {event.get('country_name', 'N/A')}<br>"
                    f"<b>City:</b> {event.get('city_name', 'N/A')}<br>"
                    f"<b>Average Injured:</b> {event['average_injured']}<br>"
                    f"<b>Average Killed:</b> {event['average_killed']}<br>"
                    f"<b>Score:</b> {event['score']}",
                    max_width=300
                ),
            ).add_to(base_map)

    # Save the map as an HTML file in the specified directory
    base_map.save(full_output_path)
    print(f"Map generated and saved as '{full_output_path}'")
    return full_output_path

#####################################################
def create_shared_target_map_by_region(region_id):


    # Get data from the database
    shared_targets = get_groups_with_shared_targets_by_region(region_id)

    # Create the base map
    region_map = folium.Map(location=[20, 0], zoom_start=2)

    # Add MarkerCluster for better visualization
    marker_cluster = MarkerCluster().add_to(region_map)

    for target in shared_targets:
        # Get target data
        target_name = target["target_name"]
        latitude = target["latitude"]
        longitude = target["longitude"]
        event_count = target["event_count"]
        groups = target["groups"]

        # Prepare popup content
        popup_content = f"<strong>{target_name}</strong><br>"
        popup_content += f"<b>Event Count:</b> {event_count}<br>"
        popup_content += "<b>Groups:</b><ul>"
        for group in groups:
            popup_content += f"<li>{group}</li>"
        popup_content += "</ul>"

        # Add a marker for the target
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{target_name} ({event_count} events)"
        ).add_to(marker_cluster)

    return region_map

def create_shared_target_map_by_country(country_id):

    # Get data from the database
    shared_targets = get_groups_with_shared_targets_by_country(country_id)

    # Create the base map
    country_map = folium.Map(location=[20, 0], zoom_start=2)

    # Add MarkerCluster for better visualization
    marker_cluster = MarkerCluster().add_to(country_map)

    for target in shared_targets:
        # Get target data
        target_name = target["target_name"]
        latitude = target["latitude"]
        longitude = target["longitude"]
        event_count = target["event_count"]
        groups = target["groups"]

        # Prepare popup content
        popup_content = f"<strong>{target_name}</strong><br>"
        popup_content += f"<b>Event Count:</b> {event_count}<br>"
        popup_content += "<b>Groups:</b><ul>"
        for group in groups:
            popup_content += f"<li>{group}</li>"
        popup_content += "</ul>"

        # Add a marker for the target
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{target_name} ({event_count} events)"
        ).add_to(marker_cluster)

    return country_map




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
