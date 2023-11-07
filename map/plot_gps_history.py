import folium
from folium.plugins import TimestampedGeoJson

# Your list of GPS positions with timestamps
gps_positions_with_time = [
    {'time': '2023-01-01T00:00:00', 'coordinates': (6.960279, 50.937531, )},  # Cologne Cathedral
    {'time': '2023-01-01T01:00:00', 'coordinates': (2.294481, 48.858370)},  # Eiffel Tower
    # Add more dictionaries with 'time' and 'coordinates' keys here
]

# Create a map object, starting at the first position
mymap = folium.Map(location=gps_positions_with_time[0]['coordinates'], zoom_start=5)

# Create a features list for the TimestampedGeoJson
features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': point['coordinates'],
        },
        'properties': {
            'time': point['time'],
            'popup': point['time'],  # Use the timestamp as a popup content
            'id': 'house',
            'icon': 'circle',
            'iconstyle': {
                'fillColor': '#ff0000',
                'fillOpacity': 0.8,
                'stroke': 'true',
                'radius': 7
            },
        },
    } for point in gps_positions_with_time
]

# Add the features to the map with a time slider
TimestampedGeoJson({
    'type': 'FeatureCollection',
    'features': features,
}, period='PT1H',  # Set the period for the timeslider here, 'PT1H' is 1 hour
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY/MM/DD HH:mm:ss',
    time_slider_drag_update=True).add_to(mymap)

# Save it to an html file
mymap.save('my_timed_map.html')

# This will open the map in your web browser
import webbrowser
webbrowser.open('my_timed_map.html')
