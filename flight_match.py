from arduinostuff.arduino_data import *

# curflightJSON = getFlight()
# user_height = 5.66 #constant 5' 8"
# user_direc = 0
while True:
    user_lat = getLat()
    user_lon = getLon()
    user_pitch = getPitch()
    user_roll = getRoll()
    print(str(user_lat) + " " + str(user_lon) + " " + str(user_pitch) + " " + str(user_roll))

# flight_alt = curflightJSON['data'][0]['live']['altitude']
# flight_direc = curflightJSON['data'][0]['live']['direction']
# flight_coords = (curflightJSON['data'][0]['live']['latitude'], curflightJSON['data'][0]['live']['longitude'])


# dist_y = flight_alt-user_height
    
# expected_angle = math.atan(dist_y/dist_x)


# print(dist_x)
# print(dist_y)
# print(expected_angle)
# print(flight_coords)

