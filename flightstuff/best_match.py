from haversine import haversine
import math

def best_match(user_lat, user_lon, possibleFlights, user_angle):
    min_diff = 1000
    best_match = 0
    for curFlight in possibleFlights['data']:
        flight_lat = curFlight['lat']
        flight_lon = curFlight['lon']
        
        flight_alt = curFlight['alt']
        distance = haversine((user_lat, user_lon), (flight_lat, flight_lon), unit='km')/1000

        expected_user_angle = math.atan(flight_alt/distance)

        min_diff = min(min_diff,abs(expected_user_angle-user_angle))

        if (min_diff == abs(expected_user_angle-user_angle)):
            best_match = curFlight
    
    return best_match







