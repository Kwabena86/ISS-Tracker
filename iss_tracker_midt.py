
from flask import Flask,request
import requests
import xmltodict 
import math
from geopy.geocoders import Nominatim
from datetime import datetime
from geopy.distance import geodesic
import json
import time


app = Flask(__name__)

MEAN_EARTH_RADIUS = 6371

data = {}
entire_data = {}



def get_data():
    """
    The function returns all of the data in the corresponding ste
    
    Args:
        N/A
  
   Returns:
        List of dictionaries that will represent the collected data in the set of ISS locations
    """

    url ='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data['ndm']['oem']['body']['segment']['data']['stateVector']


def get_entire_data() -> dict:

    """
    The funtion returns the entire XML of data

    Args:
        N/A

    Returns:
        A dictionary with all of the data in the requested XML file

  
    """
    url ='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data

data = get_data()
entire_data = get_entire_data()

    

# The defaul curl command method without more aguments


@app.route('/', methods=['GET'])
def location():
    """
    The funtion returns all the data in the set

    Args:
        N/A
    Returns:
        List of dictionaries that will represent the collected data in the set of ISS loctions
    """
    try:
        data = get_data()
        return data
    except NameError:
        return "Data has been deleted, must be repost first using /post-data\n"
    return data



@app.route('/epochs/', methods= ['GET'])
def all_Epochs():

    """
    This function returns all of the EPOCHs in the set

    Args:
        N/A
    Returns:
        It will return a list of strings the represents the EPOCHs in the data set
    """


    data = get_data()

    try:
        limit = int(request.args.get('list',5))
    except ValueError:
        return "Error input. Please enter ant integer\n",400
    
    try:
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return 'Error input. Please enter ant integer\n",400'


    epochs = []
    total_Results = 0
    index = 0
    for e in data:
        if (total_Results == limit):
            break
        if (index >= offset):
             epochs.append(e['EPOCH'])
             total_Results+= 1
      
        index += 1
    return epochs



@app.route('/epochs/<epoch>', methods=['GET'])
def specific_Epoch(epoch):
    """
    The funtion take a perticular EPOCHs string value and returns its state vector 

    Args:
        N/A

    Returns:
        Returns a specific data for a perticular epoch
    """
    data = get_data()

    try: 
        for e in data:
            if (e['EPOCH'] == epoch):
                return e
    except NameError:
        return "Data has been deleted, must be repost first using /post-data\n "
    return 'Epoch value error, not found\n'

@app.route('/epochs/<epoch>/speed', methods=['GET'])
def epoch_Speed(epoch):

    """
    It take in a specific EPOCH string values for a particular time duration that is recorded for the ISS

    Args:
        (String) epoch: EPOCH string value for a particular time that is recorded for the ISS

    Returns:
        The speed of the ISS at the given EPOCH

    """
    data = get_data()
    for e in data:
            if (e['EPOCH'] == epoch):
                vec_x = float(e['X_DOT']['#text'])
                vec_y = float(e['Y_DOT']['#text'])
                vec_z = float(e['Z_DOT']['#text'])
                cart_vel_Vector_speed = math.sqrt(vec_x**2 +vec_y**2 + vec_z**2)
                return {"Cartesian velocity vector_speed":cart_vel_Vector_speed}
    return 'Epoch value error, not found\n'


@app.route('/delete-data', methods=['DELETE'])
def delate_Data():
    """
    The funtion deletes the global data object dictionary

    Args:
        N/A

    Returns:
        A data delete comfirmation message if calling the data variable which causes a NamrError
    """
    global data
    global entire_data
    try:
        del data
        del entire_data
    except NameError:
        return  "Data has been deleted, must be repost first using /post-data\n "
    return "Data deleted\n"



@app.route('/help', methods=['GET'])
def help() -> str:
    
    """
    The funtion return all tools needed in a summary discrption of all associated and avaailable routes and thier corresponding methods for this API

    Args:
        N/A

    Returns:
        Outputs in a form of text that enumerate all available routes and its corresponding methods

    """
    return '''
    Available Routes:
    
    GET / 
    Return entire data set


    GET /epochs
    Return list of all Epochs in the data set

    GET /epochs?limit=int&offset=int
    Return modified list of Epochs given query parameters

    GET/ epochs/<epoch>
    Return state vectors for a specific Epoch from the data set

    GET /epochs/<epoch>/speed
    Return instantaneous speed for a specific Epoch in the data set (math required!)

    GET /help
    Return help text (as a string) that briefly describes each route

    DELETE /delete-data
    Delete all data from the dictionary object

    POST /post-data
    Reload the dictionary object with data from the web

    '''


@app.route('/post-data', methods=['POST'])
def post_Data() -> str:

    """
    The function post data to the global data dictionary objects

    Args:
        N/A

    Returns:
        Data Post Successfully after setting the global data variable to the requested data sets
    """
    global data
    global entire_data
    data = get_data()

    return "Data Posted\n"
 

@app.route('/comment', methods=['GET'])
def comment() -> list:


     """
     This returns the comment that is recorded in the XML data file for the ISS

     Args:
         N/A

     Returns:
        The list of comments recorded in the XML data
            
     """
     global entire_data
     try:
         return entire_data['ndm']['oem']['body']['segment']['data']['COMMENT']
     except NameError:
        return " Data has been deleted and must be reposted first using /post-data\n"


@app.route('/header', methods=['GET'])
def header() -> dict:

     """
     This returns the header recorded in the XLM data file for the ISS

     Args:
         N/A

     Returns:
        The header of the XML data in a dictionary format

     """


     global entire_data
     try:
        return entire_data['ndm']['oem']['header']
     except NameError:
        return "Data has been deleted and must be reposted first using /post-data\n"

@app.route('/metadata', methods=['GET'])
def metadata() -> dict:

     """
     This returns the metadata that is recorded in the XML data file for the ISS

     Args:
         N/A

     Returns:
         The metadata of the XML data in a dictionary format

     """


     global entire_data
     try:
        return entire_data['ndm']['oem']['body']['segment']['metadata']
     except NameError:
        return "Data has been deleted and must be reposted first using /post-data\n"

@app.route('/epochs/<epoch>/location', methods=['GET'])
def get_Epoch_location(epoch):

     """
     This returns relevant epoch location data from the dataset for the ISS

     Args:
         Epoch (String): The time stamp of the ISS data

     Returns:
        In dictionary format the following:
                Longitude: In degrees
                Latitude: In degrees
                Altitude: Altitude from sea level (km)
                Geolocation: Position over Earth

     """
     global data
     try:

         for e in data:
             if e["EPOCH"] == epoch:
                x = float(e["X"]["#text"])
                y = float(e["Y"]["#text"])
                z = float(e["Z"]["#text"])
                hrs = int (epoch[9]*10 + epoch[10])
                mins = int(epoch[12]*10 + epoch[13])

                lat = math.degrees(math.asin((z/ math.sqrt(x**2 + y**2))))
                lon = math.degrees(math.atan2(y, x)) -  ((hrs-12)+(mins/60))*(360.0/24) + 32
                alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS

                while (lon < -180):
                    lon = lon + 360
                while (lon > 180):
                    lon = lon - 360
                while (lat > 90):
                    lat = lat - 180
                while (lat < -90):
                    lat = lat + 180
                geocoder = Nominatim(user_agent = 'iss_trcaker')
                geoloc = geocoder.reverse((lat, lon), zoom=5,language='en')
                try:
                    return {"Latitude": lat, "Longitude": lon, "Altitude": alt, "Geo":geoloc.address}
                except AttributeError:
                    return {"Latitude": lat, "Longitude": lon, "Altitude": alt, "Geo":"Over the Ocean"}

     except NameError:
            return "Data has been deleted and must be reposted first using /post-data\n"

     return "Error: Epoch not found\n"

@app.route('/now', methods=['GET'])
def get_Now():

     """
     This returns relevant epoch location data from the epoch that is closest to the current time

     Args:
          N/A

     Returns:
        In dictionary format the following:
                Location:
                Longitude: In degrees
                Latitude: In degree
                Altitude: Altitude from sea level (km)
                Geolocation: Position over Earth
                Closet Epoch: Written in standard epoch notation
                Second from now: (s)

     """    

     global data
    # try:
     time_now = time.time()
     epoch_closest = None
     time_difference_closest = None
     for e in data:
         epoch_datetime = time.mktime(time.strptime(e['EPOCH'] [:-5],'%Y-%jT%H:%M:%S'))
         difference = abs(epoch_datetime-time_now)
         if (time_difference_closest is None or difference < time_difference_closest):
             time_difference_closest = difference
             epoch_closest = e
     epoch_name = epoch_closest['EPOCH']
     x = float(epoch_closest["X"]["#text"])
     y = float(epoch_closest["Y"]["#text"])
     z = float(epoch_closest["Z"]["#text"])
     hrs = int (epoch_name[9]*10 + epoch_name[10])
     mins = int(epoch_name[12]*10 + epoch_name[13])

     lat = math.degrees(math.asin((z/ math.sqrt(x**2 + y**2))))
     lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 32


     while(lon < -180):
         lon = lon + 360
     while(lon > 180):
         lon = lon - 360
     while(lat > 90):
         lat = lat - 180
     while(lat < -90):
         lat = lat + 180

     distance_from_origion = math.sqrt(x**2 + y**2 + z**2)
     altitude = distance_from_origion - MEAN_EARTH_RADIUS
     geocoder = Nominatim(user_agent='iss_tracker')
     geolocator =geocoder.reverse((lat,lon)) 

     try:
         return {"Closest Epoch": epoch_name, "Seconds from now": epoch_closest,"Location":{"Latitude": lat,"Longitude": lon, "Altitude":{"Value": altitude, "units": "km" }, "Geo":geolocator.address}}


     except AttributeError:
         return {"Closest Epoch": epoch_name, "Second from now":epoch_closest,"Location":{"Latitude": lat,"Longitude": lon, "Altitude":{"Value": altitude, "units": "km" }, "Geo":"Over the Ocean"}}


     #except NameError:
             
      #   return "Data has been deleted and must be reposted first using /post-data\n"
     

     return "Error:Epoch not found\n"




            
if __name__  ==  '__main__ ': 
    app.run(debug=True, host='0.0.0.0')

