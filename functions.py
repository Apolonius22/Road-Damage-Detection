from geopy.geocoders import Nominatim
import datetime
import os
current_path = os.path.dirname(__file__) 

class Damage:
    
    def __init__(self, damage_id, lat, lon, damageclass, severity, weather, timestamp, user_id, repair_status, piture_path):

        damagetypelist=['Pothole','Crack','Alligator Crack'] 


        self.damage_id = damage_id
        self.lat = lat
        self.lon = lon
        self.damageclass = damagetypelist[damageclass]
        self.severity = severity
        self.weather = weather
        self.timestamp = timestamp
        self.user_id = user_id
        self.repair_status = repair_status
        self.piture_path = piture_path

    def __str__(self):
        return f"Damage_ID:{self.damage_id}\nGPS:{self.lat}\\{self.lon}\nClass:{self.damageclass}\nSeverity:{self.severity}\nWeather:{self.weather}\nTimestamp:{self.timestamp}\nUser_id:{self.user_id}\nRepair_status:{self.repair_status}\nPath_to_picture:{self.piture_path}\n"

class Filter():
    areaselection = []
    severityselection = {1,2,3}
    classselection = {'Pothole','Crack','AlligatorCrack'}
    weatherselection = {1,0}
    userselection = []
    repairstatusselection = {1,0}


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_adress(Latitude,Longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(Latitude) + "," + str(Longitude))

    return location


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)



def detect_with_yolo():
    pass
    

###### This is a Test#########