import folium
from folium.plugins import TimestampedGeoJson
import datetime

# Function to create a feature for each segment of the journey
def create_line_geojson_features(data):
    return [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [data[index]['coordinates'], data[index+1]['coordinates']],
            },
            'properties': {
                'times': [data[index]['time'], data[index+1]['time']],
                'popup': str(point['time']),  # Use the timestamp as a popup content
                'style': {
                    'color': 'red',
                    'weight': 3
                }
            }
        }
for index, point in enumerate(data[:-1]) ]

def create_point_geojson_features(data):
    return [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': point['coordinates'],
            },
            'properties': {
                'time': point['time'],
                'popup': f"""
                Date: {str(point['time'])}\n
                Battery: {str(point.get('batt', 'N/A'))}
                """,  # Use the timestamp as a popup content
                'id': 'house',
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': '#ff0000',
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 7
                },
            },
        } for point in data
    ]



if __name__ == '__main__':
    # Sample data: list of coordinates with timestamps
    data = [
        {'coordinates': [6.960279, 50.937531], 'time': '2023-01-01T00:00:00Z', 'batt': 55}, # Cologne Cathedral
        {'coordinates': [2.294481, 48.858370], 'time': '2023-01-01T01:00:00Z', 'batt': 45}, # Eiffel Tower
        {'coordinates': [3.294481, 48.858370], 'time': '2023-01-01T02:00:00Z', 'batt': 35},
        {'coordinates': [4.294481, 48.858370], 'time': '2023-01-01T03:00:00Z', 'batt': 25},
        {'coordinates': [5.294481, 47.858370], 'time': '2023-01-01T04:00:00Z', 'batt': 15},
        # Add more entries here
    ]
    # Create map object
    m = folium.Map(location=data[0]['coordinates'], zoom_start=3)

    # Create features
    features = create_point_geojson_features(data)

    # Create a TimestampedGeoJson object and add it to the map
    TimestampedGeoJson({
        'type': 'FeatureCollection',
        'features': features,
    }, period='PT1H',
        transition_time=1000,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY/MM/DD HH:mm:ss',
        time_slider_drag_update=True,
        add_last_point=True).add_to(m)

    # Save to an HTML file
    name = 'popup_path.html'
    m.save(name)
    print(f'Map saved to {name}')
