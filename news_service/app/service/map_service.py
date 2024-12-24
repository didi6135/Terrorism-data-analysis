import os
import random

import folium

from news_service.app.repository.elastic_repository import search_all_sources, search_real_time_articles, \
    search_historic_articles, search_combined_articles


def generate_map(
    search_type="all",
    keywords=None,
    limit=100,
    start_date=None,
    end_date=None,
    output_file="generated_map.html",
):

    search_functions = {
        "all": lambda: search_all_sources(keywords, limit),
        "realtime": lambda: search_real_time_articles(keywords, limit),
        "historic": lambda: search_historic_articles(keywords, limit),
        "combined": lambda: search_combined_articles(keywords, start_date, end_date),
    }

    # Ensure the directory exists
    save_dir = "static/maps/"
    os.makedirs(save_dir, exist_ok=True)

    # Fetch the appropriate search function
    if search_type not in search_functions:
        raise ValueError("Invalid search type. Choose from 'all', 'realtime', 'historic', or 'combined'.")

    if search_type == "combined" and (not start_date or not end_date):
        raise ValueError("Start and end dates must be provided for combined search.")

    # Execute the selected search function
    data = search_functions[search_type]()
    print(data)
    if not data:
        print("No data found for the given search parameters.")
        return None
    # Full path to save the file
    full_output_path = os.path.join(save_dir, output_file)

    # Handle missing latitude and longitude by assigning random coordinates
    for event in data:
        if not event.get("latitude") or not event.get("longitude"):
            event["latitude"] = random.uniform(-90.0, 90.0)  # Random latitude
            event["longitude"] = random.uniform(-180.0, 180.0)  # Random longitude

    # Filter valid locations
    valid_events = [event for event in data if event["latitude"] and event["longitude"]]

    if not valid_events:
        print("No valid locations found to plot on the map.")
        return None

    # Create a base map (centered at the first valid event)
    first_event = valid_events[0]
    base_map = folium.Map(location=[first_event["latitude"], first_event["longitude"]], zoom_start=5)

    # Define colors for event types
    event_colors = {
        "General News": "blue",
        "Current Terror Event": "red",
        "Historical Terror Event": "green",
        "Combined Search": "purple",
    }

    # Add markers for each valid event
    for res in valid_events:
        popup_content = (
            f"<b>Event title:</b> {res['title']}<br>"
            f"<b>Event body:</b> {res.get('body', 'N/A')}<br>"
            f"<b>Location:</b> {res.get('location', 'N/A')}<br>"
            f"<b>Date:</b> {res.get('dateTime', 'N/A')}<br>"
            f"<b>Source:</b> {res.get('source', 'N/A')}<br>"
        )

        popup = folium.Popup(
            popup_content,
            max_width=300,
            min_width=200,
            max_height=400,
        )

        # Determine the color based on the event category or type
        color = event_colors.get(res.get("category", "General News"), "blue")

        folium.CircleMarker(
            location=[res["latitude"], res["longitude"]],
            radius=10,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=popup,
        ).add_to(base_map)

    # Save the map as an HTML file
    base_map.save(full_output_path)
    print(f"Map generated and saved at {full_output_path}")
    return full_output_path
