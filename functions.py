from geopy.geocoders import Nominatim
import datetime
import os
import config as config
import threading
import cv2
import numpy as np
import subprocess 

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


def create_gpx(source_file, gpx_file = None):

    current_path = os.path.dirname(__file__) 
    file_name = source_file.split('\\')[-1]
    file_name = file_name[:file_name.rfind('.')]

    path_to_exif = os.path.join(current_path, "tools","exiftool.exe")
    fmt_file = os.path.join(current_path, "tools", "gpx.fmt")

    if gpx_file == None:
        gpx_file = None
    with open(gpx_file, "w+") as gpx_file:
        exiftool_command = [path_to_exif , f'{source_file}' , "-p" , f'{fmt_file}' , "-ee"]
        subprocess.run(exiftool_command,stdout = gpx_file)

def grab_contours(cnts):
    # OpenCV v2.4, v4-official
    if len(cnts) == 2:
        return cnts[0]
    # OpenCV v3
    elif len(cnts) == 3:
        return cnts[1]





def get_intensity_of_damage(img,data):

    damages = []
    print(f"detecting")
    dh, dw, _ = img.shape
    img = cv2.resize(img, (int(dw/3), int(dh/3))) 
    dh, dw, _ = img.shape 

    for index, dt in enumerate(data):

        # Split string to float
        id = dt[0]
        _, x, y, w, h = map(float, dt.split(' '))
        

        # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
        # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)
        
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1


        #cv2.imshow("edged", img)
        #cv2.waitKey(0)

        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (l, t), (r, b), 255, -1)
        mask = mask.astype(np.uint8)
        masked_img = cv2.bitwise_and(img,img, mask = mask) 
        #cv2.imshow("edged", img)
        #cv2.waitKey(0)
        gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 120, 255, 1)
        #cv2.imshow("edged", edged)
        #cv2.waitKey(0)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)

        contour_image = edged.copy()
        area = 0

        for c in cnts:
            area += cv2.contourArea(c) 
            cv2.drawContours(contour_image,[c], 0, (100,5,10), 3)

        damages.append((id , area))

        if True:
            file_name = "severity_" + str(index) + ".png"
            print(file_name)
            cv2.imwrite("severity_" + str(index) + ".png", contour_image)

        if False:
            cv2.putText(contour_image, str(area), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)

            cv2.imshow("area", contour_image)
            cv2.waitKey(0)

    
    return damages

