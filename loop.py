import json
import requests
import math

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

# request format: [[lat, lon],[measure 1, measure 2, ...]]
requestList = [{'location': [64.141430, -21.914849], 'measures': ['H2S']}]

stations = json.loads(requests.get('https://api.ust.is/aq/a/getStations').text)

# find closest station with measure
minDist = 1000000
id = -1

for index, station in enumerate(stations):
    lat = station['latitude']
    lon = station['longitude']
    measures = station['parameters']

    for request in requestList: # process each request
        # filter out stations that don't measure the request
        hasMeasure = False
        for test in request['measures']:
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
    print('Næsta stöð sem mælir þessi gögn er:', stations[id]['name'])
else:
    print('Engin stöð fannst.')