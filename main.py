import json
import requests
import math
from typing import List

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

def degreesToRadians(deg):
    return math.pi * deg / 180

def dist(lat1, lon1, lat2, lon2):
    earthRadius = 6371000
    dLat = degreesToRadians(lat2 - lat1)
    dLon = degreesToRadians(lon2 - lon1)
    lat1 = degreesToRadians(lat1)
    lat2 = degreesToRadians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return earthRadius * c

@app.get('/')
async def front_page():
    return RedirectResponse(url='/docs')

@app.get('/get-closest-station')
async def get_closest_station(lat: float, lon: float, measure: str):
    """[summary]

    Args:
        lat (float): [description]
        lon (float): [description]
        measure (str): [description]

    Returns:
        [type]: [description]
    """    
    # request format: [[lat, lon],[measure 1, measure 2, ...]]
    # requestList = [{'location': [64.141430, -21.914849], 'measures': ['H2S']}]
    requestList = [{'location': [lat, lon], 'measure': [measure]}]
    stations = json.loads(requests.get('https://api.ust.is/aq/a/getStations').text)

    # find closest station with measure
    minDist = 1000000 # meters?
    id = -1
        
    for index, station in enumerate(stations):
        # lat = station['latitude']
        # lon = station['longitude']
        measures = station['parameters']

        for request in requestList: # process each request
            # filter out stations that don't measure the request
            hasMeasure = False
            for test in request['measure']:
                if test in measures and station['activity_end'] == None:
                    hasMeasure = True
            
            if hasMeasure:
                lat1 = float(station['latitude'])
                lon1 = float(station['longitude'])
                lat2 = request['location'][0]
                lon2 = request['location'][1]
                thisDist = dist(lat1, lon1, lat2, lon2)

                if thisDist < minDist:
                    minDist = thisDist
                    id = index

    if id >= 0:
        return {'station_id': stations[id]['local_id'], 'station_name': stations[id]['name']}
    else:
        return {'station': 'NO STATION FOUND'}
    
@app.get('/get-current-station-data')
async def get_current_station_data(id: str, measure: str):
    """[summary]

    Args:
        id (str): [description]
        measure (str): [description]

    Returns:
        JSON Object: The most reasent measurement from a stations
    """    
    stations_one_day_data = json.loads(requests.get('https://api.ust.is/aq/a/getLatest').text)
    value = stations_one_day_data[id]['parameters'][measure]['0']['value']
    measurement_endtime = stations_one_day_data[id]['parameters'][measure]['0']['endtime']
    unit = stations_one_day_data[id]['parameters'][measure]['unit']
    
    return {'station_id': id, 'timestamp': measurement_endtime, 'measurement_variable': measure, 'value': value, 'unit': unit}

@app.post('/register-alarm')
async def register_alarm(phone_number: str, lat: float, lon: float, variable: str, passkey: str):
    pass

@app.post('/deregister-alarm')
async def deregister_alarm(phone_number: str, variable: str, passkey: str):
    pass

@app.post('/list-alarms')
async def list_alarms(phone_number: str, passkey: str):
    pass

@app.get('/get-passkey')
async def get_passkey(phone_number: str):
    pass
