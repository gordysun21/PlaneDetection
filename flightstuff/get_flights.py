#Live Key ****************************************************************
#Sandbox Key ****************************************************************
import requests
from userinfostuff.get_user_seen_coordinates import *

def getFlight(userBounds):
    url = 'https://fr24api.flightradar24.com/api/live/flight-positions/full?bounds='
    url += str(userBounds[0]) + ','
    url += str(userBounds[1]) + ','
    url += str(userBounds[3]) + ','
    url += str(userBounds[2]) + '&limit=10'
    
    headers = {
        'Accept': 'application/json',
        'Accept-Version': 'v1',
        'Authorization': 'Bearer 9d885098-7ef8-4b64-bb8c-a092072ac2ff|QPA8TSMXsdqKq3UMd83U3l8d44B3vFcywd6yNwpq1832a59f'
    }
    
    # Perform the GET request with headers
    response = requests.get(url, headers=headers)
    
    # Check for successful response
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")