import folium
from folium.plugins import HeatMap

from Statistics_Service.app.repository.country_repository import get_top_5_countries_by_events
from Statistics_Service.app.repository.event_repository import get_events_with_coordinates_and_victims
from Statistics_Service.app.repository.group_repository import get_top_events_with_coordinates, \
    get_top_groups_by_region, get_region_coordinates


def generate_map_file(limit=5, output_file="top_events_map.html"):
    """
    Generates a map with the top events based on casualties and saves it as an HTML file.
    """
    # Get top events with coordinates
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
    """
    Generates a map with the top 5 countries by event count.
    """
    # Get top countries data
    countries = get_top_5_countries_by_events()

    # Create a base map
    base_map = folium.Map(location=[20, 0], zoom_start=2)

    # Coordinates for demonstration purposes (replace with actual country center coordinates)


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




def generate_top_groups_map():
    """
    Generate a map showing the top 5 most active groups by region.
    """
    # Fetch data
    top_groups_by_region = get_top_groups_by_region()
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

    # Save map as an HTML file
    world_map.save("top_groups_by_region_map.html")
    return world_map




import os

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

