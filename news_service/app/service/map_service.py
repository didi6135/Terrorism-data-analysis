import json
import os

import folium

from news_service.app.repository.elastic_repository import search_all_sources


import folium
import os

def generate_map_for_keywords(keyword, limit, output_file="keywords_map.html"):
    if not keyword:
        print('Keyword is required.')
        return None

    data = search_all_sources(keyword, limit)
    print(f'len of data: {len(data)}')
    print(json.dumps(data, indent=4))
    if not data:
        print("No data found for the given keyword.")
        return None

    # Ensure the directory exists
    save_dir = "static/maps/"
    os.makedirs(save_dir, exist_ok=True)

    # Full path to save the file
    full_output_path = os.path.join(save_dir, output_file)

    # Filter valid locations
    valid_events = [event for event in data if event["latitude"] and event["longitude"]]

    if not valid_events:
        print("No valid locations found to plot on the map.")
        return None

    print(f"Number of valid events: {len(valid_events)}")  # Debug log

    # Create a base map (centered at the first valid event)
    first_event = valid_events[0]
    base_map = folium.Map(location=[first_event["latitude"], first_event["longitude"]], zoom_start=5)

    # Define colors for event types
    event_colors = {
        "General News": "blue",
        "Current Terror Event": "red",  # Current events
        "Historical Terror Event": "green"  # Historical events

    }

    # Add markers for each valid event
    for res in valid_events:
        popup_content = (
            f"<b>Event title:</b> {res['title']}<br>"
            f"<b>Event body:</b> {res.get('body', 'N/A')}<br>"
            f"<b>Location:</b> {res.get('location', 'N/A')}<br>"
            f"<b>Date:</b> {res.get('dateTime', 'N/A')}<br>"
            f"<b>Source:</b> {res['source']}<br>"
        )

        popup = folium.Popup(
            popup_content,
            max_width=300,
            min_width=200,
            max_height=400,
        )

        # Determine the color based on the event source
        color = event_colors.get(res["source"], "blue")  # Default to blue if source is unknown

        folium.CircleMarker(
            location=[res["latitude"], res["longitude"]],
            radius=10,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=popup,
        ).add_to(base_map)

    # Save the map as an HTML file in the specified directory
    base_map.save(full_output_path)
    print(f"Map generated and saved as '{full_output_path}'")
    return full_output_path

