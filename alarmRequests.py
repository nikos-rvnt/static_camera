import requests 
'''
testQuadLatitude = 38.00321
testQuadLongitude = 27.00000

'''
def reqGet( latLong, where):
    URL = "http://localhost:3000/" + where
    PARAMS = {'latitude': latLong[0], 'longitude': latLong[1]} 
    r = requests.get(url = URL, params = PARAMS)
    return r

def newAlarm(latitude, longitude):

    r = reqGet( (latitude, longitude), "new_alarm")
    
    return r


# prepei na einai syndedemeno to quad me to systima kai na 
# exei sima gps
def getQuadCoords():
    '''
    global testQuadLatitude, testQuadLongitude
    return [testQuadLatitude, testQuadLongitude]
    '''
    URL = "http://localhost:3000/quad_latest_data"
    r = requests.get(url = URL)
    jsonObj = r.json()
    return [jsonObj["lat"], jsonObj["lon"]]


def validateAlarm( latitude, longitude):
    '''
    URL = "http://localhost:3000/validate_alarm"
    parameters = {'latitude': latitude, 'longitude':longitude}
    r = requests.get(url = URL, params = parameters)
    '''
    r = reqGet( (latitude, longitude), "validate_alarm")
    
    return r


# diagrafei ton synagermo apo tin proswrini mnimi
def deleteAlarm():
    
    URL = "http://localhost:3000/delete_key"
    parameters = {'key': 'newAlarm'}
    r = requests.get( url = URL, params = parameters)
    
    return r

def falseAlarm():
    URL = "http://localhost:3000/unvalidate_alarm"
    r = requests.get( url = URL)
    
    return r
    
# epistrefei energous "synagermous"
def getActiveAlarm():
    
    URL = "http://localhost:3000/active_alarm"
    r = requests.get(url = URL)
    jsonObj = r.json()
    
    return [jsonObj["lat"], jsonObj["lon"]]

