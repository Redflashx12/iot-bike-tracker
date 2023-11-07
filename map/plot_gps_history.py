import folium
from folium.plugins import TimestampedGeoJson
import datetime

# Function to create a feature for each segment of the journey
def create_geojson_features(data):
    features = []
    for i in range(len(data) - 1):
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [data[i]['coordinates'], data[i+1]['coordinates']],
            },
            'properties': {
                'times': [data[i]['time'], data[i+1]['time']],
                'style': {
                    'color': 'red',
                    'weight': 5
                }
            }
        }
        features.append(feature)
    return features

if __name__ == '__main__':
    # Sample data: list of coordinates with timestamps
    data = [
        {'coordinates': [6.960279, 50.937531], 'time': '2023-01-01T00:00:00Z'}, # Cologne Cathedral
        {'coordinates': [2.294481, 48.858370], 'time': '2023-01-01T01:00:00Z'}, # Eiffel Tower
        {'coordinates': [3.294481, 48.858370], 'time': '2023-01-01T02:00:00Z'},
        {'coordinates': [4.294481, 48.858370], 'time': '2023-01-01T03:00:00Z'},
        {'coordinates': [5.294481, 47.858370], 'time': '2023-01-01T04:00:00Z'},
        # Add more entries here
    ]
    # Create map object
    m = folium.Map(location=data[0]['coordinates'], zoom_start=3)

    # Create features
    features = create_geojson_features(data)

    # Create a TimestampedGeoJson object and add it to the map
    TimestampedGeoJson({
        'type': 'FeatureCollection',
        'features': features,
    }, period='PT30M',
        transition_time=1000,
        auto_play=True,
        loop=True,
        max_speed=1,
        loop_button=True,
        date_options='YYYY/MM/DD HH:mm:ss',
        time_slider_drag_update=True,
        add_last_point=True).add_to(m)

    # Save to an HTML file
    m.save('animated_path.html')
