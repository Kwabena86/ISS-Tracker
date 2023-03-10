

 PART ONE

                             BUDDY FLASK (INTERNATIONAL SPACE STATION(ISS) TRACKER)

This project is based on realtime data that provides us information ISS that helps to determine the speed and location of the system depending on the data collected.The data contains ISS state vectors over an ~15 day period.The determination of speed and the location of the ISS depending on when the data was collected.The speed and location may vary.The data collected helps to get interesting information from the ISS data sets. 


                                            DATA RETRIEVED

The data used fro the project is accessed from the the url link from ISS Trajectory Data website (url:https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml).The from the site https://spotthestation.nasa.gov/trajectory_data.cfm. The url link is loaded into the script through API request from the python requests library.By performing these commands to get access to the data.
                                        INSTALLING DEPENDENCIES
  install: pip3 install flask
  install: pip3 install requests
  ininstall: pip3 install xmltodict
  intstall: geopy
  import xmldodict
  import requests
  import json

                                               PARTS TWO

Writing Flask application that runs the application on the local port. The application will queries data form the ISSposition and velocity. The curl route will be used to run the data sets in other to get our requests from the Flask application. The Routes used are as follows.

       ROUTES                       METHOD                             RETURS(OUTPUTS)

        /                            GET                  The entire data set

       /epochs                       GET                  A list of all Epochs in the data set

       /epochs/<epoch>               GET                  State vectors for a specific Epoch from the data set

       /epochs/<epoch>/speed         GET                  Instantaneous speed for a specific Epoch in the data set (math required!)

       /epochs?limit=int&offset=int  GET                  Return modified list of Epochs given query parameters

       /help                         GET                  Return help text (as a string) that briefly describes each route

       /delete-data                  DELETE               Delete all data from the dictionary object

       /post-data                    POST                 Reload the dictionary object with data from the web

       /comment                                           Return ‘comment’ list object from ISS data

       /header                       GET                  Return ‘header’ dict object from ISS data

       /metadata                     GET                  Return ‘metadata’ dict object from ISS data

       /epochs/<epoch>/location      GET                  Return latitude, longitude, altitude, and geoposition for given Epoch

       /now                          GET                  Return latitude, longitude, altidue, and geoposition for Epoch that is nearest in time


                                             INSTRUCTIONS TO RUN
METHOD (Prefered) -  Docker-compose

Pull docker image from dockerhub using - docker pull samboateng/iss_tracker_mit

Run this command in the termknal - docker-compose up

Run this command in a seperate terminal which is a curl command - curl 'localhost:5000/help'



                                           INSTUCTIONS CURL OUTPUT

The following commands should be run in terminal to other to run flask.

    flask --app iss_tracker --debug run

This command will start the flask terminal,the command should be exercuted on a different terminal.The following routes should be exercuted with the curl requests to achieved the expected results.

                                         ROUTES COMMANDS USING CURL

   1  curl localhost:5000/

    The command should returns the following output represent the path of the data set from ISS 
 {
 "EPOCH": "2023-063T11:59:00.000Z",
 "X": { 
     "#text": "2511.5681106492402",
     "@units": "km"
     },
 "X_DOT": {
     "#text": "5.2410359153923798",
     "@units": "km/s"
"Y":{
    "#text": "-5991.3267501460596",
    "@units": "km"
     },
"Y_DOT": {
         "#text": "0.32894397165270001",
         "@units": "km/s"
     }
"Z":{
    "#text": "1991.1683453687999",
    "@units": "km" }, 
"Z_DOT":{
    "#text": "-5.57976406061041",
    "@units": "km/s"
                                                         }
     },

   ]



    2  curl localhost:5000/epochs

    The command returns the following output of the epoch data set value as shown below
   [
     "2023-058T12:00:00.000Z",
     "2023-058T12:04:00.000Z",
     "2023-058T12:08:00.000Z",
     "2023-058T12:12:00.000Z",
     "2023-058T12:16:00.000Z",
     "2023-058T12:20:00.000Z",
     "2023-058T12:24:00.000Z",
     "2023-058T12:28:00.000Z",
     "2023-058T12:32:00.000Z",
     "2023-058T12:36:00.000Z"
   ]



   3 curl localhost:5000/epochs/<epoch>

    Will return

   The command returns the following output of the state vector of the specific epoch specified in the angled brackets as shown below
    {
     "EPOCH": "2023-048T12:00:00.000Z",
     "X": {
         "#text": "-5097.51711371908",
         "@units": "km"
                              },
     "X_DOT": {
         "#text": "-4.5815461024513304",
         "@units": "km/s"
     },
     "Y": {
         "#text": "1610.3574036042901",
         "@units": "km"
                                  },
     "Y_DOT": {
         "#text": "-4.8951801207083303",
         "@units": "km/s"
     },
     "Z": {
         "#text": "-4194.4848049601396",
         "@units": "km"
     },
     "Z_DOT": {
         "#text": "3.70067961081915",
         "@units": "km/s"
         }
     }



   4 curl localhost:5000/epochs/<epoch>/speed

    The command returns the following output of the epoch speed in the angled brackets as shown below
    {
            "Cartesian velocity vector_speed": 7.658223206788738
    }


    5 curl localhost:5000/epochs/?/limit=5

    Will return the following five data set, it sets the number of results by the app.The query accepts on integer values, any number with a float character will return error.

[
  "2023-067T12:00:00.000Z",
  "2023-067T12:04:00.000Z",
  "2023-067T12:08:00.000Z",
  "2023-067T12:12:00.000Z",
  "2023-067T12:16:00.000Z"
]


    Running the following command:

   6 curl 'localhost:5000/help returns:All available routes with their methods

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
     
    7 curl -X DELETE 'localhost:5000/delete-data
 
    Return : Data delete

    8 curl -X POST 'localhost:5000/poat-data
 
    Return: Post delete

    9 curl 'localhost:5000/comment'

    return some comment data as this display of this output
  [
  "Units are in kg and m^2",
  "MASS=473291.00",
  "DRAG_AREA=1421.50",
  "DRAG_COEFF=2.80",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2023-03-08T12:50:10.295 $ ORBIT = 2617 $ LAN(DEG) = 108.61247",
  "ISS last asc. node : EPOCH = 2023-03-23T11:58:44.947 $ ORBIT = 2849 $ LAN(DEG) = 32.65474",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "GMT067 Reboost        067:19:47:00.000             0.6     428.1     408.4",
  "(2.0)   (231.1)   (220.5)",
  null,
  "Crew05 Undock         068:22:00:00.000             0.0     428.7     409.6",
  "(0.0)   (231.5)   (221.2)",
  null,
  "SpX27 Launch          074:00:30:00.000             0.0     428.3     408.7",
  "(0.0)   (231.2)   (220.7)",
  null,
  "SpX27 Docking         075:12:00:00.000             0.0     428.2     408.6",
  "(0.0)   (231.2)   (220.6)",
  null,
  "=============================================================================",
  "End sequence of events"
  ]


    10 curl 'localhost:5000/header'

    return the header data on the display
   {
  "CREATION_DATE": "2023-067T21:02:49.080Z",
  "ORIGINATOR": "JSC"
   }

    11 curl 'localheader:5000/metadata'

    returns the the metadata set as follows
  {
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2023-067T12:00:00.000Z",
  "STOP_TIME": "2023-082T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
  }

    11 curl localhost:5000/epochs/<epoch>/location

    return the following

    curl localhost:5000/epochs/"2023-067T12:16:00.000Z"/location
  {
  "Altitude": 434.11046173598425,
  "Geo": "Over the Ocean",
  "Latitude": -45.696156101778115,
  "Longitude": 34.273406982421875
  }

    12 curl localhost:5000/now 

    returns a specific and relevant information about where the ISS is at the EPOCH closest to current(now)

    {
  "Closest Epoch": "2023-069T14:11:00.000Z",
  "Location": {
    "Altitude": {
      "Value": 432.06663395991745,
      "units": "km"
    },
    "Geo": "Over the Ocean",
    "Latitude": -42.67692799443817,
    "Longitude": 108.58612060546875
  },
  "Second from now": {
    "EPOCH": "2023-069T14:11:00.000Z",
    "X": {
      "#text": "2438.8308700822499",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "-3.9242687502873701",
      "@units": "km/s"
    },
    "Y": {
      "#text": "5075.7055823115697",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "5.0426165124751003",
      "@units": "km/s"
    },
    "Z": {
      "#text": "-3817.2021763228299",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "4.2093601876543998",
      "@units": "km/s"
    }
  }
}
    
    
   



     
 


