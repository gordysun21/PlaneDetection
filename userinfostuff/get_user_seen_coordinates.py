import folium
import math
from geopy.distance import distance
from geopy import Point
from shapely.geometry import Point as ShPoint
from shapely.geometry import Polygon as ShPolygon

distWidth = 3
distLen = 15

def get_user_seen_coordinates(user_lat, user_lon, orientation):
    user_point = Point(user_lat, user_lon)
    point_1 = distance(miles=distWidth).destination(user_point, orientation - 90)
    point_2 = distance(miles=distWidth).destination(user_point, orientation + 90)
    farDirecAngle = 90-math.degrees(math.atan(distLen/distWidth))
    point_3 = distance(miles=distLen).destination(user_point, orientation + farDirecAngle)
    point_4 = distance(miles=distLen).destination(user_point, orientation - farDirecAngle)

    square_coords = [
        (point_1.latitude, point_1.longitude),
        (point_4.latitude, point_4.longitude),
        (point_3.latitude, point_3.longitude),
        (point_2.latitude, point_2.longitude)
    ]

    maxLat = -200
    minLat = 200
    maxLon = -200
    minLon = 200

    for i in range(0,4):
        maxLat = max(maxLat, square_coords[i][0])
        minLat = min(minLat, square_coords[i][0])
        maxLon = max(maxLon, square_coords[i][1])
        minLon = min(minLon, square_coords[i][1])
    
    boundLimits = [round(maxLat,3), round(minLat,3), round(maxLon,3), round(minLon,3)]
    return boundLimits

def build_html_file(user_lat, user_lon, orientation):
    user_point = Point(user_lat, user_lon)
    point_1 = distance(miles=distWidth).destination(user_point, orientation - 90)
    point_2 = distance(miles=distWidth).destination(user_point, orientation + 90)
    farDirecAngle = 90-math.degrees(math.atan(distLen/distWidth))
    point_3 = distance(miles=distLen).destination(user_point, orientation + farDirecAngle)
    point_4 = distance(miles=distLen).destination(user_point, orientation - farDirecAngle)

    square_coords = [
        (point_1.latitude, point_1.longitude),
        (point_4.latitude, point_4.longitude),
        (point_3.latitude, point_3.longitude),
        (point_2.latitude, point_2.longitude)
    ]
    return square_coords

def fovFlights(user_lat, user_lon, orientation, possibleFlights):
    mymap = folium.Map(location=[user_lat, user_lon], zoom_start=14)

    # Build the box coordinates
    box_coordinates = build_html_file(user_lat, user_lon, orientation)

    # Create a polygon using the coordinates
    pgon = ShPolygon(box_coordinates)

    # Add the polygon to the map
    folium.Polygon(
        locations=box_coordinates,  # The coordinates of the box
        color="blue",               # Border color
        fill=True,                  # Fill the polygon
        fill_color="blue",          # Fill color
        fill_opacity=0.3            # Opacity of the fill
    ).add_to(mymap)

    # Add a marker for the user's location
    folium.Marker(
        location=[user_lat, user_lon],
        popup="User Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mymap)

    # Iterate through possible flights
    flightsInFOV = []
    for curFlight in possibleFlights['data']:
        if (pgon.contains(ShPoint(curFlight['lat'],curFlight['lon']))):
            folium.Marker(
                location=[curFlight['lat'], curFlight['lon']],
                popup=curFlight['callsign'],
                icon=folium.Icon(color="green", icon="check-circle")
            ).add_to(mymap)
            flightsInFOV.append(curFlight)
        else:
            folium.Marker(
                location=[curFlight['lat'], curFlight['lon']],
                popup=curFlight['callsign'],
                icon=folium.Icon(color="gray", icon="check-circle")
            ).add_to(mymap)

    # Save the map to an HTML file
    mymap.save("box_map.html")
    return flightsInFOV

    