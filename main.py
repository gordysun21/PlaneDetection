import numpy as np
from userinfostuff import *
from flightstuff import *
from pprint import pprint

#Figure out user inforomation
userCoords = get_user_coordinates()[0]

#Break that down
user_orientation = get_user_orientation()
user_lat = userCoords[0]
user_lon = userCoords[1]
user_angle = get_user_angle()

#Create the box of view that planes could be in
possibleFlightsBounds = get_user_seen_coordinates(user_lat, user_lon, user_orientation)

#Find the planes that are located in that box of view
possibleFlights = getFlight(possibleFlightsBounds)

#Address the weird box of angles and find which planes I'm actually looking at
possibleFlights = fovFlights(user_lat, user_lon, user_orientation, possibleFlights)

#Get the possible planes
bestFlight = best_match(user_lat, user_lon, possibleFlights, user_angle)

#Print out the best matching plane
pprint(bestFlight)

