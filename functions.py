from geopy.geocoders import Nominatim
import datetime
import os
import config as config
import threading

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

    def __str__(self):# will return object as a string in e.g. print statement
        return f"Damage_ID:{self.damage_id}\nGPS:{self.lat}\\{self.lon}\nClass:{self.damageclass}\nSeverity:{self.severity}\nWeather:{self.weather}\nTimestamp:{self.timestamp}\nUser_id:{self.user_id}\nRepair_status:{self.repair_status}\nPath_to_picture:{self.piture_path}\n"

class Filter():
    areaselection = []
    severityselection = {1,2,3} #class = set (like list but no duplicates)
    classselection = {'Pothole','Crack','Alligator Crack'} #class = set (like list but no duplicates)
    weatherselection = {1,0} #class = set (like list but no duplicates)
    userselection = []
    repairstatusselection = {1,0} #class = set (like list but no duplicates)


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
    


def run_rdd(source_file_path, detection_mode = None):

    current_path = os.path.dirname(__file__) 
    
    

    path_to_Yolo_folder = f'{current_path}\\yolov7'
    print(path_to_Yolo_folder)

    weights = config.weights
    imgagesize = config.imgagesize
    confidence = config.confidence

    detect_file_path = f'{path_to_Yolo_folder}\detect.py'
    

    if detection_mode == 'Live mode':
        source_file_path = 0
    os.chdir(path_to_Yolo_folder)
    command = f'python "{detect_file_path}" --weights "{weights}"  --conf {confidence} --source "{source_file_path}" --save-txt'#f'python "{detect_file_path}" --weights "{weights}" --img {imgagesize} --conf {confidence} --source "{source_file_path}" --save-txt --project RDD --view-img'
    #print("python detect.py --weights yolov7.pt --conf 0.25 --img-size 640 --source 1.jpg")
    print(command)
    #os.system("python detect.py --weights yolov7.pt --conf 0.25 --img-size 640 --source 1.jpg")

    t1 = threading.Thread(target=os.system, args=(command,))
    t1.start()
    return t1


